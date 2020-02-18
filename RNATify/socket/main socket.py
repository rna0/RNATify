from socket import *
import thread
import sqlite3
import sys
import os


def return_file(sock):
    buffer_size = 8196
    filename = sock.recv(buffer_size)
    if os.path.isfile(filename):
        sock.send("EXISTS " + str(os.path.getsize(filename)))
        user_response = sock.recv(buffer_size)
        if user_response[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytes_to_send = f.read(buffer_size)
                sock.send(bytes_to_send)
                while bytes_to_send != "":
                    bytes_to_send = f.read(buffer_size)
                    sock.send(bytes_to_send)
    else:
        sock.send("ERR ")

    sock.close()


def main_song_transfer(port):
    serversock.listen(2)
    host = ''

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))

    s.listen(5)

    print "Server Started."
    while True:
        c, address = s.accept()
        print "client connected ip: <" + str(address) + ">"

        thread.start_new_thread(return_file, (c,))

    s.close()


def hendler(clientsock, addr):
    while 1:
        data = clientsock.recv(BUFSIZ)
        connection = sqlite3.connect("login.db")
        print data
        if not data:
            print 'END OF MESSAGE'
            break

        elif data[0:5] == 'CHECK':
            print 'checking username valid'
            username = data.split(' ')[1]
            result = connection.execute("SELECT * FROM USERS WHERE USERNAME = ?",
                                        (username,))

            if len(result.fetchall()) > 0:
                clientsock.send("True")
            else:
                clientsock.send("False")

        elif data[0:6] == 'CREATE':
            print 'adding to login.db'
            username, password, email = data.split(' ')[1], data.split(' ')[3], data.split(' ')[5]

            connection.execute("INSERT INTO USERS (USERNAME, EMAIL, PASSWORD, MONEY)"
                               " VALUES (?,?,?,?)", (username, email, password, '0.00'))
            connection.commit()
            clientsock.send("True")

        elif data[0:8] == 'USERNAME':
            print 'checking to get user'
            username, password = data.split(' ')[1], data.split(' ')[3]
            result = connection.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?",
                                        (username, password))

            if len(result.fetchall()) > 0:
                clientsock.send("True")
            else:
                clientsock.send("False")

        elif data == 'SONG_TRANSFER':
            thread.start_new_thread(main_song_transfer, (5000,))
            clientsock.send("ok")

        elif data[0:8] == 'GETMONEY':
            print 'giving back amount of money in bank'
            username = data.split(' ')[1]
            result = connection.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))

            clientsock.send(result.fetchall()[0][-1])

        elif data[0:8] == 'SETMONEY':
            print 'setting amount of money in bank'
            money, username = data.split(' ')[1], data.split(' ')[3]
            print money
            connection.execute("UPDATE USERS SET MONEY = ? WHERE USERNAME = ?", (money, username))
            connection.commit()

            clientsock.send('ok')

        else:
            print 'error'
        connection.close()

    clientsock.close()


HOST = ''
PORT = 51421
BUFSIZ = 1024
ADDR = (HOST, PORT)
serversock = socket(AF_INET, SOCK_STREAM)
serversock.bind(ADDR)
serversock.listen(2)

while 1:
    print 'wating for connection'
    clientsock, addr = serversock.accept()
    print 'connection from', addr
    thread.start_new_thread(hendler, (clientsock, addr))
serversock.close()
