from enum import Enum


class EnumBase(Enum):

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Severity(EnumBase):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
