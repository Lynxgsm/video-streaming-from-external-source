import socket
import cv2
import pickle
import struct
import imutils  # pip install imutils
import threading
import cv2


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at", socket_address)

global frame
frame = None


def start_video_stream():
    global frame
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '192.168.1.112'
    port = 9999
    client_socket.connect((host_ip, port))
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO FROM SOURCE", frame)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break
    client_socket.close()


thread = threading.Thread(target=start_video_stream, args=())
thread.start()


def serve_client(addr, client_socket):
    global frame
    try:
        print('CLIENT {} CONNECTED!'.format(addr))
        if client_socket:
            while True:
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a))+a
                client_socket.sendall(message)

    except Exception as e:
        print(f"CLINET {addr} DISCONNECTED")
        pass


while True:
    client_socket, addr = server_socket.accept()
    print(addr)
    thread = threading.Thread(target=serve_client, args=(addr, client_socket))
    thread.start()
    # edited here because one thread is already started before
    print("TOTAL CLIENTS ", threading.activeCount() - 2)
