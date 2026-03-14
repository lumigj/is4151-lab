def convertMicrobitValue(data):
	if data is None or len(data) == 0:
		return None

	return data[0]


def marshalStringForBleUartSending(strData):
	
	strPreparedData = strData + '\r\n'
	strPreparedData = strPreparedData.encode('utf-8')
	
	return strPreparedData


def decodeBleUartPayload(data):
	if data is None:
		return ''

	try:
		return data.decode('utf-8').rstrip('\r\n')
	except UnicodeDecodeError:
		return data.hex()


def normalizeBleAddress(address):
	if address is None:
		return ''

	return address.upper()
