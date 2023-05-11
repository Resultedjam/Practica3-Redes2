import socket
import pickle
from threading import Thread
import random

HOST = '127.0.0.1'
PORT = 5000
MAX_PLAYERS = 2


# Función que maneja la conexión con cada cliente
def handle_client(client_socket, player_id):
    print(f"Conexión establecida con jugador {player_id}")
    player = ("X" if player_id == 1 else "O")

    # Espera hasta que se conecten todos los jugadores
    while len(players) < MAX_PLAYERS:
        pass

    print("Todos los jugadores se han conectado. Iniciando el juego...")

    # Ciclo principal del juego
    while True:
        if player_id == 1:
            # Es el turno del jugador 1
            print("Esperando al jugador 1...")
            x_symbol_list = pickle.dumps(player.symbol_list)
            client_socket.send(x_symbol_list)
            player_coord = client_socket.recv(1024).decode("utf-8")
            player.edit_square(player_coord)

            # Si el jugador 1 gana o empata, termina el juego
            if player.did_win("X") or player.is_draw():
                break
        else:
            # Es el turno del jugador 2 (controlado por el servidor)
            print("Es el turno del jugador 2 (controlado por el servidor)")
            available_squares = player.available_squares()
            server_choice = random.choice(available_squares)
            print(f"El servidor escoge la casilla {server_choice}")
            player.edit_square(server_choice)

            # Si el jugador 2 (servidor) gana o empata, termina el juego
            if player.did_win("O") or player.is_draw():
                break

            # Envía el tablero actualizado al jugador 1
            x_symbol_list = pickle.dumps(player.symbol_list)
            client_socket.send(x_symbol_list)
            player_coord = client_socket.recv(1024).decode("utf-8")
            player.update_square(player_coord)

        # Si el juego no ha terminado, espera al siguiente turno
        player.draw_grid()

    # Muestra el resultado final del juego
    if player.did_win("X"):
        print(f"El jugador 1 gana!")
    elif player.did_win("O"):
        print(f"El jugador 2 (servidor) gana!")
    else:
        print(f"Empate!")

    # Cierra la conexión con el cliente
    client_socket.close()


# Inicializa el servidor y espera a que se conecten los clientes
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(MAX_PLAYERS)
print(f"Servidor iniciado en {HOST}:{PORT}. Esperando jugadores...")

# Inicializa la lista de jugadores conectados
players = []

# Espera a que se conecten los dos jugadores
while len(players) < MAX_PLAYERS:
    client_socket, client_address = s.accept()
    players.append(client_socket)
    Thread(target=handle_client, args=(client_socket, len(players))).start()

# Cierra el servidor cuando termina el juego
s.close()
