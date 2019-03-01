# Challenge Minggu 3

## Outline
- [Challenge Minggu 3](#challenge-minggu-3)
    - [Outline](#outline)
    - [Deskripsi Challenge](#deskripsi-challenge)
    - [Dokumentasi](#dokumentasi)

## Deskripsi Challenge
1. Menjelaskan `challenge-server-1.py` serta membuat `challenge-client-1.py`.
2. Menjelaskan dan memperbaiki `challenge-server-2.py` serta membuat `challenge-client-2.py`.
3. Modifikasi `challenge-server-1.py` agar bisa menerima input beberapa dari operasi matematika dari client, 
`1 + 5,4 * 6,8 / 2` (1 string mendapatkan 1 thread), kemudian menampilkan hasilnya dalam urutan terbalik
`4,24,6`.Secret

## Dokumentasi
3. Soal 3
   - Modifikasi class `Client` menjadi 
    ```python
    class Client(threading.Thread):
        def __init__(self,(client,address)):
            threading.Thread.__init__(self)
            self.client = client
            self.address = address
            self.size = 1024
        def run(self):
            running = 1
            while running:
                data = self.client.recv(self.size)
                if data:
                    t = threading.Thread(target=jawab, args=(self.client,data))
                    t.start()
                else:
                    self.client.close()
                    running = 0
    ```
    Agar setiap string yang diterima dibuatkan thread baru dengan fungsi `jawab`.
   - Mendefinisikan fungsi `jawab` sebagai berikut
    ```python
    def jawab(socket,data):
        stack = Queue.LifoQueue()
        matematika = data.split(',')
        for m in matematika:
            stack.put(m)
        output = []
        while not stack.empty():
            output.append(str(eval(stack.get())))

        socket.send(','.join(output)+'\n')
        print ','.join(output)+'\n'
    ```