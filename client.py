import socket, threading

# 1. Digita o IP e porta de um servidor que esteja ativo para se conectar ao chat
serverIP = input("IP do servidor: ")
PORT = int(input("PORTA: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Verificar se tem algum servidor ativo com IP e Porta digitados pelo cliente
try:
  username = input('Diga seu nome: ')
  client.connect((serverIP, PORT))
  print(f'Conexão feita com sucesso ao {serverIP}:{PORT}')
except:
  print(f'ERROR: Por favor confira seu IP e Porta: {serverIP}:{PORT}')

# 3. Recebe a mensagem que foi enviada pelo servidor que ele está ativo no chat
def receiveMessage():
  while True:
    try:
      message = client.recv(2048).decode('ascii')
      if message == 'getUser':
        client.send(username.encode('ascii'))
      else:
        print(message)
    except:
      print('ERROR: Cheque sua conexão com o servidor, ou a conexão pode estar Offline ')
# 4. Envia uma mensagem para o servidor
def sendMessage():
  while True:
    client.send(input().encode('ascii'))

thread1 = threading.Thread(target=receiveMessage, args=())
thread2 = threading.Thread(target=sendMessage, args=())

thread1.start()
thread2.start()