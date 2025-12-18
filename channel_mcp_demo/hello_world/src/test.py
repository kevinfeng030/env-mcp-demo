import asyncio
from datetime import datetime, timedelta

async def _background_task() -> None:
    """
    Background async task triggered by hello_world_sse.

    轮询 3 分钟，每次间隔 5 秒发送一条带时间（年月日时分秒）的消息。
    """
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    end_time = datetime.now() + timedelta(minutes=3)
    while datetime.now() < end_time:
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"start time:{start_time},hello env-channel at {current_time_str}")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(_background_task())