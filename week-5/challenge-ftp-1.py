import sys

from ftplib import FTP

sys.stdout.write(">> [IP USERNAME PASSWORD]\n")
sys.stdout.write(">> ")
login = sys.stdin.readline()
login = login[:-1].split(' ')
ftp = FTP(login[0],login[1],login[2])
print "Welcome:", ftp.getwelcome()

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
