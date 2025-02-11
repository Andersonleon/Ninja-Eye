
import os
import datetime
import time
from dotenv import load_dotenv
import threading 

load_dotenv() 

"""todo 

setup an aws instance - for command to access and for node to connect too for  file transfer

the file compare names need to be changed to be more descriptive and fixed as there is an logic error 

auto get ssh key from idrsa - command 
ssh whitelist - command 
inital connection- node 

add cool ascii art -both 
optimisation - both 

"""


def firstSetup():
    ##Setup required directories and files.
    folderpath = "/etc/NinjaEye"
    folders = ["logs", "client_info", "logs/alerts", "file_compare"]
    try:
        for folder_name in folders:
            folder_path = os.path.join(folderpath, folder_name)
            os.makedirs(folder_path, exist_ok=True)
        print(f"Directories set up successfully in {folderpath}.")
    except PermissionError:
        print("Permission denied: Please run the script with elevated privileges.")
        exit(1)

  

def get_env_variable():
    try:
       ssh_key = os.getenv('SSH_KEY')
       ip_address = os.getenv('IP_ADDRESS')
       ssh_username = os.getenv('SSH_USERNAME')
    
       print("enviroment variables loaded")
       return ssh_key, ip_address, ssh_username
    
    except Exception as e:
        print(f"An error occurred with the enviroment variables: {e}")
        return None

def commandConnection(ip_address, ssh_username, data, filereason):    #main function used for connecting to command through scp
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
    filename = f"NINJAEYE-{ip_address}-{currentTime}-{filereason}"  
    filepath = f"/etc/NinjaEye/logs/alerts/{filename}"


    # Write "data" to file 
    with open(filepath, "w") as f:
        f.write(data)

    os.system(f"scp {filepath} {ssh_username}@{ip_address}:/tmp") # sends data to server
    return



#def sshLog(): # gathers ssh logs and places them into a compare file

def fileChecker():  
    test =  os.stat("control_file.txt") ## the file that is being accessed to test the function using nano
    statfile = "/etc/NinjaEye/file_compare/newfile.txt" 
    with open(statfile, "w") as file: 
        file.write(f"{test.st_atime} : {test.st_mtime} \n")
    access_time = test.st_atime
    modify_time = test.st_mtime
    fileCompare(access_time, modify_time) 
        #return access_time, modify_time 


def sshCompare(): # comparison function of ssh logs to predefined ssh log
    filereason = "unauthorizedSSH" 
    while True:

        sshCmd = "grep sshd /var/log/auth.log > /etc/NinjaEye/logs/sshCompare.txt"  ## 
        os.system(sshCmd)

        afterLog = open("/etc/NinjaEye/logs/sshCompare.txt")
        beforeLog = open("/etc/NinjaEye/logs/ssh.txt")

        beforeLog_data = beforeLog.readlines()
        afterLog_data = afterLog.readlines()

        before_set = set(beforeLog_data)
        after_set = set(afterLog_data)
    
        differences = after_set - before_set 

        if differences:
            alert_data = "" 
            for line in differences:
                print("\t ALERT! ", line, end="")
                alert_data += line #combines the alert data 

                ##sends information to command 
            commandConnection(ip_address, ssh_username, alert_data, filereason)  # file reason will be parsed in here 
         

        else:
            print("No differences found.")

        afterLog.close()
        beforeLog.close()
        time.sleep(30) #checks every 30 seconds 



def fileCompare(access_time, modify_time):
    filereason = "unauthorizedAccess"
    while True:

        afterLog = open("/etc/NinjaEye/file_compare/newfile.txt") ## the file that has the current time the file was accessed
        beforeLog = open("previousfile.txt")

        beforeLog_data = beforeLog.readlines()
        afterLog_data = afterLog.readlines()

        before_set = set(beforeLog_data)
        after_set = set(afterLog_data)
    
        differences = after_set - before_set 
        if differences:
            alert_data = "" 
            for line in differences:
                print(f"\t ALERT! folder accessed ", line, end="")
                alert_data += line #combines the alert data 

                ##sends information to command 
            commandConnection(ip_address, ssh_username, alert_data, filereason)  # file reason will be parsed in here          

        else:
            print("No differences found.")

        afterLog.close()
        beforeLog.close()
        ##write code into previous file 
        with open("previousfile.txt", "w") as file: 
            file.write(f"{access_time} : {modify_time} \n")


        time.sleep(30) 
        fileChecker()

if __name__ == "__main__":
  

  firstSetup()
  ssh_key, ip_address, ssh_username = get_env_variable()
  
  sshThread = threading.Thread(target=sshCompare, daemon=True)  # Create a thread for the sshCompare function
  sshThread.start() # Start the thread

  fileThread = threading.Thread(target=fileChecker, daemon=True)  # Create a thread for the fileChecker function
  fileThread.start() # Start the thread

  sshThread.join()  # Wait for the thread to finish
  fileThread.join()  # Wait for the thread to finish

  sshCompare()
  fileChecker() 
  #fileCompare() 
  