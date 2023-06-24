import sys
import threading
import queue
import time
import requests

# Definição das variáveis globais
lastphoto = 289  # Última foto a ser baixada
lastphotoid = 1553030  # ID da última foto
profileid = 173993  # ID do perfil
baseurl = 'https://images.meupatrocinio.com/'  # URL base
queued = 0  # Contador de fotos enfileiradas
increment = 1  # Incremento
num_threads = 10 # Defina o número desejado de threads

# Declaração da variável inurl com valor padrão
inurl = 'https://images.meupatrocinio.com/173993/15538230/289/'  # URL de entrada padrão

# Verifica se foi fornecido um argumento na linha de comando
if len(sys.argv) > 1:
    inurl = sys.argv[1]

if len(sys.argv) > 2:
    increment = int(sys.argv[2])

# Separar os dados contidos na variável inurl
split_url = inurl.split('/')
baseurl = split_url[0] + '//' + split_url[2]
profileid = int(split_url[3])
lastphotoid = int(split_url[4])
lastphoto = int(split_url[5])

class DownloadManager:
    def __init__(self):
        self.baseurl = baseurl
        self.profileid = profileid
        self.lastphotoid = lastphotoid
        self.lastphoto = lastphoto
        self.increment = increment
        self.queue = queue.Queue()

    def run(self):
        # Inicializa as threads
        # num_threads = 10  # Defina o número desejado de threads
        global num_threads

        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            threads.append(thread)

        # Alimenta a fila com os dados iniciais
        self.enqueue_photos()

        # Loop principal
        while True:
            if self.queue.qsize() <= num_threads + 5:
                self.enqueue_photos()
            # self.enqueue_photos()
            time.sleep(0.005)

    def enqueue_photos(self):
        # Enfileira as fotos para download
        # for photoid in range(self.lastphotoid, self.lastphotoid + 1):
        #     url = f"{self.baseurl}{self.profileid}/{photoid}/{self.lastphoto}/"
        url = f"{self.baseurl}/{self.profileid}/{self.lastphotoid}/{self.lastphoto}/"
        # print(url)
        self.queue.put(url)

        #Incrementa lastphotoid
        self.lastphotoid += self.increment

    def worker(self):
        # print('worker')
        while True:
            try:
                url = self.queue.get()
                self.download_photo(url)
                self.queue.task_done()
            except queue.Empty:
                break

    def download_photo(self, url):
        # Remonta a URL com base nos parâmetros
        photoid = url.split('/')[4]
        profileid = url.split('/')[3]
        lastphotoid = url.split('/')[4]
        lastphoto = url.split('/')[5]

        # url = f"{self.baseurl}/{self.profileid}/{self.lastphotoid}/{photoid}/"
        # url = f"{self.baseurl}/{self.profileid}/{self.lastphotoid}/{self.lastphoto}/"
        print (url + '                                                            ', end="\r")
        # time.sleep(0.2)

        # Realiza o download
        try:
            response = requests.get(url, stream=True)
        except:
            print('Esperando conexão em 2 segundos...                             ', end="\r")
            # Aguarda 2 segundos e tenta novamente
            time.sleep(2)
            self.download_photo(url)
        else: 
            split_url = url.split('/')

            if response.ok:
                # print('200')
                # Obtém o tipo de arquivo
                mimetype = response.headers.get('content-type').split('/')[-1]

                # Salva o arquivo com base nas informações
                filename = f"{lastphoto}_{lastphotoid}_{profileid}.{mimetype}"
                # filename = f"{self.lastphoto}_{self.lastphotoid}_{self.profileid}.{mimetype}"
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)

                # Atualiza o lastphotoid e lastphoto, imprime a mensagem
                # self.lastphotoid += self.increment
                # self.lastphoto += self.increment
                self.lastphotoid = int(split_url[4])
                self.lastphoto = int(split_url[5]) + self.increment
                print(f"Arquivo salvo com o nome: {filename}                                                                  ")

                # Limpa a fila de downloads após o download bem-sucedido
                self.queue.queue.clear()
                return

            else:
                # Imprime as informações
                # print(f"Perfil: {self.profileid}, ID de Foto: {self.lastphotoid}, N. Foto: {self.lastphoto}", end="\r")
                
                # Atualiza o lastphotoid e lastphoto, imprime a mensagem
                # self.lastphotoid += self.increment
                # self.lastphotoid = int(split_url[4]) + 1
                return




if __name__ == '__main__':
    manager = DownloadManager()
    # print("Start")
    manager.run()
