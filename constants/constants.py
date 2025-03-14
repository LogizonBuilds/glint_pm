from enum import Enum


class EnumBase(Enum):

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Severity(EnumBase):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class ServiceType(EnumBase):
    TECH = "TECH"
    PROJECT_MANAGEMENT = "PROJECT_MANAGEMENT"


class TransactionStatus(EnumBase):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
