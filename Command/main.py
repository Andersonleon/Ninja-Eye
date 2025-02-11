import os 
import subprocess
import time
import shutil

def firstsetup():
    ##Setup required directories and files.
    folderpath = "/etc/NinjaEye"
    folders = ["logs", "client_info", "alerts"]
    try:
        for folder_name in folders:
            folder_path = os.path.join(folderpath, folder_name)
            os.makedirs(folder_path, exist_ok=True)
        print(f"Directories set up successfully in {folderpath}.")
    except PermissionError:
        print("Permission denied: Please run the script with elevated privileges.")
        exit(1)




def alertmonitoring(): # Monitors for incomming files in tmp folder and alerts the user if there is one then stores the file
    
    folderpath = "/tmp/"

    while True:
        for filename in os.listdir(folderpath):
         if filename.startswith("NINJAEYE"):
             source = (folderpath + filename)
             shutil.move(source, "/etc/NinjaEye/alerts")
             print(f"ALERT! See /etc/NinjaEye/alerts/{filename} for more information!")
        time.sleep(5)


if __name__ == "__main__":
    firstsetup()
    alertmonitoring()
