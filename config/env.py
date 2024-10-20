from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ENV:
    NAME = 'Crypto exchange'
