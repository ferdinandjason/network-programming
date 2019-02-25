# Challenge Minggu 2

## Outline
- [Challenge Minggu 2](#challenge-minggu-2)
  - [Outline](#outline)
  - [Deskripsi Challenge](#deskripsi-challenge)
  - [Dokumentasi](#dokumentasi)

## Deskripsi Challenge
1. Modifikasi code `select` agar bisa mencatat semua pesan yang diterima di server kedalam sebuah file. Catat IP,Port,Timestamp, Pesan yang dikirimkan dari Client
2. Modifikasi code `select` :
   - Client cukup mengetik nama file yang akan dikirim
   - Client akan mengirimkan data berupa isi file secara bertahap beserta nama filenya.
   - Server menerima kiriman data dan menyusun ulang menjadi sebuah file dan disimpan di*local storage* server

## Dokumentasi
1. Soal 1
    - Menambahkan string IP,Port,Timestamp, Pesan serta menyimpannya dalam file `pesan.log`
    ```python
    string = client_sockets[sock][0] + ',' + str(client_sockets[sock][1]) + ',' + str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')) + ',' + data
    with open('pesan.log','a') as f:
        f.write(string)
    ```
2. Soal 2
    - Client mengirimkan file yang dibagi bagi dengan `MAX_BUFFER` dimana nilainya adalah `1024 bit` dan mengirimkannya secara bertahap
    ```python
    filename = sys.stdin.readline()
    filename = filename[:-1]
    with open(filename,'rb') as f:
        chunk = f.read(1024)
        while chunk:
            client_socket.send(chunk)
            chunk = f.read(1024)

    client_socket.send('NAMA:'+filename)
    ```
    - Server menerima file tersebut dengan `MAX_BUFFER` sebanyak `1024 bit` sampai ditemukan nama file.
    ```python
    data = sock.recv(1024)
    with open('temp_'+str(sock.getpeername()[1]),'wb') as f:
        while True:
            if(data[:4] == 'NAMA') :
                break
            f.write(data)
            data = sock.recv(1024)
    print('File Received !')
    os.rename('temp_'+str(sock.getpeername()[1]),data[5:]+'_server')
    ```
    - Server membuat file dengan nama temporary terlebih dahulu, kemudian me-*rename* nama file bedasarkan nama yang dikirim oleh 