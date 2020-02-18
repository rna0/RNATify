import sqlite3
import os


def search_files():
    song_files, jpg_files = [], []
    directory = "song_and_Data\Mozart", "song_and_Data\songs_no_copy_right", \
                "song_and_Data\Chopin"

    for path in directory:
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith((path, ".mp3")):
                    song_files.append(os.path.join(root, name))
                if name.endswith((path, ".jpg")):
                    jpg_files.append(os.path.join(root, name))
    return song_files, jpg_files


def set_values(names):
    artist, title, album = [], [], []
    for name in names:
        temp = name[:-4].split('\\')
        artist.append(temp[-1:][0].split(' - ')[0])
        title.append(temp[-1:][0].split(' - ')[1])
        album.append(temp[1])
    return title, artist, album


def create_table():
    connection = sqlite3.connect('songs_Info.db')
    connection.execute("CREATE TABLE SONGS(Title TEXT NOT NULL,Artist TEXT,Album TEXT,Cover TEXT)")

    names, cover = search_files()
    title, artist, album = set_values(names)

    for i in range(0, len(names)):
        connection.execute("INSERT INTO SONGS VALUES(?,?,?,?)", (title[i], artist[i], album[i], cover[i]))

    connection.commit()

    result = connection.execute("SELECT * FROM SONGS")

    for data in result:
        print("title : ", data[0])
        print("artist : ", data[1])
        print("album :", data[2])

    connection.close()


create_table()
