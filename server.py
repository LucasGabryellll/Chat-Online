import socket, threading

HOST = input("Host: ")
PORT = int(input("Port: "))

# 1. Listamos o servidor no IP e porta que escolhemos
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f'Servidor rodando no {HOST}:{PORT}')

# 2. Os arrays Clients e Usernames vão salvar os:
#  - Clientes que forem conectando no servidor
#  - Nome que o cliente escolheu ao se conectar
clients = []
usernames = []

# 3. Envia a mensagem para todos escutarem quando alguem se conectar no servidor
def broadcastMensagem(mensagem):
  for client in clients:
    client.send(mensagem)

# 4. Função que enviará mensagens
def handleMessages(client):
  while True:
    # 4.1 Enviara a mensagem que foi enviada por um cliente para todos os outros que estão conectador no chat
    try:
      receiveMensagemFromClient = client.recv(2048).decode('ascii')
      broadcastMensagem(f'{usernames[clients.index(client)]}:{receiveMensagemFromClient}'.encode('ascii'))

    # 4.2 Caso o cliente se desconecte será feito:
    # - A remoçao do cliente da lista de clientes ativos no Chat
    # - E enviado uma mensagem para todos os outros clientes que alguém saiu do chat
    except:
      clientClose = clients.index(client)
      client.close()
      clients.remove(clientClose)
      clientCloseUsername = usernames[clientClose]
      print(f'{clientCloseUsername} saiu do chart.')
      broadcastMensagem(f'{clientCloseUsername} saiu do chart'.encode('ascii'))
      usernames.remove(clientCloseUsername)

# 5. Inicia a conexão no servidor adicionando uma Thread a um novo cliente que deseja se conectar
def initialConnection():
  while True:
    try:
      client, address = server.accept()
      print(f"Nova conexão: {str(address)}")
      clients.append(client)
      client.send('getUser'.encode('ascii'))

      username = client.recv(2048).decode('ascii')
      usernames.append(username)

      broadcastMensagem(f'{username} Entrou no chat'.encode('ascii'))

      user_thread = threading.Thread(target=handleMessages, args=(client,))
      user_thread.start()
    except:
      pass
initialConnection()