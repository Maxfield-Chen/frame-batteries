from enum import Enum, auto


class ConnectionState(Enum):
    CONNECTED = auto()
    DFU_CONNECTED = auto()
    DISCONNECTED = auto()
