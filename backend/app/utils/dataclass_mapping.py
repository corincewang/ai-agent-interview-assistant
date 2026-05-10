from dataclasses import fields, is_dataclass
from enum import Enum
from types import UnionType
from typing import Any, get_args, get_origin
from uuid import UUID, uuid4


def coerce_dataclass(model_type: type, value: Any) -> Any:
    if value is None:
        return None

    if isinstance(value, model_type):
        return value

    if is_dataclass(model_type) and isinstance(value, dict):
        return model_type(
            **{
                field.name: _coerce_value(field.type, value.get(field.name))
                for field in fields(model_type)
            }
        )

    return value


def _coerce_value(expected_type: Any, value: Any) -> Any:
    if value is None:
        return None

    origin = get_origin(expected_type)
    args = get_args(expected_type)

    if origin is list:
        item_type = args[0] if args else Any
        return [_coerce_value(item_type, item) for item in value]

    if origin is dict:
        return value

    if origin is UnionType or origin is None and isinstance(expected_type, UnionType):
        return _coerce_union(args or get_args(expected_type), value)

    if expected_type is UUID:
        if isinstance(value, UUID):
            return value
        try:
            return UUID(str(value))
        except ValueError:
            return uuid4()

    if isinstance(expected_type, type) and issubclass(expected_type, Enum):
        return value if isinstance(value, expected_type) else expected_type(value)

    if isinstance(expected_type, type) and is_dataclass(expected_type):
        return coerce_dataclass(expected_type, value)

    return value


def _coerce_union(types: tuple[Any, ...], value: Any) -> Any:
    non_none_types = [candidate for candidate in types if candidate is not type(None)]

    for candidate in non_none_types:
        try:
            return _coerce_value(candidate, value)
        except Exception:
            continue

    return value
