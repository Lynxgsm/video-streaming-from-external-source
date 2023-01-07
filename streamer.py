import socket, cv2, pickle, struct
import imutils
import cv2

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '192.168.1.112'  # Enter the IP address for the device where the stream is coming from
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at", socket_address)


def start_video_stream():
    client_socket, addr = server_socket.accept()
    camera = True
    if camera == True:
        vid = cv2.VideoCapture('videos/..') # Let's you stream video directly
    else:
        vid = cv2.VideoCapture(0) # Let's you stream your first camera. By default it's your webcam
    try:
        print('CLIENT {} CONNECTED!'.format(addr))
        if client_socket:
            while vid.isOpened():
                img, frame = vid.read()

                frame = imutils.resize(frame, width=620)
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
                if img:
                    cv2.imshow("TRANSMITTING TO SERVER", frame)
                else:
                    print('no video')
                    vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue

                if cv2.waitKey(1) == ord('q'):
                    client_socket.close()
                    break

    except Exception as e:
        print(f"SERVER {addr} DISCONNECTED")
        pass


while True:
    start_video_stream()
