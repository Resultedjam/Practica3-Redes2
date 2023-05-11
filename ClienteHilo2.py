import socket
import pickle

# Dirección IP y puerto del servidor
HOST = '127.0.0.1'
PORT = 5002

# Creamos el socket y nos conectamos al servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Bucle para iniciar y jugar el juego
play_again = True
while play_again:
    # Recibimos los datos de la tabla de símbolos y los convertimos a una lista
    symbol_list = s.recv(1024)
    symbol_list = pickle.loads(symbol_list)
    print("Tablero actual:")
    print(f"{symbol_list[0]} | {symbol_list[1]} | {symbol_list[2]}")
    print(f"{symbol_list[3]} | {symbol_list[4]} | {symbol_list[5]}")
    print(f"{symbol_list[6]} | {symbol_list[7]} | {symbol_list[8]}")

    # Preguntamos al usuario para introducir sus coordenadas
    player_coord = input("Introduce las coordenadas: ")
    player_coord = player_coord.upper()

    # Enviamos los datos al servidor
    player_coord = pickle.dumps(player_coord)
    s.send(player_coord)

    # Recibimos los datos actualizados de la tabla de símbolos del servidor
    symbol_list = s.recv(1024)
    symbol_list = pickle.loads(symbol_list)
    print("Tablero actualizado:")
    print(f"{symbol_list[0]} | {symbol_list[1]} | {symbol_list[2]}")
    print(f"{symbol_list[3]} | {symbol_list[4]} | {symbol_list[5]}")
    print(f"{symbol_list[6]} | {symbol_list[7]} | {symbol_list[8]}")

    # Preguntamos al usuario si quiere volver a jugar
    play_again = input("Quieres jugar otra vez? (Y/N)").lower() == 'y'

# Cerramos la conexión del socket
s.close()
print("Gracias por jugar!")
