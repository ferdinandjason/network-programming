# Challenge Minggu 5

## Outline

- [Challenge Minggu 5](#challenge-minggu-5)
  - [Outline](#outline)
  - [Deskripsi Challenge](#deskripsi-challenge)
  - [Dokumentasi](#dokumentasi)

## Deskripsi Challenge

1. FTP interatif :
   - User dapat memasukkan username dan passowrd serta IP FTP Server.
   - Fasilitas input berupa >>
   - User dpat melist isi direktori, mendownlod, mengupload, membuat folder, dan mendapatkan present working directory
2. Modifikasi :
   - Buatlah perintah `DOWNPRESS <nama folder>` agar mendownload folder beserta seluruh subfolder didalamnya, kemudian menzip file tersebut.

## Dokumentasi

1. FTP interaktif
   - Membuat file `challenge-ftp-1.py`
   ```python
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
   ```
2. Membuat command `DOWNPRESS`, dengan membuat fungsi mendownload file secara rekursif

   ```python
   def download_files(path, destination):
       os.chdir(destination)
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
   ```

   Kemudian menzip file tersebut dan menghapus foldernya

   ```python
   os.system("zip -r /home/ferdinand/Code/network-programming/week-5/TEST.zip " + os.getcwd())
   os.system("rm -rf /home/ferdinand/Code/network-programming/week-5/"+args)
   ```
