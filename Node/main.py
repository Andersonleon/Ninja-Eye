
import os
import datetime
import time

"""todo 

auto get ssh key from idrsa - command 
in parse_user_input() make it so that the information is stored in a file and the file is checked at launch to speed up workflow, - node
ssh whitelist - command 
inital connection- node 

add cool ascii art -both 
optimisation - both 

"""


def firstSetup():
    ##Setup required directories and files.
    folderpath = "/etc/NinjaEye"
    folders = ["logs", "client_info", "logs/alerts"]
    try:
        for folder_name in folders:
            folder_path = os.path.join(folderpath, folder_name)
            os.makedirs(folder_path, exist_ok=True)
        print(f"Directories set up successfully in {folderpath}.")
    except PermissionError:
        print("Permission denied: Please run the script with elevated privileges.")
        exit(1)


def parse_user_input():
    # ask  the user to input the one-line information
    user_input = input("Paste the system information command gave you (one line): ").strip()

    try:
        
        # Parse the input string into pairs
        info_dict = {}
        for pair in user_input.split(", "):  
            key, value = pair.split(": ", 1)  
            info_dict[key.strip()] = value.strip()

        # Assign variables from the  dictionary to  variable names for use 
        ip_address = info_dict.get("IP Address", "N/A").split()[0] ## temporary fix to getting too many ips 
        hostname = info_dict.get("Hostname", "N/A")
        ssh_key = info_dict.get("SSH Key", "N/A")
        commands_name = info_dict.get("Commands Name", "N/A")
        ssh_username = info_dict.get("SSH Username", "N/A")

        # Return the values for commandConnection()
        return ip_address, hostname, ssh_key, commands_name, ssh_username

    except ValueError:
        print("Error: Input format is incorrect. Ensure the data is in 'Key: Value' pairs separated by commas.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

##scp testscp.txt {ip}:/tmp for transfering files. ask client if they use ssh keys cause for this we are using ssh keys!

def commandConnection(ip_address, hostname, ssh_username, data):    #main function used for connecting to command through scp
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
    filereason = "log" ##temp solution untill a better way of determining what filetype should be 
    filename = f"NINJAEYE-{ip_address}-{hostname}-{currentTime}-{filereason}"  
    filepath = f"/etc/NinjaEye/logs/alerts/{filename}"


    # Write "data" to file 
    with open(filepath, "w") as f:
        f.write(data)

    os.system(f"scp {filepath} {ssh_username}@{ip_address}:/tmp") # sends data to server
    return filename



#def sshLog(): # gathers ssh logs and places them into a compare file



def sshCompare(): # comparison function of ssh logs to predefined ssh log
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
            filename = commandConnection(ip_address, hostname,  ssh_username, alert_data)  # file reason will be parsed in here 
         

        else:
            print("No differences found.")

        afterLog.close()
        beforeLog.close()
        time.sleep(30) #checks every 30 seconds 

if __name__ == "__main__":
  firstSetup()
 # sshLog()
 #line above is commented for testing 
  ip_address, hostname, ssh_key, commands_name, ssh_username = parse_user_input()  # Store the returned values
  sshCompare()

  