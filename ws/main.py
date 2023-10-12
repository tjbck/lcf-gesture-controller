import socketio
import math

import serial
from serial.tools import list_ports

ports = list_ports.comports()
for p in ports:
    print(p.device)

# # TODO combine the two
# print(len(ports), 'ports found')
ser = serial.Serial('COM6',115200) 
# create a Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins=[], async_mode='asgi')


def get_angle(x1,y1,x2,y2):
    return str(int(math.degrees(math.atan2(y2-y1, x2-x1)) % 360))

@sio.event
async def connect(sid, environ):
    print('connect ', sid)


@sio.event
async def disconnect(sid):
    print('disconnect')



@sio.on('data-event')
async def data_event_handler(sid, data):
    print('data_event_handler', sid, data)
    if(data['type'] == 'touch'):
        angle = get_angle(data['data']['start']['x'], data['data']['start']['y'], data['data']['end']['x'], data['data']['end']['y'])
        ser.write(f'a{angle}'.encode())
        # ser.write(angle.encode())
        print(f'a{angle}')

    if(data['type'] == 'heat'):
        print(f"h{data['data']}")
        ser.write(f"h{data['data']}".encode())


    # data = Serial.readString();
    # data.charAt(0)
    # if 'a' -> angle
    # if 'h' -> heat
    # data++
    # atoi(data)
    


# wrap with ASGI application
app = socketio.ASGIApp(sio)
