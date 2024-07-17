import pytest
from domain.repositories.frame import BleakFrameRepo


class TestSmokeConnection:

    @pytest.mark.asyncio
    async def test_connection(self):
        bleak_repo = BleakFrameRepo()
        try:
            await bleak_repo.connect()
            assert bleak_repo._client, "Unable to set client"
            assert bleak_repo._client.is_connected, "Client is not connected"
            assert bleak_repo._service, "Service not found"
            assert bleak_repo._tx_char, "TX Characteristic not found"
            assert bleak_repo._rx_char, "RX Characteristic not found"
        finally:
            await bleak_repo.disconnect()
