from domain.repositories.frame import BleakFrameRepo
import asyncio


class TestSmokeConnection:

    def test_connection(self):
        bleak_repo = BleakFrameRepo()
        asyncio.run(bleak_repo.connect())
