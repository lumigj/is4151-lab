from bleak import BleakClient

import util


MICROBIT_TEMPERATURE_CHAR_UUID = 'e95d9250-251d-470a-a062-fa1922dfa9a8'
MICROBIT_UART_RX_CHAR_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
MICROBIT_UART_TX_CHAR_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'


class BleUartDevice:

	def __init__(self, address):
		self.address = address
		self.client = BleakClient(self.address)
		self._uart_callback = None
		self._temperature_callback = None
		self._uart_write_uuid = MICROBIT_UART_RX_CHAR_UUID
		self._uart_notify_uuid = MICROBIT_UART_TX_CHAR_UUID

	def _resolve_uart_characteristics(self):
		# Use characteristic properties rather than fixed UUID direction, since
		# some BlueZ/micro:bit combinations expose notify/write on swapped UUIDs.
		services = self.client.services
		if services is None:
			return

		write_candidate = None
		notify_candidate = None

		for service in services:
			for char in service.characteristics:
				uuid = char.uuid.lower()
				if uuid not in (MICROBIT_UART_RX_CHAR_UUID, MICROBIT_UART_TX_CHAR_UUID):
					continue

				props = set(char.properties)
				if notify_candidate is None and ('notify' in props or 'indicate' in props):
					notify_candidate = char.uuid
				if write_candidate is None and ('write' in props or 'write-without-response' in props):
					write_candidate = char.uuid

		if write_candidate is not None:
			self._uart_write_uuid = write_candidate
		if notify_candidate is not None:
			self._uart_notify_uuid = notify_candidate

	async def connect(self):
		await self.client.connect()
		if hasattr(self.client, 'get_services'):
			await self.client.get_services()
		self._resolve_uart_characteristics()

	async def readTemperature(self):
		temp = await self.client.read_gatt_char(MICROBIT_TEMPERATURE_CHAR_UUID)
		return util.convertMicrobitValue(temp)

	async def enable_temperature_receive(self, callback):
		self._temperature_callback = callback

		def _on_temperature_notify(_sender, data):
			self._temperature_callback(util.convertMicrobitValue(data))

		await self.client.start_notify(MICROBIT_TEMPERATURE_CHAR_UUID, _on_temperature_notify)

	async def disable_temperature_receive(self):
		if self.client.is_connected:
			await self.client.stop_notify(MICROBIT_TEMPERATURE_CHAR_UUID)

	async def send(self, strData):
		txData = util.marshalStringForBleUartSending(strData)
		try:
			await self.client.write_gatt_char(self._uart_write_uuid, txData, response=True)
		except Exception:
			# Fallback for peripherals that only support write-without-response.
			await self.client.write_gatt_char(self._uart_write_uuid, txData, response=False)

	async def enable_uart_receive(self, callback):
		self._uart_callback = callback

		def _on_uart_notify(_sender, data):
			self._uart_callback(util.decodeBleUartPayload(data))

		try:
			await self.client.start_notify(self._uart_notify_uuid, _on_uart_notify)
		except Exception as ex:
			if 'NotSupported' not in str(ex):
				raise

			fallback_notify = (
				MICROBIT_UART_RX_CHAR_UUID
				if self._uart_notify_uuid.lower() == MICROBIT_UART_TX_CHAR_UUID
				else MICROBIT_UART_TX_CHAR_UUID
			)
			await self.client.start_notify(fallback_notify, _on_uart_notify)
			self._uart_notify_uuid = fallback_notify

	async def disable_uart_receive(self):
		if self.client.is_connected:
			await self.client.stop_notify(self._uart_notify_uuid)

	async def disconnect(self):
		if self.client.is_connected:
			await self.client.disconnect()
