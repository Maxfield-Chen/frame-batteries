from typing import Any, Iterable, Protocol


class GenericDBRepo(Protocol):

    def add(self, models: Iterable | Any) -> None: ...

    def delete(self, models: Iterable | Any) -> None: ...

    def get(self, model_id: Iterable | Any) -> Iterable | Any: ...


class GenericFrameRepo(Protocol):

    @property
    def connection_state(self) -> None: ...

    def connect(self) -> None: ...

    def disconnect(self) -> None: ...

    def upload_file(self, file_path: str) -> None: ...

    # def upload_firmware(self, firmware_path: str) -> None: ...

    def send_str(self, data: str) -> None: ...

    def send_bytes(self, data: bytes) -> None: ...

    def receive_str(self) -> str: ...

    def receive_bytes(self) -> bytes: ...

    def halt_execution(self) -> None: ...

    def send_reset(self) -> None: ...
