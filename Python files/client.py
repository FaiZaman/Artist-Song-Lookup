from socket import *
import datetime
import sys

# creating log file
client_log = open("../Log files/client.log.txt", "a")

# setting up to connect to server
server_name = "127.0.0.1"
server_port = 12000
client_socket = socket(AF_INET, SOCK_STREAM)

# connecting to server and requesting artist
try:
    client_socket.connect((server_name, server_port))
except ConnectionRefusedError:  # if server is not running or port number is busy
    print("Server not found/port " + str(server_port)
          + " is busy. Please run the server and try again.")
    client_log.close()
    sys.exit()

client_log.write("=======================================================" + '\n\n')

disconnected = False

while disconnected is False:    
    artist = input("Enter an artist's name to see their songs: ")

    # validate non-blank artist and send request to server
    while artist == "":
        print("Please try again with a non blank artist name.")
        artist = input("Enter an artist's name to see their songs: ")
    client_socket.send(artist.encode())
    start = datetime.datetime.now()

    # receiving songs and exiting if timeout
    try:
        songs = client_socket.recv(1024)
    except TimeoutError:
        print("The connection timed out. Please try again")
        sys.exit()
        
    print('From server:', songs.decode())
    end = datetime.datetime.now()
    response_time = end - start

    # adding to logs and returning songs to user
    client_log.write("Server response received at: "
                     + str(end.strftime('%I:%M:%S %p on %d/%m/%Y') + '\n\n'))

    client_log.write("Time taken to receive a response from the server for"
                     + '\n' + "the request to get songs for "
                     + str(artist) + ": " + str(response_time) + '\n\n')

    client_log.write("The response length was " + str(len(songs)) + " bytes" + '\n\n')
    
    # prompting user to disconnect from server and confirming connection closure
    msg = str(input("Enter 'continue' to choose another artist, or 'quit' to disconnect from the server: "))

    if msg == "continue":
        client_socket.send(msg.encode())
    elif msg == "quit":
        disconnected = True
    else:
        print("Please enter a valid command")

client_log.close()
client_socket.close()
print("You have disconnected from the server.")
