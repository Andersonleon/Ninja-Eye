
import os
import socket
import ssl


def firstSetup():
  ##setup files, folders, keys etc here

      folders = ["logs"]
      for folderName in folders:

        foldersSetup = f"/etc/NinjaEye/{folderName}"
        os.makedirs(foldersSetup, exist_ok=True)
        return


def sslCert():
    opensslreq = "openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt -days 365 -nodes"
    os.system(opensslreq)


def sshLog():
  sshCmd = "grep sshd /var/log/auth.log > /etc/NinjaEye/logs/sshCompare.txt" 
  os.system(sshCmd)


def sshCompare():
    afterLog = open("/etc/NinjaEye/logs/sshCompare.txt")
    beforeLog = open("/etc/NinjaEye/logs/ssh.txt")

    beforeLog_data = beforeLog.readlines()
    afterLog_data = afterLog.readlines()

    before_set = set(beforeLog_data)
    after_set = set(afterLog_data)
 
    differences = after_set - before_set 

    if differences:
        for line in differences:
            print("\t ALERT! ", line, end="")
            ##send this information to command and control!


    else:
        print("No differences found.")

    afterLog.close()
    beforeLog.close()
         

def serverCommunication():
  print("hello world")


  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


  context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
  context.load_verify_locations("server.crt")


  with context.wrap_socket(client, server_hostname="localhost") as secure_socket:
     secure_socket.connect(("127.0.0.1", 9999))
     print("SSL connection established")

     secure_socket.send("hello from ssl client".encode())
     response = secure_socket.recv(1024).decode()
     print(f"recieved: {response}")




if __name__ == "__main__":
  firstSetup()
  sslCert()
  sshLog()
  sshCompare()
  serverCommunication()