import os
import socketio
from aiohttp import web
from evdev import InputDevice, ecodes
from time import sleep

sio = socketio.AsyncServer(cors_allowed_origins="ws://piterminator.local:8080")
app = web.Application()
sio.attach(app)

# Device's Bluetooth UUID
devID = "7B:D2:C0:E6:78:57"


async def helper():

	KEY_PRESSED = 1

	# Path for bluetooth remote on this app's server.
	devPath = "/dev/input/event2"

	# If remote is not connected...
	while not os.path.exists(devPath):
		# Wait until it returns...
		sleep(5)
	device = InputDevice(devPath)
	
	while True:

		try:
			async for event in device.async_read_loop():

				if event.type != ecodes.EV_KEY:
					continue
				if event.value != KEY_PRESSED:
					continue

				try:
					match event.code:
						case ecodes.KEY_PLAYPAUSE:
							await sio.emit("keypress", ecodes.KEY[ecodes.KEY_PLAYPAUSE])
						case ecodes.KEY_VOLUMEDOWN:
							await sio.emit("keypress", ecodes.KEY[ecodes.KEY_VOLUMEDOWN])
						case ecodes.KEY_VOLUMEUP:
							await sio.emit("keypress", ecodes.KEY[ecodes.KEY_VOLUMEUP])
						case ecodes.KEY_PREVIOUSSONG:
							await sio.emit("keypress", ecodes.KEY[ecodes.KEY_PREVIOUSSONG])
						case ecodes.KEY_NEXTSONG:
							await sio.emit("keypress", ecodes.KEY[ecodes.KEY_NEXTSONG])
						case _:
							pass
				except:
					continue
		except:
			# If bluetooth device is no longer present - wait until it returns...
			while not os.path.exists(devPath):
				sleep(5)
			device = InputDevice(devPath)
				

async def init_app():
    sio.start_background_task(helper)
    return app

        
if __name__ == "__main__":
	web.run_app(init_app())
