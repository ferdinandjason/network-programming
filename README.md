# Pemrograman Jaringan

Dokumentasi Mata Kuliah Pemrograman Jaringan

## Outline
- [Pemrograman Jaringan](#pemrograman-jaringan)
  - [Outline](#outline)
  - [Materials](#materials)
    - [Week 1](#week-1)
      - [Terminologi](#terminologi)
      - [Client Server](#client-server)
      - [Socket](#socket)
    - [Week 2](#week-2)
      - [Select](#select)
      - [Poll](#poll)
  - [Challenge](#challenge)

## Materials
### Week 1
#### Terminologi
- Host : perangkat
- Alamat IP : alamat perangkat
- Port : "pintu" untuk pertukaran data
  - Diatur oleh *Internet Assigned Numbers Authority* (IANA). (http://www.iana.org/assignments/port-numbers)
  - Terdapat 3 range :
    - *Well-Known Ports* (0 - 1023)
    - *Registered Ports* (1024- 49151)
    - *Free Ports* (49152 - 65535)
- Socket : "end-point" komunikasi
- Client-Server
  
#### Client Server
- Port pada server ditentukan pada aplikasi
- Port pada klient ditentukan oleh sistem operasi secara acak dan port yang tersedia saat itu.

#### Socket
- Merupakan *end-point* dari komunikasi antar 2 host
- Terdapat beberapa operasi dasar:
  - Membuka koneksi
  - Mengirim data
  - Menerima data
  - Menutup koneksi
  - *Bind* ke suatu port
  - Menerima koneksi dari *host* lain ke *bound port*
- Terdapat 2 tipe socket di `python`
  - UDP -> `SOCK_DGRAM`
  - TCP -> `SOCK_STREAM`
- Tipe alamat socket di `python` ada 3 :
  - `AF_UNIX` = *Socket* antara 2 proses yang berjalan dan berkomunikasi dalam satu *host*
  - `AF_INET` = *Socket* antara 2 proses yang bisa berjalan pada *host* yang berbeda menggunakan IPv4
  - `AF_INET6` = Sama dengan `AF_INET` tetapi menggunakan IPv6 
- Pada bahasa pemrograman `python`, server socket memiliki fungsi :
  - `listen(args)` : Mendegarkan koneksi klien yang masuk, memiliki parameter jumlah antrian koneksi klien.
  - `accept()` : Menerima koneksi dari klien, memiliki return value client socket serta client address.

### Week 2
#### Select
- Menangani banyak klien dalam suatu waktu
- Bergantian antara banyak klien yang terkoneksi
- Menunggu pengiriman data satu klien, melayani klien yang lain
- Diproses setelah salah satu socket selesai bertransaksi
- Fungsi select membuat pemantauan koneksi jamak dalam satu waktu menjadi jauh lebih mudah
- Sintaks :
  - `select(rlist, wlist, xlist[, timeout])`
    - `rlist` : wait until ready for reading, list of objects to be checked for incoing data to be read
    - `wlist` : wait until ready for writing, list of objects that will receive outgoing data when there is room in their buffer
    - `xlist` : wait for *exceptional condition*, list of object that may have an error

#### Poll
- Mempunyai *behavior* yang mirip dengan select
- Hanya berjalan di sistem operasi yang berbasis UNIX
  - Tidak bissa berjalan di Windows, sehingga jarang digunakan
- Menyediakan solusi yang lebih scalable untuk server yang menghandle junlah client yang besar atau sangat besar
- Perbedaan performa :
  - Poll : system call hanya memerlukan listing dari file descriptor of interest
  - Select : system akan membangun bitmap, menset 0/1 setiap bit dari file descriptor of interest. Kemudian mengecek keseluruhan bitmap satu persatu di setiap perubahan



## Challenge
- [Week 1](week-1)
- [Week 2](week-2)
- [Week 3](week-3)

