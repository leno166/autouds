"""
Mock ECU —— 持续尝试连接 13400 端口，处理 DoIP 诊断帧。
直接运行：python tests/mock_ecu.py
"""
import socket
import struct
import time

HOST = '127.0.0.1'
PORT = 13400

DOIP_VERSION = 0x02
DOIP_INVERSE = 0xFD
DIAG_MSG = 0x8001


def recv_exact(sock: socket.socket, size: int) -> bytes:
    data = bytearray()
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError('连接已关闭')
        data.extend(chunk)
    return bytes(data)


def recv_frame(sock: socket.socket) -> tuple[int, bytes] | None:
    """接收一帧 DoIP，返回 (payload_type, payload)。失败返回 None。"""
    try:
        header = recv_exact(sock, 8)
    except (ConnectionError, OSError):
        return None
    version, inverse, ptype, length = struct.unpack('!BBHL', header)
    try:
        payload = recv_exact(sock, length)
    except (ConnectionError, OSError):
        return None
    return ptype, payload


def build_frame(payload_type: int, payload: bytes) -> bytes:
    header = struct.pack('!BBHL', DOIP_VERSION, DOIP_INVERSE, payload_type, len(payload))
    return header + payload


def handle_diag(sock: socket.socket, payload: bytes):
    """处理诊断帧：交换 SA/TA，变换 UDS SID + 追加 00，回传。"""
    if len(payload) < 5:
        return

    sa = payload[0:2]   # 源地址 (tester)
    ta = payload[2:4]   # 目标地址 (ECU)
    uds = payload[4:]   # UDS 请求

    if not uds:
        return

    print(f'[MockEcu] 收到 UDS: {uds.hex(" ").upper()}')

    # 响应：SID | 0x40 + 原数据[1:] + 00
    resp_uds = bytes([uds[0] | 0x40]) + uds[1:] + b'\x00'
    print(f'[MockEcu] 回传 UDS: {resp_uds.hex(" ").upper()}')

    # 封装 DoIP，地址互换
    resp_payload = ta + sa + resp_uds
    frame = build_frame(DIAG_MSG, resp_payload)
    try:
        sock.sendall(frame)
    except OSError:
        print('[MockEcu] 发送失败')


def serve(sock: socket.socket):
    """连上后的 DoIP 收发循环。"""
    while True:
        result = recv_frame(sock)
        if result is None:
            print('[MockEcu] 对端断开')
            break

        ptype, payload = result
        if ptype == DIAG_MSG:
            handle_diag(sock, payload)
        else:
            print(f'[MockEcu] 忽略 Payload Type: 0x{ptype:04X}')


def main():
    print(f'[MockEcu] 目标 {HOST}:{PORT}，开始连接循环 ...')
    while True:
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            print(f'[MockEcu] 尝试连接 {HOST}:{PORT} ...')
            sock.connect((HOST, PORT))
            sock.settimeout(None)  # 清除 connect 阶段的超时
            print(f'[MockEcu] 已连接 {HOST}:{PORT}，等待数据 ...')
            serve(sock)
        except (ConnectionRefusedError, OSError, socket.timeout):
            pass
        except KeyboardInterrupt:
            print('\n[MockEcu] 退出')
            break
        finally:
            if sock:
                try:
                    sock.close()
                except OSError:
                    pass

        time.sleep(1)


if __name__ == '__main__':
    main()