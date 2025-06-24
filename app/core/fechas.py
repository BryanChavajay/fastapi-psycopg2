from datetime import date, datetime
from zoneinfo import ZoneInfo


def obtener_fecha_actual() -> date:
    zona = ZoneInfo("America/Guatemala")
    return datetime.now(zona).date()


def obtener_fecha_hora_actual() -> datetime:
    zona = ZoneInfo("America/Guatemala")
    return datetime.now(zona)
