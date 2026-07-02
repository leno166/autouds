"""
Tester —— 用 autouds 连接 MockEcu，发送 22 10 03 并打印返回值。
直接运行：python tests/tester.py
"""
import logging
from autouds import App
from autodoip import Config as DoIpConfig

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
)

print('启动 App，等待 ECU 连接 ...')
try:
    app = App(
        ip='127.0.0.1',
        ecus={'mock': (0x1001, '127.0.0.1', 0)},
        port=13400,
        doip_config=DoIpConfig(accept_timeout=5.0, p6_timeout=3.0),
    )
    print('App 启动完成，发送 22 10 03 ...')
    result = app.read_did(0x1003)
    print(f'返回值: {result.hex(" ").upper()}')
except Exception as e:
    print(f'错误: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()