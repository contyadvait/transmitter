import socket
import os
import sys

class FileTransmitter:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """Establish connection to the server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to {self.host}:{self.port}")
        self.socket.connect((self.host, self.port))

    def send_file(self, filename):
        """Send a file to the connected server"""
        # Check if file exists
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' not found")

        try:
            if not self.socket:
                self.connect()
            
            # Send filename first
            self.socket.send(os.path.basename(filename).encode())
            
            # Wait for receiver acknowledgment
            self.socket.recv(1024)
            
            # Open and send the file
            with open(filename, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.socket.send(data)
                    
            return True
            
        except Exception as e:
            raise e

    def close(self):
        """Close the connection"""
        if self.socket:
            self.socket.close()
            self.socket = None

def main():
    if len(sys.argv) != 2:
        print("Usage: python network-send.py <filename>")
        return

    transmitter = FileTransmitter()
    try:
        transmitter.send_file(sys.argv[1])
        print(f"File {sys.argv[1]} sent successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        transmitter.close()

if __name__ == "__main__":
    main()