import random
import socket
import time
import threading
from bots import all_actions

# Empty array so that sometimes action2 is empty
empty_actions = [None]*(int(all_actions.__len__()/3))

action = random.choice(all_actions)
action2 = random.choice(all_actions + empty_actions)

# Lists which will contain information about connected clients and bots
clients = []
bots = []

# bots number of client which must be reached for dialogue to start
# Max 4
bots_nr = 4

# Creates TCP s socket
s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_socket.bind(("127.0.0.1", 24242))
s_socket.listen(bots_nr)



# Broadcasts message to all clients

def broadcast(message, sender=None):
    if type(message) == str:
        message = message.encode()

    for client in clients:
        if client != sender:
            client.send(message)
    time.sleep(0.3)


# Sends client a request for a botname
def add_Bots(client, address):
    client.send("USRNM".encode())
    # Client will check that botname is one of the valid names and send to server
    user = client.recv(1024).decode()

    # If bot hasn't already been initialised, add it
    if user not in bots:
        print(f"User: {user}\n")
        bots.append(user)
        clients.append(client)
        client.send("\nYou connected to the server".encode())
        broadcast(f"\n{user} joined the chat", client)
        time.sleep(0.3)
        if clients.__len__() < bots_nr:
            broadcast(f"there are now \n{clients.__len__()} clients connected."
                      f" Program will start when {bots_nr} are connected")

        else:
            broadcast(f"\n{clients.__len__()} clients connected. Program is starting...\n")
        time.sleep(0.5)

    # Else, close connection
    else:
        client.send("You are kicked out".encode())
        print(f"Duplicated user: {user}")
        print(f"Disconnecting from {str(address)}")
        client.close()



# Sends activity suggestion(s) and receives answers from bots
def send():
    if action2 == None:
        message = f"Host suggested: {action} "
    else:
        message = f"Host suggested: {action} or {action2}"

    for i in clients:
        i.send(message.encode())
    for i in clients:
        message = i.recv(1024)
        time.sleep(0.2)
        broadcast(message, i)


# "Main" function: listens for connections and starts chat when it is time
def start():
    # On the lookout for connections while the bot number isn't reached
    while clients.__len__() < bots_nr:
        try:
            # Establishing connection with client upon request
            client, address = s_socket.accept()
            print(f"Connected to {str(address)}")

            # Gets botname. If valid, adds client to a list of clients. Else, closes the connection
            add_Bots(client, address)
        except KeyboardInterrupt:
            print("\nthe rule 1 was to sey \"bye\"!!!. Everyone are kicked out.")
            s_socket.close()
            quit()


    # Starts chat when the bot number is reached
    if clients.__len__() == bots_nr:
        print("Bots_number reached!")

        try:
            # Starts message exchange on separate thread
            thread = threading.Thread(target=send)
            thread.start()
            thread.join()


        except:
            print ("Bye...")
            s_socket.close()
            quit()

print("Server is listening...")
# Effectively runs the servers
start()