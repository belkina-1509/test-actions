from fastapi import FastAPI
from datetime import datetime
from typing import Dict

app = FastAPI(title="Server Time API", version="1.0.0")


@app.get("/")
async def root() -> Dict[str, str]:
    """Корневой эндпоинт с приветствием"""
    return {"message": "Server Time API", "status": "running"}


@app.get("/time")
async def get_server_time() -> Dict[str, str]:
    """Возвращает текущее время сервера"""
    current_time = datetime.now()
    return {
        "server_time": current_time.isoformat(),
        "timestamp": str(current_time.timestamp()),
        "timezone": str(current_time.astimezone().tzinfo)
    }


@app.get("/time/formatted")
async def get_formatted_time() -> Dict[str, str]:
    """Возвращает текущее время сервера в отформатированном виде"""
    current_time = datetime.now()
    return {
        "date": current_time.strftime("%Y-%m-%d"),
        "time": current_time.strftime("%H:%M:%S"),
        "datetime": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "iso_format": current_time.isoformat()
    }
