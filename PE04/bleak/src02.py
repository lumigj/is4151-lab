# demo temperature service

import asyncio
import traceback
from bleak import BleakScanner

import util
from bleuartlib import BleUartDevice


async def main():

	bleUartDevice1 = None
	found_address = None

	print('********** Initiating device discovery......')

	devices = await BleakScanner.discover(timeout=2.0)

	for device in devices:

		address = util.normalizeBleAddress(device.address)

		if address == 'F1:B1:2E:B3:CC:5B':

			print('Found BBC micro:bit [vivaz]: {}'.format(address))
			found_address = address
			break

	if found_address is None:
		print('********** UNKNOWN ERROR')
		return

	try:

		bleUartDevice1 = BleUartDevice(found_address)
		await bleUartDevice1.connect()
		print('Connected to micro:bit device')

		while True:

			temp = await bleUartDevice1.readTemperature()
			print('Temperature = {}'.format(temp))
			await asyncio.sleep(1)

	except KeyboardInterrupt:

		print('********** END')

	except Exception as ex:

		print('********** UNKNOWN ERROR')
		print('Error detail: {}'.format(ex))
		traceback.print_exc()

	finally:

		if bleUartDevice1 is not None:
			try:
				await bleUartDevice1.disconnect()
				print('Disconnected from micro:bit device')
			except Exception as ex:
				print('Disconnect error: {}'.format(ex))


if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('********** END')
