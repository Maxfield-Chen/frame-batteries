from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

from domain.repositories.abstract import GenericFrameRepo


class BleakFrameRepo(GenericFrameRepo):
    frame_service_uuid = "7A230001-5475-A6A4-654C-8431F6AD49C4"
    frame_rx_uuid = "7A230002-5475-A6A4-654C-8431F6AD49C4"
    frame_tx_uuid = "7A230003-5475-A6A4-654C-8431F6AD49C4"
    frame_name = "Frame"
    client: BleakClient

    async def _discover_frames(self) -> list:
        """
        Asynchronously discovers Frame devices in the vicinity.

        This method scans for Bluetooth devices in the vicinity for a duration of 3 seconds.
        It then filters out the devices whose local name matches the frame_name attribute of the class.
        The addresses of these Frame devices are returned in a list.

        Returns:
            list: A list of addresses of the discovered Frame devices.
        """
        devices = await BleakScanner.discover(3, return_adv=True)
        frame_addrs = []
        for addr, device in devices.items():
            (_, adv_data) = device
            print(f"ADV DATA: {adv_data.local_name}")
            if adv_data.local_name == self.frame_name:
                frame_addrs.append(addr)
        return frame_addrs

    async def _transmit_bytes(
        *, client: BleakClient, tx: BleakGATTCharacteristic, data: bytes, show_me=False
    ):
        """
        Asynchronously transmits bytes on Frame's TX line     .

        This method writes the provided data to the given GATT characteristic of the client.
        If the length of the data exceeds the maximum transmission unit (MTU) size of the client,
        an exception is raised.

        Args:
            client (BleakClient): The client to which the data is to be transmitted.
            tx (BleakGATTCharacteristic): The GATT characteristic to which the data is to be written.
            data (bytes): The data to be transmitted.
            show_me (bool, optional): If True, the data is printed before transmission. Defaults to False.

        Raises:
            Exception: If the length of the data exceeds the client's MTU size minus 3.
        """
        if show_me:
            print(data)

        if len(data) > client.mtu_size - 3:
            raise Exception("payload length is too large")

        await client.write_gatt_char(tx, data)

    @property
    async def connection_state(self) -> None: ...

    async def connect(self, retries: int = 50):
        """
        Asynchronously connects to a Frame device, saving a client object. Must be called before other methods.

        This method attempts to discover Frame devices and connect to the first one found.
        If no Frame devices are found, it retries the process for a specified number of times.
        Once connected, it validates the Frame service and TX characteristic is present.
        If the Frame service or TX characteristic is not found, an exception is raised.

        Args:
            retries (int, optional): The number of times to retry the connection process if no Frame devices are found. Defaults to 50.

        Raises:
            Exception: If the service specified by frame_service_uuid is not found.
            Exception: If the TX characteristic specified by frame_tx_uuid is not found.
            Exception: If no Frame device is found after the specified number of retries.
        """
        frames = []
        while retries > 0:
            frames = await self._discover_frames()
            if frames:
                frame_addr = frames[0]
                async with BleakClient(frame_addr) as client:
                    print(f"Connected {client.is_connected}")
                    if client.is_connected:
                        service = client.services.get_service(self.frame_service_uuid)
                        if not service:
                            raise Exception(
                                f"Service '{self.frame_service_uuid} not found"
                            )
                        tx = service.get_characteristic(self.frame_tx_uuid)
                        if not tx:
                            raise Exception(
                                f"TX characteristic '{self.frame_tx_uuid}' not found"
                            )
                        self.client = client
            else:
                print("Frames not found, trying again...")
                retries += 1
        raise Exception(f"Frame not found after {retries} retries.")

    async def disconnect(self) -> None: ...

    async def upload_file(self, file_path: str) -> None: ...

    # async def upload_firmware(self, firmware_path: str) -> None: ...

    async def send_str(self, data: str) -> None: ...

    async def send_bytes(self, data: bytes) -> None: ...

    async def receive_str(self) -> str: ...

    async def receive_bytes(self) -> bytes: ...

    async def halt_execution(self) -> None: ...

    async def send_reset(self) -> None: ...
