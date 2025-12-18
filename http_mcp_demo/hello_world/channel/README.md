## env-channel 使用手册（简明版）

### 1. 安装

#### 1.1 从本地 wheel 安装（推荐）

```bash
cd env-channel
uv build                     # 构建 wheel 包
ls dist/                     # 查看生成的 .whl 文件

# 在其它项目中安装（示例）
cd /your/other/project
uv pip install /绝对路径/env-channel/dist/env_channel-0.1.0-py3-none-any.whl
```

#### 1.2 本地开发模式安装（联调用）

```bash
cd /your/other/project
uv pip install -e /绝对路径/env-channel
```

---

### 2. 核心概念

- **EnvChannelServer**：WebSocket 服务端，负责转发消息。
- **EnvChannelPublisher**：发布端，往某个 `topic` 推送消息。
- **@env_channel_sub**：订阅端装饰器，把函数标记为某个 `topic` 的订阅处理函数。

---

### 3. 启动 WebSocket Server（环境侧）

最简单示例（可放在独立脚本或你的服务启动逻辑里）：

```python
import asyncio
from env_channel.server import EnvChannelServer

async def main():
    server = EnvChannelServer(host="0.0.0.0", port=8765)
    await server.start()
    print("EnvChannelServer started at ws://0.0.0.0:8765")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await server.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

> 在实际项目中，可以参考 `env-channel-demo`，把 `EnvChannelServer` 放到 FastAPI 的 lifespan 里统一管理。

---

### 4. 发布消息（Publisher）

```python
import asyncio
from env_channel.client import EnvChannelPublisher

async def main():
    publisher = EnvChannelPublisher(
        server_url="ws://localhost:8765",
        auto_connect=True,
        auto_reconnect=True,
    )

    await publisher.publish(
        topic="demo-channel",
        message={"text": "hello env-channel"},
    )

if __name__ == "__main__":
    asyncio.run(main())
```

- **`topic`**：业务通道名，如 `"order-updates"`、`"task-progress"`。
- **`message`**：`dict`，放业务数据。

---

### 5. 订阅消息（Subscriber）

#### 5.1 直接使用 `EnvChannelSubscriber`

```python
import asyncio
import logging
from env_channel.client import EnvChannelSubscriber
from env_channel.common.message import EnvChannelMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    sub = EnvChannelSubscriber(
        server_url="ws://localhost:8765",
        auto_connect=True,
        auto_reconnect=True,
        reconnect_interval=10.0,
    )

    async def handle(msg: EnvChannelMessage):
        logger.info("received: %s", msg.message)

    await sub.subscribe(topics=["demo-channel"], handler=handle)
    logger.info("listening on demo-channel...")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await sub.unsubscribe(["demo-channel"])
        await sub.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

#### 5.2 使用装饰器 `@env_channel_sub`（零样板）

```python
import asyncio
import logging
from env_channel.client import env_channel_sub
from env_channel.common.message import EnvChannelMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@env_channel_sub(
    server_url="ws://localhost:8765",
    topics=["demo-channel"],
    auto_connect=True,
    auto_reconnect=True,
    reconnect_interval=10.0,
    # auto_start=True（默认）：导入模块后自动启动订阅线程
)
async def handle_demo(msg: EnvChannelMessage):
    logger.info("decorator received: %s", msg.message)

async def main():
    logger.info("Listening... (Ctrl+C to stop)")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping...")

if __name__ == "__main__":
    asyncio.run(main())
```

---

### 6. env-channel-demo 快速体验

项目内自带 `env-channel-demo`，集成了 FastAPI + EnvChannelServer + 发布 + 装饰器订阅。

1. 启动 demo：

```bash
cd env-channel/env-channel-demo/src/env_channel_demo
uv run main.py
```

2. 通过 HTTP 发布消息：

```bash
curl "http://127.0.0.1:8000/publish?text=hello-from-demo"
```

3. 在启动 demo 的控制台中可以看到订阅日志：

```text
Decorator subscriber 111 received: {'text': 'hello-from-demo'}
```

---

### 7. 总结

- **环境侧**：启动 `EnvChannelServer`，业务代码用 `EnvChannelPublisher.publish(topic, message)` 推消息。
- **Agent / 客户端侧**：用 `EnvChannelSubscriber` 或 `@env_channel_sub` 订阅对应 `topic`，在 handler 里处理 `EnvChannelMessage` 即可。



