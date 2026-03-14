# demo uart transmit and receive



import asyncio
import traceback
from bleak import BleakScanner

import util
from bleuartlib import BleUartDevice



async def addBleUartDevice(address, name):

	bleUartDevice = BleUartDevice(address)
	await bleUartDevice.connect()
	await bleUartDevice.enable_uart_receive(bleUartReceiveCallback)

	bleUartDevices.append({'device': bleUartDevice, 'name': name})



def bleUartReceiveCallback(data):

	print('Received data = {}'.format(data))



async def sendCommandToAllBleUartDevices(command):

	for bled in bleUartDevices:

		await bled['device'].send(command)



async def disconnectFromAllBleUartDevices():

	for bled in bleUartDevices:

		if bled['device'] is not None:
			await bled['device'].disable_uart_receive()
			await bled['device'].disconnect()
			bled['device'] = None



async def main():

	global bleUartDevices
	bleUartDevices = []

	print('********** Initiating device discovery......')

	devices = await BleakScanner.discover(timeout=2.0)

	for device in devices:

		address = util.normalizeBleAddress(device.address)

		if address == 'E9:01:B2:1A:C5:4E':

			print('Found BBC micro:bit [vavet]: {}'.format(address))
			await addBleUartDevice(address, 'vavet')

			print('Added micro:bit device...')

		elif address == 'C8:06:B1:B4:66:53':

			print('Found BBC micro:bit [tipov]: {}'.format(address))
			await addBleUartDevice(address, 'tipov')

			print('Added micro:bit device...')

		elif address == 'DF:60:7F:9B:61:F6':

			print('Found BBC micro:bit [popap]: {}'.format(address))
			await addBleUartDevice(address, 'popap')

			print('Added micro:bit device...')

		elif address == 'E4:C8:06:E7:73:CF':

			print('Found BBC micro:bit [vuzuv]: {}'.format(address))
			await addBleUartDevice(address, 'vuzuv')

			print('Added micro:bit device...')

	try:

		if len(bleUartDevices) > 0:

			while True:

				response = await asyncio.to_thread(input, 'Do you want to transmit command to micro:bit (Y/n) = ')

				if response == 'Y':

					command = await asyncio.to_thread(input, 'Enter command to send = ')
					await sendCommandToAllBleUartDevices(command)
					print('Finished sending command to all micro:bit devices...')

				await asyncio.sleep(0.1)

	except KeyboardInterrupt:

		print('********** END')

	except Exception as ex:

		print('********** UNKNOWN ERROR')
		print('Error detail: {}'.format(ex))
		traceback.print_exc()

	finally:

		await disconnectFromAllBleUartDevices()
		print('Disconnected from all micro:bit devices')



if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('********** END')
