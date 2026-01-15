from fastapi import FastAPI, HTTPException
from datetime import datetime, date, time
from typing import Dict, Any
from zoneinfo import ZoneInfo
import calendar

app = FastAPI(title="Server Time API", version="1.0.0")

TIMEZONE_ALIASES = {
    "москва": "Europe/Moscow",
    "санкт-петербург": "Europe/Moscow",
    "питер": "Europe/Moscow",
    "екатеринбург": "Asia/Yekaterinburg",
    "екаьеринбург": "Asia/Yekaterinburg",
    "новосибирск": "Asia/Novosibirsk",
    "омск": "Asia/Omsk",
    "красноярск": "Asia/Krasnoyarsk",
    "иркутск": "Asia/Irkutsk",
    "якутск": "Asia/Yakutsk",
    "владивосток": "Asia/Vladivostok",
    "хабаровск": "Asia/Vladivostok",
    "камчатка": "Asia/Kamchatka",
    "самара": "Europe/Samara",
    "калининград": "Europe/Kaliningrad",
    "саратов": "Europe/Saratov",
    "волгоград": "Europe/Volgograd",
}


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


@app.get("/time/convert")
async def convert_time(time_str: str, target_city: str) -> Dict[str, str]:
    """Конвертирует время (HH:MM) из UTC в выбранный часовой пояс"""
    normalized_city = target_city.strip().lower()
    timezone_name = TIMEZONE_ALIASES.get(normalized_city)
    if not timezone_name:
        available = ", ".join(sorted(set(TIMEZONE_ALIASES.keys())))
        raise HTTPException(
            status_code=400,
            detail=f"Неизвестный город. Доступные значения: {available}"
        )

    try:
        parsed_time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Неверный формат времени. Используйте HH:MM, например 15:00"
        ) from exc

    utc_now = datetime.now(ZoneInfo("UTC"))
    source_dt = datetime.combine(utc_now.date(), parsed_time, tzinfo=ZoneInfo("UTC"))
    target_dt = source_dt.astimezone(ZoneInfo(timezone_name))

    return {
        "input_time": parsed_time.strftime("%H:%M"),
        "assumed_source_timezone": "UTC",
        "target_city": target_city,
        "target_timezone": timezone_name,
        "converted_time": target_dt.strftime("%H:%M")
    }


@app.get("/date")
async def get_server_date() -> Dict[str, str]:
    """Возвращает текущую дату сервера"""
    current_date = date.today()
    return {
        "date": current_date.isoformat(),
        "year": str(current_date.year),
        "month": str(current_date.month),
        "day": str(current_date.day)
    }


@app.get("/date/formatted")
async def get_formatted_date() -> Dict[str, str]:
    """Возвращает текущую дату сервера в различных форматах"""
    current_date = date.today()
    return {
        "iso": current_date.isoformat(),
        "dd_mm_yyyy": current_date.strftime("%d.%m.%Y"),
        "yyyy_mm_dd": current_date.strftime("%Y-%m-%d"),
        "dd_mm_yy": current_date.strftime("%d.%m.%y"),
        "full": current_date.strftime("%d %B %Y"),
        "short": current_date.strftime("%d %b %Y")
    }


@app.get("/date/info")
async def get_date_info() -> Dict[str, Any]:
    """Возвращает подробную информацию о текущей дате"""
    current_date = date.today()
    weekday_names = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    weekday_names_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    return {
        "date": current_date.isoformat(),
        "year": current_date.year,
        "month": current_date.month,
        "day": current_date.day,
        "weekday": current_date.weekday(),
        "weekday_name_ru": weekday_names[current_date.weekday()],
        "weekday_name_en": weekday_names_en[current_date.weekday()],
        "isoweekday": current_date.isoweekday(),
        "day_of_year": current_date.timetuple().tm_yday,
        "days_in_month": calendar.monthrange(current_date.year, current_date.month)[1]
    }
