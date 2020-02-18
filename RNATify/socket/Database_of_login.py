import sqlite3


def createTable():
    connection = sqlite3.connect('login.db')

    connection.execute("CREATE TABLE USERS(USERNAME TEXT NOT NULL,EMAIL TEXT,PASSWORD TEXT,MONEY TEXT)")

    connection.execute("INSERT INTO USERS VALUES(?,?,?,?)",
                       ('client', 'tcpclientsock@gmail.com', 'serverclient', '0.00'))

    connection.commit()

    result = connection.execute("SELECT * FROM USERS")

    for data in result:
        print("Username : ", data[0])
        print("Email : ", data[1])
        print("Password :", data[2])

    connection.close()


if __name__ == '__main__':
    createTable()
