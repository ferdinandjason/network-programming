from ftplib import FTP

ftp = FTP('10.151.254.61')
print "Welcome:", ftp.getwelcome()

ftp.login("progjar","progjar123")
print "Current working directory:", ftp.pwd()
names = ftp.nlst()
print "List of directory: ", names

fd = open('kdei-bundle', 'wb')
ftp.retrbinary('RETR kdei-bundle',fd.write)
fd.close()

ftp.quit()