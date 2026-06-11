"""
@文件: _models.py
@作者: 雷小鸥
@日期: 2026/6/11 12:02
@许可: MIT License
@描述:
    UDS Request / Response 模型

    Request — 构造时可用 model_validate 传入语义名，内部查表转换：
    - Request.model_validate({'service_name': 'session', 'sub_fn_name': 'default'})
    - Request.model_validate({'service_id': 0x10, 'sub_fn': 0x01})

    Response — 两阶段：先创建空壳，收到 raw 后 _parse 填充

@版本: Version 0.1
"""

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator, PrivateAttr
from ._tables import SERVICE_MAP, SUB_FN_MAP, NRC_MAP


# ═══════════════════════════════════════════════════════════════════════
# Request
# ═══════════════════════════════════════════════════════════════════════

class Request(BaseModel):
    service_id: int = Field(..., ge=0x00, le=0xFF)
    sub_fn: int | None = Field(None, ge=0x00, le=0x7F)
    suppress_positive_response: bool = False

    params: bytes | None = Field(None)

    _fn_byte: bytes | None = PrivateAttr(None)

    # noinspection PyPropertyDefinition
    @property
    def raw(self) -> bytes:
        return self.service_id.to_bytes(1, 'big') + (self._fn_byte or b'') + (self.params or b'')

    # noinspection PyPropertyDefinition
    @property
    def hex(self) -> str:
        return ' '.join(f'{b:02X}' for b in self.raw)

    # noinspection PyNestedDecorators
    @model_validator(mode='before')
    @classmethod
    def _preprocess(cls, data):
        """统一处理 service_name / sub_fn_name，并按依赖顺序验证。"""
        if not isinstance(data, dict):
            return data

        # 1. 解析 service_name -> service_id
        s_name = data.pop('service_name', None)
        if s_name is not None:
            resolved_sid = SERVICE_MAP.get(s_name)
            if resolved_sid is None:
                raise ValueError(f'未知服务名: {s_name!r}')
            existing_sid = data.get('service_id')
            if existing_sid is not None and existing_sid != resolved_sid:
                raise ValueError(
                    f'service_name({s_name!r}) 与 service_id(0x{existing_sid:02X}) 冲突'
                )
            data['service_id'] = resolved_sid

        # 2. 尝试获取 service_id（可能上一步已设置，或用户直接提供）
        s_id = data.get('service_id')

        # 3. 解析 sub_fn_name -> sub_fn（此时必须已知 service_id）
        sub_fn_name = data.pop('sub_fn_name', None)
        if sub_fn_name is not None:
            if s_id is None:
                raise ValueError(
                    '提供了 sub_fn_name 但未指定服务，请同时提供 service_id 或 service_name'
                )
            table = SUB_FN_MAP.get(s_id)
            if table is None or not table.get('enable'):
                raise ValueError(
                    f'服务 0x{s_id:02X} 不支持子功能，却提供了 sub_fn_name: {sub_fn_name!r}'
                )
            resolved_fn = table.get(sub_fn_name)
            if resolved_fn is None:
                raise ValueError(
                    f'未知子功能名: {sub_fn_name!r} (服务 0x{s_id:02X})'
                )
            existing_fn = data.get('sub_fn')
            if existing_fn is not None and existing_fn != resolved_fn:
                raise ValueError(
                    f'sub_fn_name({sub_fn_name!r}) 与 sub_fn(0x{existing_fn:02X}) 冲突'
                )
            data['sub_fn'] = resolved_fn

        # 4. 验证直接传入的 sub_fn 值（如果存在）
        fn = data.get('sub_fn')
        if fn is not None:
            if not isinstance(fn, int) or not (0x00 <= fn <= 0x7F):
                raise ValueError('sub_fn 必须是 0x00~0x7F 的整数')
            if s_id is None:
                raise ValueError('提供了 sub_fn 但未指定服务，请同时提供 service_id 或 service_name')
            table = SUB_FN_MAP.get(s_id)
            if table is None or not table.get('enable'):
                raise ValueError(f'服务 0x{s_id:02X} 不支持子功能，却提供了 sub_fn=0x{fn:02X}')

            allowed_values = {v for k, v in table.items() if k != 'enable'}
            if fn not in allowed_values:
                raise ValueError(f'sub_fn=0x{fn:02X} 对于服务 0x{s_id:02X} 无效')

        return data

    @model_validator(mode='after')
    def _build_fn_byte(self):
        """根据 sub_fn 和 suppress_positive_response 构造功能字节。"""
        if self.sub_fn is None:
            self._fn_byte = b''
        else:
            fn_byte = self.sub_fn
            if self.suppress_positive_response:
                fn_byte |= 0x80
            self._fn_byte = fn_byte.to_bytes(1, 'big')
        return self


