import base64
import cv2
import zmq
from time import sleep
context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://localhost:5001')

camera = cv2.VideoCapture(0)  # init the camera

while True:
    try:
        grabbed, frame = camera.read()  # grab the current frame
        frame = cv2.resize(frame, (640, 480))  # resize the frame
        # print(frame)
        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        footage_socket.send(jpg_as_text)

    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break


# python3 client.py