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



def key_generation(): # generates a key that is used to setup Nodes 
    # Define the output file path
    output_file = "/etc/NinjaEye/client_info/system_info.txt"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        # Collect system information
        ip_address = subprocess.getoutput("hostname -I").strip() #ip
        hostname = subprocess.getoutput("hostname").strip() # systems name
        commands_name = subprocess.getoutput("whoami") # username 

        # Prompt the user for SSH credentials
        ssh_username = input("Enter your COMMAND SSH username: ").strip()
       

        # Check if an SSH key exists
        ssh_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
        ssh_key = "Not available"
        if os.path.exists(ssh_key_path):
            with open(ssh_key_path, "r") as key_file:
                ssh_key = key_file.read().strip()

        # Combine all information into one line
        data = (
            f"IP Address: {ip_address}, Hostname: {hostname}, "
            f"SSH Username: {ssh_username}, "
            f"SSH Key: {ssh_key}, "
            f"Commands Name: {commands_name}, "
        )

        # Write the information to the output file
        with open(output_file, "w") as f:
            f.write(data + "\n")

        print(f"System information written to {output_file}. Copy information contained to node for setup")
        print(data)

    except PermissionError:
        print("Permission denied: Unable to write system information. Try running as root.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
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
    key_generation()
    alertmonitoring()
