from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Mapping, Self


@dataclass(frozen=True)
class Opt:
    flag: str
    takes_value: bool = True
    transform: Callable[[Any], str] = str
    default: Any = None


def build_args(options: Mapping[str, Any], specs: Mapping[str, Opt]) -> List[str]:
    args = []
    for key, value in options.items():
        if value is None:
            continue

        spec = specs.get(key)
        if spec is None:
            raise ValueError(f"Unsupported option: {key}")

        if spec.takes_value:
            args.append(spec.flag)
            args.append(spec.transform(value))
        elif value:
            args.append(spec.flag)
    return args


class CommandSpec:
    def __init__(self) -> None:
        self._specs: Dict[str, Opt] = {}
        self._defaults: Dict[str, Any] = {}

    def opt(
        self,
        name: str,
        flag: str,
        *,
        default: Any = None,
        transform: Callable[[Any], str] = str,
    ) -> Self:
        self._specs[name] = Opt(flag, True, transform, default)
        if default is not None:
            self._defaults[name] = default
        return self

    def flag(
        self,
        name: str,
        flag: str,
        *,
        default: Any = None,
    ) -> Self:
        self._specs[name] = Opt(flag, False, str, default)
        if default is not None:
            self._defaults[name] = default
        return self

    def build(self, options: Mapping[str, Any]) -> List[str]:
        merged = dict(self._defaults)
        merged.update(options)
        return build_args(merged, self._specs)
