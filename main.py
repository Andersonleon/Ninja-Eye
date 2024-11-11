
import os
import filecmp


def firstSetup():
  ##setup files, folders, keys etc here

      folders = ["logs"]
      for folderName in folders:

        foldersSetup = f"/etc/NinjaEye/{folderName}"
        os.makedirs(foldersSetup, exist_ok=True)
        return


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
    else:
        print("No differences found.")

    afterLog.close()
    beforeLog.close()
         
####
# Strings that SSH connections can be identified by
#  session opened for user
#authentication failure
#identify ssh attampts and print "alert if identified"
####

if __name__ == "__main__":
  firstSetup()
  sshLog()
  sshCompare()