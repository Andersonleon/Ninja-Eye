import socket
import ssl
import os 


def firstSetup():
  ##setup files, folders, keys etc here

      folders = ["logs"]
      for folderName in folders:

        foldersSetup = f"/etc/NinjaEye/{folderName}"
        os.makedirs(foldersSetup, exist_ok=True)
        return


def sslCert():
    if not os.path.exists("server.crt") or not os.path.exists("server.key"):
        openssl_cmd = "openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt -days 365 -nodes"
        os.system(openssl_cmd)




def serverCommunication():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 9999))
    server_socket.listen(5)
    print("Server listening on port 9999")

    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        with context.wrap_socket(client_socket, server_side=True) as secure_socket:
            print("SSL connection established")
            
            data = secure_socket.recv(1024).decode()
            print(f"Received: {data}")
            secure_socket.send("Hello from SSL server".encode())

if __name__ == "__main__":
    firstSetup()
    sslCert()
    serverCommunication()
