# Challenge Minggu 1

## Outline
- [Challenge Minggu 1](#challenge-minggu-1)
  - [Outline](#outline)
  - [Deskripsi Challenge](#deskripsi-challenge)
  - [Dokumentasi](#dokumentasi)

## Deskripsi Challenge
1. Modifikasi `server2.py` dan `client1.py` untuk membuat program kalkulator sederhana dengan socket programming, client bisa mengirimkan operasi matematika dengan bentuk `a op b` ke server dan server bisa membalasnya dengan hasil dari operasi matematika tersebut. \
Contoh : \
**client** : `1 + 4` \
**server** : `5`

2. Modifikasi soal sebelumnya, agar server bisa menerima banyak client dan dapat me-broadcast hasil dari operasi matematika dari client tertentu kepada semua client dengan format `ip_client,port_socket,operasi_matematika,hasil_operasi`. Kemudian ketika salah satu client mengirim string `END` maka server membalas `TOTAL : {hasil_pertamabahan_operasi_matematika} END` kepada semua client dan memutuskan koneksi.

## Dokumentasi
1. Soal 1
      - `server2.py` dapat dimodifikasi dengan menambahkan parser pada data yang dikirimkan, karena operasi matematika yang dikirim selalu `a op b`, maka string tersebut dapat di pisah menjadi `['a','op','b']` kemudian 
        ```python
        operasi = data.split(' ')
        if operasi[1] == '+' :
            print int(operasi[0]) + int(operasi[2])
        elif operasi[1] == '-' :
            print int(operasi[0]) - int(operasi[2])
        elif operasi[1] == '*' :
            print int(operasi[0]) * int(operasi[2])
        elif operasi[1] == '/' :
            print int(operasi[0]) / int(operasi[2])
        ```
    - Untuk `client1.py` dapat dimodifikasi dengan menambahkan input untuk dikirimkan ke server
        ```python
        string_matematika = raw_input('Masukkan operasi matematika sederhana : ')
        ```
        Kemudian menampilkan balasan dari server.
2. Soal 2
   - Karena melibatkan komunikasi 2 arah, maka akan digunakan 2 socket untuk menjalankan soal ini, socket pertama digunakan untuk mengirimkan operasi matematika ke server dari beberapa client, dan socket kedua digunakan untuk memberi balasan server.
   - Server akan membuat `thread` untuk masing masing client yang connect melalui port `5000` 
    ```python
    def start(self):
        self.start_server_socket()
        try:
            while True:
                thread = ServerThread(self.server_sock.accept(), self, self.reply_port)
                thread.daemon = True
                thread.start()

                self.clients.append(thread)

        except KeyboardInterrupt:
            print 'Closing socket connection'
            self.server_sock.close()
            sys.exit(0)
    ```
   - Kemudian sama seperti pada soal 1, memparse data yang dikirim dengan eksepsi untuk string `END` dan membroadcastkannya ke semua client dengan format yang diberikan
    ```python
    try:
        while True:
            data = self.client.recv(MAX_BUFFER)
            print data
            if data == 'END':
                self.server.broadcast(
                    'TOTAL AKHIR : ' + str(self.server.total_result) + ' END')
                self.client.close()
            else:
                result = self.parse_data(data)

                self.server.total_result += result
                reply_message = data + ',' + str(result)
                self.server.broadcast(reply_message)
    except Exception:
        pass
    ```
   - Untuk broadcast, connect terhadap socket client dengan alamat ip client dengan port `5001` yang disediakan client kemudian mengirim pesan balasan kepada client
   -  Pada Client, terdapat 2 socket, socket untuk koneksi kepada client, serta socket sebagai *server* untuk mendapatkan balasan yang dikirim oleh server. Socket balasan ini dijalankan menggunakan `thread`, sehingga bisa terjadi secara real time.
   ```python
    def start(self):
		self.create_connection()
		self.create_reply_connection()

		while True:
			try:
				command = raw_input('math> ')
				self.socket.send(command)
				reply_thread = threading.Thread(target=self.reply_listener)
				reply_thread.start()
			except KeyboardInterrupt:
				self.socket.close()
				sys.exit(0)
   ```
   -  Kemudian untuk `thread reply_listener` terdapat receive dari yang dikirim server serta terdapat eksepsi jika sudah `END`
   ```python
    def reply_listener(self):
		try:
			server_reply_socket , _ = self.reply_socket.accept()
		except:
			pass

		reply = server_reply_socket.recv(MAX_BUFFER)
		if reply[-3:] == 'END':
			self.socket.close()
			sys.exit()
		print reply

		self.reply_socket.close()
   ```

