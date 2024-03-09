from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ENV:
    platform_name = 'Crypto exchange'