# ═══════════════════════════════════════════════════════════════════════
# Response
# ═══════════════════════════════════════════════════════════════════════

class Response(BaseModel):
    father: Response | None = None
    request: Request
    raw: bytes = b''

    # ── 解析后的字段 ──
    ok: bool = False
    is_negative: bool = False

    service_id: int = 0
    sub_fn: int | None = None
    params: bytes = b''

    request_id: int = 0
    nrc: int = 0
    nrc_desc: str = ''

    # noinspection PyPropertyDefinition
    @property
    def hex(self) -> str:
        return ' '.join(f'{b:02X}' for b in self.raw)

    @model_validator(mode='after')
    def _parse(self):
        if not self.raw:
            return self

        raw = self.raw
        s_id = raw[0]

        match s_id:
            case 0x7F:
                self.__handle_negative(raw)
            case _:
                self.__handle_positive(raw)
        return self

    def __handle_negative(self, raw: bytes):
        if len(raw) < 3:
            raise ValueError("负响应长度不足，至少需要 3 字节")
        request_id = raw[1]
        if request_id != self.request.service_id:
            raise ValueError(
                f"负响应的请求 SID 不匹配：期望 0x{self.request.service_id:02X}，"
                f"收到 0x{request_id:02X}"
            )
        self.request_id = request_id
        self.is_negative = True
        self.service_id = raw[0]
        self.nrc = raw[2]
        self.nrc_desc = NRC_MAP.get(self.nrc, "Unknown NRC")

    def __handle_positive(self, raw: bytes):
        expected_sid = self.request.service_id | 0x40
        s_id = raw[0]
        if s_id != expected_sid:
            raise ValueError(f"无效响应：期望 SID 0x{expected_sid:02X}，收到 0x{s_id:02X}")

        self.ok = True
        self.is_negative = False
        self.service_id = s_id

        # 判断服务是否需要子功能字节
        table = SUB_FN_MAP.get(self.request.service_id)
        need_sub_fn = (table is not None and table.get('enable', False))

        if not need_sub_fn:
            self.sub_fn = None
            self.params = raw[1:] if len(raw) > 1 else b''
            return

        if len(raw) < 2:
            raise ValueError(f"服务 0x{self.request.service_id:02X} 需要子功能，但响应缺少子功能字节")

        if self.request.sub_fn is None:
            raise ValueError("服务需要子功能但请求未提供子功能")

        response_sub_fn = raw[1]
        if response_sub_fn != self.request.sub_fn:
            raise ValueError(
                f"响应子功能不匹配：期望 0x{self.request.sub_fn:02X}，"
                f"收到 0x{response_sub_fn:02X}"
            )

        self.sub_fn = response_sub_fn
        self.params = raw[2:] if len(raw) > 2 else b''


# ═══════════════════════════════════════════════════════════════════════
# UdsError
# ═══════════════════════════════════════════════════════════════════════

class UdsError(Exception):
    """UDS 负响应异常，通过 resp 属性获取完整 Response。"""

    def __init__(self, resp: Response):
        self.resp = resp
        super().__init__(f'{resp.nrc_desc} 0x{resp.nrc:02X}')
