#!/usr/bin/env python3
"""Valida el perfil sin enviarlo a ningún servicio externo."""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DAYS = {
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
}
LEVELS = {"beginner", "intermediate", "advanced"}
UNITS = {"metric", "imperial"}
PLACEHOLDERS = ("tu nombre", "describe ", "modelo del")


class ProfileError(ValueError):
    pass


def _require_table(data: dict, name: str) -> dict:
    value = data.get(name)
    if not isinstance(value, dict):
        raise ProfileError(f"Falta la sección [{name}]")
    return value


def _require(table: dict, key: str, kind: type):
    value = table.get(key)
    if not isinstance(value, kind) or (kind is str and not value.strip()):
        raise ProfileError(f"Falta o no es válido: {key}")
    return value


def _check_placeholders(data: object, path: str = "perfil") -> list[str]:
    found: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            found.extend(_check_placeholders(value, f"{path}.{key}"))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            found.extend(_check_placeholders(value, f"{path}[{index}]"))
    elif isinstance(data, str) and any(token in data.lower() for token in PLACEHOLDERS):
        found.append(path)
    return found


def validate(data: dict, strict: bool = False) -> list[str]:
    warnings: list[str] = []
    athlete = _require_table(data, "athlete")
    goals = _require_table(data, "goals")
    schedule = _require_table(data, "schedule")
    health = _require_table(data, "health")
    training = _require_table(data, "training")
    zones = _require_table(data, "heart_rate_zones")
    privacy = _require_table(data, "privacy")

    _require(athlete, "name", str)
    year = _require(athlete, "birth_year", int)
    if not 1900 <= year <= date.today().year:
        raise ProfileError("birth_year está fuera de rango")
    if date.today().year - year < 18:
        warnings.append("Perfil de menor de edad: requiere supervisión adulta y profesional.")
    timezone = _require(athlete, "timezone", str)
    try:
        ZoneInfo(timezone)
    except ZoneInfoNotFoundError as exc:
        raise ProfileError(f"Zona horaria desconocida: {timezone}") from exc
    if _require(athlete, "units", str) not in UNITS:
        raise ProfileError("units debe ser metric o imperial")
    if _require(athlete, "experience_level", str) not in LEVELS:
        raise ProfileError("experience_level debe ser beginner, intermediate o advanced")

    _require(goals, "primary", str)
    raw_date = _require(goals, "event_date", str)
    try:
        date.fromisoformat(raw_date)
    except ValueError as exc:
        raise ProfileError("event_date debe usar AAAA-MM-DD") from exc
    _require(goals, "success_definition", str)

    days = _require(schedule, "available_days", list)
    if not days or any(day not in DAYS for day in days):
        raise ProfileError("available_days contiene días inválidos o está vacío")
    preferred = _require(schedule, "preferred_time", str)
    if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", preferred):
        raise ProfileError("preferred_time debe usar HH:MM en formato 24 horas")
    maximum = _require(schedule, "max_session_minutes", int)
    if not 10 <= maximum <= 600:
        raise ProfileError("max_session_minutes debe estar entre 10 y 600")
    if schedule.get("long_session_day") not in days:
        raise ProfileError("long_session_day debe estar incluido en available_days")

    if not isinstance(health.get("medical_clearance"), bool):
        raise ProfileError("medical_clearance debe ser true o false")
    if health.get("red_flags_today") is True:
        warnings.append("Hay síntomas de alarma declarados: no generar entrenamiento.")
    if health.get("active_injuries"):
        warnings.append("Hay lesiones activas: confirmar límites con un profesional.")

    sports = _require(training, "sports", list)
    if not sports or not all(isinstance(item, str) and item.strip() for item in sports):
        raise ProfileError("training.sports debe incluir al menos un deporte")

    previous_high = 0
    for number in range(1, 6):
        key = f"z{number}"
        pair = zones.get(key)
        if not isinstance(pair, list) or len(pair) != 2 or not all(isinstance(x, int) for x in pair):
            raise ProfileError(f"{key} debe ser una lista de dos pulsaciones enteras")
        low, high = pair
        if not 30 <= low < high <= 250:
            raise ProfileError(f"{key} tiene límites fisiológicamente improbables")
        if low < previous_high:
            raise ProfileError(f"{key} se solapa con la zona anterior")
        previous_high = high

    if privacy.get("share_raw_health_data") is True:
        warnings.append("share_raw_health_data=true: revisa el riesgo antes de compartir exportaciones.")

    if strict:
        placeholders = _check_placeholders(data)
        if placeholders:
            raise ProfileError("Quedan campos de ejemplo: " + ", ".join(placeholders))
    return warnings


def load_and_validate(path: Path, strict: bool = False) -> list[str]:
    if not path.is_file():
        raise ProfileError(f"No existe el perfil: {path}")
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    return validate(data, strict=strict)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    parser.add_argument("--strict", action="store_true", help="rechaza textos de ejemplo")
    args = parser.parse_args()
    try:
        warnings = load_and_validate(args.profile, strict=args.strict)
    except (ProfileError, tomllib.TOMLDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"OK: perfil válido ({args.profile})")
    for warning in warnings:
        print(f"AVISO: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
