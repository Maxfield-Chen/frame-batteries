from pathlib import Path


class LuaCode:
    """
    This class provides methods to read a Lua file from a host path, clean its contents,
    and generate chunks of the file for BLE transmission to Frame.

    Init Parameters:
        host_path (Path): The path to the Lua file on the host.
        contents (str): The contents of the Lua file.
        client_path (Path): The path to the Lua file on the client. Defaults to "app.lua".
        chunk_size (int): The size of the chunks to split the file into. Defaults to 170.

    External Properties:
        upload_codes (list[str]): A list of Lua code strings to upload the file to Frame.
    """

    host_path: Path
    contents: str
    client_path: Path
    chunk_size: int

    def __init__(
        self,
        host_path: Path,
        *,
        client_path: Path = Path("app.lua"),
        chunk_size: int = 170,
    ):
        self.host_path = host_path
        self.client_path = client_path
        self.chunk_size = chunk_size
        self.contents = host_path.read_text()

    def _clean_contents(self) -> str:
        cleaned = self.contents
        replacements = [
            ("\\", "\\\\"),
            ("\n", "\\n"),
            ("'", "\\'"),
            ('"', '\\"'),
        ]
        for target, escaped in replacements:
            cleaned = cleaned.replace(target, escaped)
        return cleaned

    def _generate_open_file(self) -> str:
        return f"f=frame.file.open('{str(self.client_path)}', 'w');print('\x02')"

    def _generate_chunk_idxs(self) -> list[tuple[int, int]]:
        idxs: list[tuple[int, int]] = []
        start = 0
        end = self.chunk_size
        while end <= len(self.contents):
            if self.contents[end - 1] == "\\":
                end -= 1
            idxs.append((start, end))
            start = end
            end += self.chunk_size
        if end > len(self.contents):
            idxs.append((start, len(self.contents)))
        return idxs

    @property
    def upload_codes(self):
        cleaned_contents = self._clean_contents()

        def generate_chunk(chunk: str) -> str:
            return f"file:write('{chunk}');print('\x02')"

        return [self._generate_open_file()] + [
            generate_chunk(cleaned_contents[s:e])
            for s, e in self._generate_chunk_idxs()
        ]
