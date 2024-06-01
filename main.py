from bleak import BleakClient, BleakScanner


# TODO: move ble code into separate client module
frame_service_uuid = "7A230001-5475-A6A4-654C-8431F6AD49C4"
frame_rx_uuid = "7A230002-5475-A6A4-654C-8431F6AD49C4"
frame_tx_uuid = "7A230003-5475-A6A4-654C-8431F6AD49C4"
frame_name = "Frame"


async def discover_frame() -> list:
    devices = await BleakScanner.discover(3, return_adv=True)
    frame_addrs = []
    for addr, device in devices.items():
        (_, adv_data) = device
        print(f"ADV DATA: {adv_data.local_name}")
        if adv_data.local_name == frame_name:
            frame_addrs.append(addr)
    return frame_addrs


async def _transmit(client, tx, data, show_me=False):
    if show_me:
        print(data)  # TODO make this print nicer

    if len(data) > client.mtu_size - 3:
        raise Exception("payload length is too large")

    await client.write_gatt_char(tx, data)


async def connect_frame(retries: int = 50):
    frames = []
    while retries > 0:
        frames = await discover_frame()
        if frames:
            frame_addr = frames[0]
            async with BleakClient(frame_addr) as client:
                print(f"Connected {client.is_connected}")
                if client.is_connected:
                    service = client.services.get_service(frame_service_uuid)
                    tx = service.get_characteristic(frame_tx_uuid)
                    if not service:
                        raise Exception(f"Service '{frame_service_uuid} not found")
                    if not tx:
                        raise Exception(
                            f"TX characteristic '{frame_tx_uuid}' not found"
                        )
                    await _transmit(client, tx, "print('i love u')".encode())
                    await client.disconnect()
        else:
            print("Frames not found, trying again...")
            retries += 1


# asyncio.run(connect_frame())
