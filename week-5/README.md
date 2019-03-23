# Challenge Minggu 5

## Outline

- [Challenge Minggu 5](#challenge-minggu-5)
  - [Outline](#outline)
  - [Deskripsi Challenge](#deskripsi-challenge)
  - [Dokumentasi](#dokumentasi)

## Deskripsi Challenge

1. Buatlah protokol FTP sederhana menggunakan `ftplib`, dengan menerapkan perintah : `NLST` , `RETR`, `STOR`, `PWD`, dan `MKD`.
2. Modifikasi soal 1, agar menerima perintah `DOWNPRESS`, yaitu mendownload folder beserta seluruh sub folder didalamnya kemudian mengkompressnya.

## Dokumentasi

1. Soal 1

   - Menggunakan library `ftplib` :

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

2. Mendownload folder beserta seluruh sub folder dialamnya dilakukan secara rekursif apabila hasil list direktori tersebut adalah sebuah folder. Berikut merupakan kode untuk mendownload folder seacara rekursif.

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
