"""
@文件: _handler.py
@作者: 雷小鸥
@日期: 2026/6/11 12:01
@许可: MIT License
@描述: handler 装饰器 + 发送桥接。
@版本: Version 0.1
"""
from __future__ import annotations

import functools
import logging
from typing import Callable, Generator, ParamSpec, TypeVar
from ._models import Request, Response, UdsError

_log = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def handler(*args, **kwargs):
    """装饰器工厂：预建 Request，驱动用户生成器完成 UDS 交互。"""
    fn = args[0] if len(args) == 1 else None

    def decorator(f: Callable[..., Generator[bytes | None, Response, R]]) -> Callable[..., R]:
        @functools.wraps(f)
        def wrapper(self, *inner_args, **inner_kwargs):
            # 1. 从装饰器参数取初始值（可能为 None）
            s_name = kwargs.get('service_name', None)
            s_id = kwargs.get('s_id', None)
            fn_name = kwargs.get('sub_fn_name', None)
            sub_fn = kwargs.get('sub_fn', None)
            supp = kwargs.get('suppress_positive_response', None)

            # 2. 调用时关键字覆盖：不传则保留装饰器参数（get 不删除，函数需要时也能收到）
            s_name = inner_kwargs.get('service_name', s_name)
            s_id = inner_kwargs.get('s_id', s_id)
            fn_name = inner_kwargs.get('sub_fn_name', fn_name)
            sub_fn = inner_kwargs.get('sub_fn', sub_fn)
            supp = inner_kwargs.get('suppress_positive_response', supp)

            # 3. 最终默认值
            if supp is None:
                supp = False

            # 4. 工厂形式：驱动生成器获取 params
            gen = f(self, *inner_args, **inner_kwargs)
            params = next(gen)  # 驱动生成器到第一个 yield
            if params is not None and not isinstance(params, bytes):
                _log.error(
                    '%s.%s 第一个 yield 类型错误：期望 bytes 或 None，实际 %s，值=%r',
                    type(self).__name__,
                    f.__name__,
                    type(params).__name__,
                    params if len(repr(params)) <= 200 else repr(params)[:200] + '…',
                )
                raise TypeError(
                    f'{type(self).__name__}.{f.__name__} '
                    f'第一个 yield 必须为 bytes 或 None，实际为 {type(params).__name__}'
                ) from None

            request = Request.model_validate({
                'service_name'              : s_name,
                'service_id'                : s_id,
                'sub_fn_name'               : fn_name,
                'sub_fn'                    : sub_fn,
                'suppress_positive_response': supp,
                'params'                    : params
            })

            # 5. 发送请求、收集响应
            resp: Response | None = None
            for raw in self._send_impl(request.raw):
                resp = Response.model_validate({
                    'raw': raw, 'request': request, 'father': resp
                })
                if not (resp.is_negative and resp.nrc == 0x78):
                    break

            if resp is None:
                resp = Response.model_validate({'request': request})

            if resp.is_negative:
                raise UdsError(resp)

            try:
                gen.send(resp)
            except StopIteration as e:
                return e.value
            finally:
                gen.close()

            raise RuntimeError(
                "generator must return immediately after receiving Response"
            )

        return wrapper

    return decorator(fn) if fn else decorator
