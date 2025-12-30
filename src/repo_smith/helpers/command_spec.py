from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Literal, Mapping, Self

ArgStyle = Literal["flag", "space", "equals"]


@dataclass(frozen=True)
class Opt:
    flag: str
    takes_value: bool = True
    transform: Callable[[Any], str] = str
    default: Any = None
    style: ArgStyle = "space"


def build_args(options: Mapping[str, Any], specs: Mapping[str, Opt]) -> List[str]:
    args = []
    for key, value in options.items():
        if value is None:
            continue

        spec = specs.get(key)
        if spec is None:
            raise ValueError(f"Unsupported option: {key}")
        if spec.takes_value:
            rendered = spec.transform(value)

            if spec.style == "equals":
                args.append(f"{spec.flag}={rendered}")
            else:
                args.append(spec.flag)
                args.append(spec.transform(value))
        elif value:
            args.append(spec.flag)
        elif spec.style == "equals":
            args.append(f"{spec.flag}={spec.transform(value)}")
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
        self._specs[name] = Opt(flag, True, transform, default, style="space")
        if default is not None:
            self._defaults[name] = default
        return self

    def bool_opt(
        self,
        name: str,
        flag: str,
        *,
        default: Any = None,
        transform: Callable[[Any], str] = str,
    ) -> Self:
        self._specs[name] = Opt(flag, True, transform, default, style="equals")
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
        self._specs[name] = Opt(flag, False, str, default, style="flag")
        if default is not None:
            self._defaults[name] = default
        return self

    def build(self, options: Mapping[str, Any]) -> List[str]:
        merged = dict(self._defaults)
        merged.update(options)
        print(merged)
        return build_args(merged, self._specs)
