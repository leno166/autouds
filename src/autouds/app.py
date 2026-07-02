"""
@文件: app.py
@作者: 雷小鸥
@日期: 2026/6/10
@许可: MIT License
@描述: UDS App 基类，封装所有 UDS 服务方法
@版本: Version 0.1
"""
from typing import Generator
from autodoip import Endpoint, Config as DoIpConfig
from ._handler import handler
from ._models import Response


class App:
    def __init__(
            self,
            ecus: dict[str, tuple[int, str, int]],
            ip: str,
            port: int = 13400,
            tester: int = 0x0E80,
            doip_config: DoIpConfig | None = None,
    ):
        self._ecus = ecus
        self._first_name = next(iter(ecus))

        endpoint_ecus = {
            addr: (ecu_ip, port)
            for addr, ecu_ip, port in ecus.values()
        }

        self._endpoint = Endpoint(ip=ip, ecus=endpoint_ecus, port=port, tester=tester, config=doip_config or DoIpConfig())
        self._send_impl = self._endpoint.conversation
        self._endpoint.start()
        self._endpoint.select(ecus[self._first_name][0])
        App._latest = self

    def on(self, name: str):
        """切换到指定 ECU。"""
        addr, _, _ = self._ecus[name]
        self._endpoint.select(addr)

    # ═══════════════════════════════════════════════════════════════════
    # 诊断会话控制 (0x10)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='session', sub_fn_name='default')
    def default(self) -> Generator[None, Response, tuple[int, int]]:
        resp: Response = yield
        if not resp.params:
            return 0, 0
        params: bytes = resp.params
        p2 = int.from_bytes(params[0:2], byteorder='big')
        p2_star = int.from_bytes(params[2:4], byteorder='big') * 10
        return p2, p2_star

    @handler(service_name='session', sub_fn_name='program')
    def program(self) -> Generator[None, Response, tuple[int, int]]:
        resp: Response = yield
        if not resp.params:
            return 0, 0
        params: bytes = resp.params
        p2 = int.from_bytes(params[0:2], byteorder='big')
        p2_star = int.from_bytes(params[2:4], byteorder='big') * 10
        return p2, p2_star

    @handler(service_name='session', sub_fn_name='extend')
    def extend(self) -> Generator[None, Response, tuple[int, int]]:
        resp: Response = yield
        if not resp.params:
            return 0, 0
        params: bytes = resp.params
        p2 = int.from_bytes(params[0:2], byteorder='big')
        p2_star = int.from_bytes(params[2:4], byteorder='big') * 10
        return p2, p2_star

    @handler(service_name='session', sub_fn_name='safety')
    def safety(self) -> Generator[None, Response, tuple[int, int]]:
        resp: Response = yield
        if not resp.params:
            return 0, 0
        params: bytes = resp.params
        p2 = int.from_bytes(params[0:2], byteorder='big')
        p2_star = int.from_bytes(params[2:4], byteorder='big') * 10
        return p2, p2_star

    # ═══════════════════════════════════════════════════════════════════
    # ECU 复位 (0x11)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='reset', sub_fn_name='hard')
    def hard(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    @handler(service_name='reset', sub_fn_name='key')
    def key(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    @handler(service_name='reset', sub_fn_name='soft')
    def soft(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    # ═══════════════════════════════════════════════════════════════════
    # 待机握手 (0x3E)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='present', sub_fn_name='resp', suppress_positive_response=True)
    def present(self) -> Generator[None, Response, None]:
        yield

    # ═══════════════════════════════════════════════════════════════════
    # 安全访问 (0x27)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='unlock', sub_fn_name='L1')
    def l1(self) -> Generator[None, Response, bytes]:
        resp: Response = yield
        if not resp.params:
            return b''
        return resp.params

    @handler(service_name='unlock', sub_fn_name='L1 Ex')
    def l1_ex(self, payload: bytes) -> Generator[bytes, Response, None]:
        yield payload

    @handler(service_name='unlock', sub_fn_name='L5')
    def l5(self) -> Generator[None, Response, bytes]:
        resp: Response = yield
        if not resp.params:
            return b''
        return resp.params

    @handler(service_name='unlock', sub_fn_name='L5 Ex')
    def l5_ex(self, payload: bytes) -> Generator[bytes, Response, None]:
        yield payload

    @handler(service_name='unlock', sub_fn_name='L19')
    def l19(self) -> Generator[None, Response, bytes]:
        resp: Response = yield
        if not resp.params:
            return b''
        return resp.params

    @handler(service_name='unlock', sub_fn_name='L19 Ex')
    def l19_ex(self, payload: bytes) -> Generator[bytes, Response, None]:
        yield payload

    # ═══════════════════════════════════════════════════════════════════
    # 通讯控制 (0x28)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='comm', sub_fn_name='en_rx_tx')
    def comm_enable_rx_tx(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    @handler(service_name='comm', sub_fn_name='dis_rx_tx')
    def comm_disable_rx_tx(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    # ═══════════════════════════════════════════════════════════════════
    # 控制 DTC 设置 (0x85)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='dtc_setting', sub_fn_name='on')
    def dtc_on(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    @handler(service_name='dtc_setting', sub_fn_name='off')
    def dtc_off(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    # ═══════════════════════════════════════════════════════════════════
    # 清除诊断信息 (0x14)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='clear_dtc')
    def clear_dtc(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    # ═══════════════════════════════════════════════════════════════════
    # 读取故障信息码 (0x19)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='read_dtc', sub_fn_name='count_by_mask')
    def read_dtc_count(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    @handler(service_name='read_dtc', sub_fn_name='dtc_by_mask')
    def read_dtc_by_mask(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    # ═══════════════════════════════════════════════════════════════════
    # 标识符读数据 (0x22)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='read_did')
    def read_did(self, did: int) -> Generator[bytes, Response, bytes]:
        resp: Response = yield did.to_bytes(2, byteorder='big')
        if not resp.params:
            return b''
        return resp.params

    # ═══════════════════════════════════════════════════════════════════
    # 标识符写数据 (0x2E)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='write_did')
    def write_did(self, did: int, payload: bytes) -> Generator[bytes, Response, None]:
        yield did.to_bytes(2, byteorder='big') + payload

    # ═══════════════════════════════════════════════════════════════════
    # 通过标识符控制输入输出 (0x2F)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='io')
    def io_control(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    # ═══════════════════════════════════════════════════════════════════
    # 例行程序控制 (0x31)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='routine', sub_fn_name='start')
    def routine_start(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    @handler(service_name='routine', sub_fn_name='stop')
    def routine_stop(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    @handler(service_name='routine', sub_fn_name='result')
    def routine_result(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    # ═══════════════════════════════════════════════════════════════════
    # 上传下载类 (0x34 / 0x35 / 0x36 / 0x37)
    # ═══════════════════════════════════════════════════════════════════

    @handler(service_name='download')
    def request_download(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    @handler(service_name='upload')
    def request_upload(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    @handler(service_name='transfer')
    def transfer_data(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp

    @handler(service_name='exit_tf')
    def exit_transfer(self) -> Generator[None, Response, Response]:
        resp: Response = yield
        return resp
