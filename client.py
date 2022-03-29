import socket, sys
import time
from bots import act_Bot

bot_name = ["Alex", "Eli", "Nina", "Livia"]


# Check if the input  is a valid value
def valid_bot(inp):
    while inp == None or inp.lower().capitalize() not in bot_name:
        print(
        f"Please choose a bot: \"{bot_name[0]}\", \"{bot_name[1]}\", \"{bot_name[2]}\""
        f" or \"{bot_name[3]}\". Do not include quotation marks.")

        inp = input("Bot Name: ")
    return inp.lower().capitalize()


# Checks if bot was inserted and confirms validity
try:
    tmp_bot = sys.argv[3]
except:
    tmp_bot = None
    bot = valid_bot(tmp_bot)


# Creates a tcp client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 24242))

# "Main" read function

def read():
    # Continuously listens for messages from the server
    while True:
        try:
            message = client.recv(1024).decode()

            # When the request for the botname comes, send botname
            if message == "USRNM":
                print(f'You choosed : {bot} ')
                client.send(bot.encode())


            # When the prompt-message from the Host comes, bot start answering
            elif message.startswith(f"Host suggested: "):
                words = message.split(' ')
                activity = words[2]
                try:
                    activity2 = words[4]
                except:
                    activity2 = None
                print(message)
                bot_msg = act_Bot(bot, activity, activity2)
                print(f"You said: {bot_msg}")
                time.sleep(2)
                client.send(f"{bot} said: {bot_msg}".encode())
                print("is Sent")


            # Handles being kicked out by the server, when two client choose the same bot
            elif message == "\nYou are kicked out":
                print(message)
                print("Bye...")
                client.close()
                quit()

            # Prints any non-empty messages that do not meet the previous conditions
            elif message != "":
                print(message)

        except:
            client.close()
            quit()
            break

read()