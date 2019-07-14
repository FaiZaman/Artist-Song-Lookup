from socket import *
import pprint
import datetime
import sys

# opening, reading, and closing the file

file = open("../Test text file/100worst.txt", "r")
next_line = False
song_info = {}

def add_song(artist): # adds a song with one artist to the dict
    if artist in song_info.keys():          # check if artist already exists in dict
        song_info[artist] = song_info[artist] + ", " + song     # add on to existing artist's songs
    else:
        song_info[artist] = song
        
def add_song_two_artists(artist): # adds a song with two artists to the dictionary
    artist = artist.split("/")
    artist1 = artist[0].strip()
    artist2 = artist[1].strip() # split the artists
    if artist1 in song_info.keys():
        song_info[artist1] = song_info[artist1] + ", " + song # add first artist's song to dict
    else:
        song_info[artist1] = song
    if artist2 in song_info:
        song_info[artist2] = song_info[artist2].append(song) # add second artist's song to dict
    else:
        song_info[artist2] = song

for line in file: # loop through each line in the file
    if next_line == False: # if we want to skip to the next line because of long song title
        if line != "\n" and "-" in line[:4] and not line.startswith("X"): # check if the line is not blank and contains a song
            year = line[64:]
            artist = line[35:64].strip().lower()
            if line[0] == "3":
                song = "Tie A Yellow Ribbon"
                artist1 = "dawn"
                artist2 = "tony orlando"
                song_info[artist1] = song
                song_info[artist2] = song
            elif "/" in artist: # if song on one line and has two artists
                song = line[4:34].strip()
                add_song_two_artists(artist)
            elif year == "": # if song on two lines with one artist
                song = line[4:].strip()
                next_line = True
            else: # if a normal song (one line with one artist)
                song = line[4:34].strip()
                add_song(artist)
    else: # if skipped line (meaning long song title)
        artist = line[35:64].strip().lower()
        if "/" in artist: # if song covers two line with one artist
            add_song_two_artists(artist)
            next_line = False
        else:
            add_song(artist)
            next_line = False

print(song_info)
file.close()

# creating server log
server_log = open("../Log files/server.log.txt", "a")
server_log.write("==============================================================" + '\n\n')

# setting up and establishing server connection
server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)

try:
    server_socket.bind(('', server_port))
except OSError:
    print("Port " + str(server_port) + " is unavaliable. Please close all other server instances and/or try again later.") # if port is busy/unavaliable
    server_log.write("Connection unsuccessful" + '\n\n')
    server_log.close()
    sys.exit()
else:
    server_socket.listen(1)

# adding to logs
now = datetime.datetime.now()
server_log.write("Server started at: " + str(now.strftime('%I:%M:%S %p on %d/%m/%Y')) + '\n\n')
print("The server is ready to receive requests")

msg = "continue"
continuing = False
socket_connection = None

while True:
    # receiving client's request
    if continuing is False:
        server_log = open("../Log files/server.log.txt", "a")
        socket_connection, addr = server_socket.accept()
        start = datetime.datetime.now()
        server_log.write("Client request received at: " + str(start.strftime('%I:%M:%S %p on %d/%m/%Y')) + '\n\n')
        server_log.write("Connection successful" + '\n\n')
    else:
        new_start = datetime.datetime.now()
        server_log.write("New client request received at: " + str(new_start.strftime('%I:%M:%S %p on %d/%m/%Y')) + '\n\n')

    # receive artist name and retrieve their songs
    artist = socket_connection.recv(1024).decode().lower()
    server_log.write("Received artist name: " + artist + '\n\n')
    songs = song_info.get(artist)

    if songs is None:   # if artist does not exist in the input file
        error_message = "The artist " + "'" + artist + "'" + " does not exist. Please try again and enter a valid artist."
        socket_connection.send(error_message.encode())
    else:   # send the songs back to client
        socket_connection.send(songs.encode())

    # checking if user wants to continue choosing artists
    msg = socket_connection.recv(1024).decode()
    if msg == "continue":
        continuing = True
    else:
        continuing = False
        end = datetime.datetime.now()
        duration = end - start

        server_log.write("Duration for which server was connected to client: "
                         + str(duration)[:10] + '\n\n')
        server_log.close()
