"""
@文件: __main__.py
@作者: 雷小鸥
@日期: 2026/6/10 08:51
@许可: MIT License
@描述: UDS 诊断入口
@版本: Version 0.1
"""
import logging
from . import App

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    app = App(
        ip='<tester-ip>',
        ecus={
            'mcu': (0x1001, '<ecu-ip>', 0),
            'soc': (0x1002, '<ecu-ip>', 0),
        },
    )

    # 诊断会话控制
    p2, p2_star = app.default()
    print(f'default: P2={p2}, P2*={p2_star}')

    # 切换到 soc
    app.on('soc')

    # 安全访问
    seed = app.l1()
    print(f'L1 seed: {seed.hex()}')

    app.l1_ex(seed)
    print('L1 unlock done')


if __name__ == '__main__':
    main()