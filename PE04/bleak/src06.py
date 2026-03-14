# demo uart transmit



import asyncio
import traceback
from bleak import BleakScanner

import util
from bleuartlib import BleUartDevice



async def main():

	bleUartDevice1 = None
	found_address = None
	target_addresses = {
		'E9:01:B2:1A:C5:4E': 'vavet',
		'E4:C8:06:E7:73:CF': 'vuzuv'
	}

	print('********** Initiating device discovery......')

	devices = await BleakScanner.discover(timeout=2.0)

	for device in devices:

		address = util.normalizeBleAddress(device.address)

		if address in target_addresses:

			print('Found BBC micro:bit [{}]: {}'.format(target_addresses[address], address))
			found_address = address
			break

	if found_address is None:
		print('********** UNKNOWN ERROR')
		return

	try:

		bleUartDevice1 = BleUartDevice(found_address)
		await bleUartDevice1.connect()
		print('Connected to micro:bit device')

		data1 = await asyncio.to_thread(input, 'Enter data to send = ')
		await bleUartDevice1.send(data1)
		print('Finished sending data...')

		data2 = await asyncio.to_thread(input, 'Enter data to send = ')
		await bleUartDevice1.send(data2)
		print('Finished sending data...')

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
