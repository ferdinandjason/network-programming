# Challenge Minggu 6

## Outline

- [Challenge Minggu 6](#challenge-minggu-6)
  - [Outline](#outline)
  - [Deskripsi Challenge](#deskripsi-challenge)
  - [Dokumentasi](#dokumentasi)

## Deskripsi Challenge

1. Buatlah program berbasis jaringan dengan mengunakan prinsip haring atau torrent-like. Misal : Client A mengontak server untuk mendownload file XYZ.txt, server pun mengirimkannya ke Client A. Tak berapa lama kemdian, Client B mengontak server untuk mendowndload file XYZ.txt. Alih alh mengirimkannya langsungm untuk meringankan loadnya, server akan memerintahkan client A untuk mengirimkan filenya ke Client B.

## Dokumentasi

1. Soal 1

   - Dibatasi dengan file yang kecil, oleh karena itu file dikirimkan dengan format =
     Pesan 1 : `FILE|<nama file>|<client address>`
     Pesan 2 : `<ISI FILE>`
   - Sehingga fungsi untuk mengirimkan file adalah sebagai berikut :

   ```python
   def send_file(filename, server_socket, client_addresss):
       server_socket.sendto(
           'FILE|'+str(client_addresss[1])+'_'+filename+'|', client_addresss)
       with open(filename, 'r') as f:
           server_socket.sendto(f.read(1024), client_addresss)

   ```

   - Untuk mengingat bahwa CLient A pernah mendownload file XYZ.txt, server menyimpan bahwa last time file tersebut telah berada `client_address` tertentu menggunakan dictionary pada python. Apabila sudah pernah diakses maka server mengirimkan perintah ke Client A untuk mengirimkan file XYZ.txt ke client B yang dikirimkan menggunakan format = `COMMAND|<nama file>|<ip client B>|<port client B>`.
