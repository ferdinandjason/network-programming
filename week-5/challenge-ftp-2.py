import os
import sys
import time
from ftplib import FTP , error_perm

sys.stdout.write(">> [IP USERNAME PASSWORD]\n")
sys.stdout.write(">> ")
login = sys.stdin.readline()
login = login[:-1].split(' ')
ftp = FTP(login[0],login[1],login[2])
print "Welcome:", ftp.getwelcome()

def download_files(path, destination):
    print path
    os.chdir(destination)
    print(destination + path + '/')
    os.mkdir(destination + path + '/')
    print "Created: " + destination+ path

    filelist = ftp.nlst()
    print(filelist)

    for filee in filelist:
        print filee
        time.sleep(0.05)
        print filee
        try:
            ftp.cwd(filee)
            download_files(path + "/" + filee + "/", destination)
        except error_perm:
            os.chdir(destination + path)
            print filee
            try :
                ftp.retrbinary("RETR " + filee, open(os.path.join(destination + path, filee),"wb").write)
                print "Downloaded: " + filee
            except :
                pass

while True:
    sys.stdout.write(">> ")
    command = sys.stdin.readline()
    command = command[:-1].split(' ')
    cmds = command[0]
    try :
        args = command[1]
    except :
        args = ''
    if cmds == "NLST":
        dirs = ftp.nlst()
        for dir in dirs:
            print dir
    if cmds == "RETR":
        with open(args,'wb') as fd:
            ftp.retrbinary('RETR '+args, fd.write)
    if cmds == "STOR":
        with open(args, "rb") as fd:
            ftp.storbinary('STOR '+args, fd)
    if cmds == "PWD":
        cwd = ftp.pwd()
        print cwd
    if cmds == "MKD":
        ftp.mkd(args)
    if cmds == "DOWNPRESS":
        ftp.cwd(args) 
        download_files(args, os.getcwd()+'/')
        os.system("zip -r /home/ferdinand/Code/network-programming/week-5/TEST.zip " + os.getcwd())
        os.system("rm -rf /home/ferdinand/Code/network-programming/week-5/"+args)