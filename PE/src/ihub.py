# python3 -m serial.tools.list_ports



import time
import random

import serial
import RPi.GPIO as GPIO

import sqlite3
import requests
import json

import paho.mqtt.client as mqtt

import _thread as thread



def sendCommand(command):
        
    command = command + '\n'
    ser.write(str.encode(command))



def waitResponse():
    
    response = ser.readline()
    response = response.decode('utf-8').strip()
    
    return response



def saveData(lights):
    
    conn = sqlite3.connect('light.db')
    c = conn.cursor()
    
    for light in lights:
        
        data = light.split('=')
        realData = data[1].split('|')
        temp = bme280.temperature

        sql = "INSERT INTO light (devicename, crowd_density, abright, atemp, timestamp) VALUES("+data[0]+","+ realData[0]+","+realData[1]+"," + temp +", datetime('now', 'localtime'))"
        c.execute(sql)
    
    conn.commit()
    conn.close()
    
    lights.clear()



def rhub():
        
    global ser
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    print('rhub: Listening on /dev/ttyACM0... Press CTRL+C to exit')
    
    # Handshaking
    sendCommand('handshake')
    
    strMicrobitDevices = ''
    
    while strMicrobitDevices == None or len(strMicrobitDevices) <= 0:
        
        strMicrobitDevices = waitResponse()        
        
        print('rhub handshake: ' + strMicrobitDevices)
        
        time.sleep(0.1)
    
    strMicrobitDevices = strMicrobitDevices.split('=')
    
    if len(strMicrobitDevices[1]) > 0:

        listMicrobitDevices = strMicrobitDevices[1].split(',')
        
        if len(listMicrobitDevices) > 0:
                
            for mb in listMicrobitDevices:
            
                print('rhub: Connected to micro:bit device {}...'.format(mb))
            
            while True:
                
                time.sleep(1)                    
                
                commandToTx = 'sensor=light'                
                sendCommand('cmd:' + commandToTx)                    
                
                if commandToTx.startswith('sensor='):
                    
                    strSensorValues = ''

                    while strSensorValues == None or len(strSensorValues) <= 0:
                        
                        strSensorValues = waitResponse()
                        time.sleep(0.1)

                    listSensorValues = strSensorValues.split(',')

                    for sensorValue in listSensorValues:
                        
                        print('rhub: {}'.format(sensorValue))
                    
                    saveData(listSensorValues)



def cloudrelay():        
    
    base_uri = 'http://169.254.53.99:5000/'
    globallight_uri = base_uri + 'api/globallight'
    headers = {'content-type': 'application/json'}
    
    
    
    while True:
    
        time.sleep(10)
        
        print('Relaying data to cloud server...')
                
        conn = sqlite3.connect('light.db')
        c = conn.cursor()
        c.execute('SELECT id, devicename, light, timestamp FROM light WHERE tocloud = 0')
        results = c.fetchall()
        c = conn.cursor()
                
        for result in results:
                    
            print('Relaying id={}; devicename={}; light={}; timestamp={}'.format(result[0], result[1], result[2], result[3]))
            
            glight = {
                'devicename':result[1],
                'light':result[2],
                'timestamp':result[3]
            }
            req = requests.put(globallight_uri, headers = headers, data = json.dumps(glight))
            
            c.execute('UPDATE light SET tocloud = 1 WHERE id = ' + str(result[0]))
        
        conn.commit()
        conn.close()



def on_connect(client, userdata, flags, rc):
	
	if rc == 0:
	
		print('Connected to MQTT Broker!')
		
	else:
	
		print('Failed to connect, return code {:d}'.format(rc))



def on_message(client, userdata, msg):
    
    smartlight = str(msg.payload.decode())
    print('Smartlight command subscribed: ' + smartlight)
    
    if smartlight == 'normal':
        
        GPIO.output(greenLedPin, True)
        GPIO.output(redLedPin, False)

    if smartlight == 'harsh':
        GPIO.output(greenLedPin, False)
        GPIO.output(redLedPin, True)



def smartlight():        
    
    broker = 'broker.emqx.io'
    port = 1883
    topic = "/is4151-is5451/73/smartlight"
    client_id = f'python-mqtt-{random.randint(0, 10000)}'
    username = 'emqx'
    password = 'public'

    print('MQTT client_id={}'.format(client_id))
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)

    client.subscribe(topic)    
    client.on_message = on_message
    
    client.loop_forever()



def init():    

    GPIO.setmode(GPIO.BCM)
    
    global redLedPin
    redLedPin = 11
    GPIO.setup(redLedPin, GPIO.OUT)
    GPIO.output(redLedPin, False)

    global greenLedPin
    greenLedPin = 13
    GPIO.setup(greenLedPin, GPIO.OUT)
    GPIO.output(greenLedPin, True) #TODO

    import board
    from adafruit_bme280 import basic as adafruit_bme280
    i2c=board.I2C()
    global bme280
    bme280=adafruit_bme280.Adafruit_BME280_I2C(i2c)


def main():
    
    init()
    
    thread.start_new_thread(rhub, ())
    # thread.start_new_thread(cloudrelay, ())
    thread.start_new_thread(smartlight, ())
    
    print('Program running... Press CTRL+C to exit')
    
    while True:

        try:                       
                        
            time.sleep(0.1)        
            
        except KeyboardInterrupt:                  
        
            if ser.is_open:
            
                ser.close()                           
        
            GPIO.cleanup()
            
            print('Program terminating...')
            
            break
        
        except Exception as error:
            
            print('Error: {}'.format(error.args[0]))
    
    print('Program exited...')



if __name__ == '__main__':
    
    main()
