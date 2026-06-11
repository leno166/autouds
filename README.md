# autouds

**autouds** 是一个基于 Python 的 UDS (Unified Diagnostic Services) 诊断工具，遵循 ISO 14229-1 标准，通过 [autodoip](https://github.com/leno166/autodoip) (ISO 13400) 传输层与汽车 ECU 进行诊断通信。

采用生成器驱动的装饰器模式，将 Python 方法映射为 UDS 服务调用，自动处理请求构造、响应解析和负响应异常。

## 特性

- 覆盖 ISO 14229-1 主要诊断服务：会话控制、安全访问、DTC 读写、数据标识符读写、例行程序控制、上传下载等
- 装饰器驱动：`@handler(service_name='session', sub_fn_name='default')` 将方法映射到 UDS 服务
- 生成器模式：`yield` 发送请求，接收 `Response` 后继续处理，流程直观
- 智能请求构造：支持中文/英文/短键名解析服务 ID 和子功能
- 自动处理延迟响应 (NRC 0x78) 的轮询等待
- 负响应自动转换为 `UdsError` 异常，附带 NRC 描述
- 基于 [autodoip](https://github.com/leno166/autodoip) 零依赖传输层

## 安装

```bash
pip install autouds
```

`autodoip` 和 `pydantic` 会作为依赖自动安装。要求 Python ≥ 3.14。

## 快速开始

```python
from autouds import App

# 创建诊断应用：监听指定 IP，预定义 ECU 列表
app = App(
    ip='192.168.10.1',
    ecus={
        'mcu': (0x1001, '192.168.10.10', 13400),
        'soc': (0x1002, '192.168.10.20', 13400),
    },
)

# 进入默认会话，获取 P2/P2* 定时参数
p2, p2_star = app.default()
print(f'P2={p2}ms, P2*={p2_star}ms')

# 安全访问 (Level 1)
seed = app.l1()
print(f'seed: {seed.hex()}')
# ... 计算密钥 ...
app.l1_ex(key)

# 读取数据标识符
data = app.read_did(0xFF00)
print(f'DID 0xFF00: {data.hex()}')

# 切换到另一个 ECU
app.on('soc')
app.read_dtc_count()
```

## 命令行

```bash
python -m autouds
```

运行内置的演示流程（需先修改 `__main__.py` 中的连接参数）。

## 支持的 UDS 服务

### 诊断会话控制 (0x10)

| 方法 | 子功能 | 说明 |
|---|---|---|
| `app.default()` | 0x01 | 默认会话，返回 `(P2, P2*)` |
| `app.program()` | 0x02 | 编程会话 |
| `app.extend()` | 0x03 | 扩展会话 |
| `app.safety()` | 0x04 | 安全系统会话 |

### ECU 复位 (0x11)

| 方法 | 子功能 | 说明 |
|---|---|---|
| `app.hard()` | 0x01 | 硬复位 |
| `app.key()` | 0x02 | 钥匙复位 |
| `app.soft()` | 0x03 | 软复位 |

### 安全访问 (0x27)

| 方法 | 子功能 | 说明 |
|---|---|---|
| `app.l1()` | 0x01 | 请求 L1 种子 |
| `app.l1_ex(key)` | 0x02 | 发送 L1 密钥 |
| `app.l5()` | 0x05 | 请求 L5 种子 |
| `app.l5_ex(key)` | 0x06 | 发送 L5 密钥 |
| `app.l19()` | 0x19 | 请求 L19 种子 |
| `app.l19_ex(key)` | 0x1A | 发送 L19 密钥 |

### 数据读写

| 方法 | 服务 | 说明 |
|---|---|---|
| `app.read_did(did)` | 0x22 | 按标识符读取数据 |
| `app.write_did(did, payload)` | 0x2E | 按标识符写入数据 |

### DTC 诊断故障码

| 方法 | 服务 | 说明 |
|---|---|---|
| `app.read_dtc_count()` | 0x19 | 按状态掩码读取 DTC 数量 |
| `app.read_dtc_by_mask()` | 0x19 | 按状态掩码读取 DTC 列表 |
| `app.clear_dtc()` | 0x14 | 清除诊断信息 |
| `app.dtc_on()` | 0x85 | 允许 DTC 更新 |
| `app.dtc_off()` | 0x85 | 禁止 DTC 更新 |

### 通信与握手

| 方法 | 服务 | 说明 |
|---|---|---|
| `app.present()` | 0x3E | 待机握手 (抑制肯定响应) |
| `app.comm_enable_rx_tx()` | 0x28 | 启用收发 |
| `app.comm_disable_rx_tx()` | 0x28 | 禁用收发 |

### 例行程序与 I/O

| 方法 | 服务 | 说明 |
|---|---|---|
| `app.routine_start()` | 0x31 | 启动例行程序 |
| `app.routine_stop()` | 0x31 | 停止例行程序 |
| `app.routine_result()` | 0x31 | 请求执行结果 |
| `app.io_control()` | 0x2F | I/O 控制 |

### 上传下载

| 方法 | 服务 | 说明 |
|---|---|---|
| `app.request_download()` | 0x34 | 请求下载 |
| `app.request_upload()` | 0x35 | 请求上传 |
| `app.transfer_data()` | 0x36 | 数据传输 |
| `app.exit_transfer()` | 0x37 | 退出传输 |

## API 概览

| 类/函数 | 说明 |
|---|---|
| `App(ip, ecus, port=13400, tester=0x0E80, doip_config=None)` | 诊断应用主类 |
| `App.on(name)` | 切换到指定 ECU |
| `handler(service_name=..., sub_fn_name=...)` | 装饰器，将生成器方法映射为 UDS 服务 |
| `Request` | UDS 请求模型，支持语义名或原始 ID 构造 |
| `Response` | UDS 响应模型，自动解析正/负响应 |
| `UdsError` | 负响应异常，包含 `resp.nrc` 和 `resp.nrc_desc` |
| `set_send_impl(func)` | 注入自定义发送实现 |

## 自定义服务

通过 `@handler` 装饰器和 `App` 子类可以扩展自定义 UDS 服务：

```python
from autouds import App, handler, Response
from typing import Generator

class MyApp(App):
    @handler(service_name='read_did')
    def read_vin(self) -> Generator[bytes, Response, bytes]:
        resp: Response = yield 0xF190.to_bytes(2, 'big')
        return resp.params
```

装饰器支持直接指定 service_id / sub_fn：

```python
@handler(s_id=0x22, sub_fn=0x01)
def custom_service(self) -> Generator[bytes, Response, bytes]:
    resp: Response = yield b'\x00\x01'
    return resp.params
```

## 依赖

- [autodoip](https://github.com/leno166/autodoip) — DoIP 传输层 (ISO 13400)
- [pydantic](https://github.com/pydantic/pydantic) — 数据验证

## 许可证

MIT License