import socket
import os
import keyboard
import threading
from audio import start_recording, stop_recording

def receive_file(stop_event):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    port = 12345
    
    server_socket.bind((host, port))
    server_socket.listen(1)
    server_socket.settimeout(1)
    print(f"Server listening on {host}:{port}")

    while not stop_event.is_set():
        try:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address}")

            filename = client_socket.recv(1024).decode()
            print(f"Receiving file: {filename}")

            client_socket.send("Ready to receive".encode())

            with open(filename, 'wb') as f:
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    f.write(data)

            print(f"File {filename} received successfully")
            client_socket.close()

        except socket.timeout:
            continue
        except Exception as e:
            print(f"Error: {e}")
            if 'client_socket' in locals():
                client_socket.close()

def main():
    stop_event = threading.Event()
    receiver_thread = threading.Thread(target=receive_file, args=(stop_event,))
    receiver_thread.start()

    recording = False
    
    def on_space_press(e):
        nonlocal recording
        if e.event_type == keyboard.KEY_DOWN and not recording:
            print("Starting recording...")
            recording = True
            start_recording()
        elif e.event_type == keyboard.KEY_UP and recording:
            print("Stopping recording...")
            recording = False
            stop_recording()

    keyboard.on_press_release('space', on_space_press)

    try:
        keyboard.wait('space')
    finally:
        stop_event.set()
        receiver_thread.join()

if __name__ == "__main__":
    main()