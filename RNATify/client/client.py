
from socket import *
import sys
import os


def main():
    buffer_size = 8196
    host = gethostbyname(gethostname())
    port = 5000
    try:
        filename = sys.argv[0]
    except IndexError:
        print "list index out of range- no argv"
        filename = 'songs_Info.db'
    s = socket()
    s.connect((host, port))
    if filename != 'q':
        s.send(filename)
        data = s.recv(buffer_size)
        if data[:6] == 'EXISTS':
            file_size = long(data[6:])

            s.send("OK")
            if filename[0:13] == 'song_and_Data':
                filename = filename.split('\\')[-1]
            f = open(filename, 'wb')
            data = s.recv(buffer_size)
            total_receive = len(data)
            f.write(data)

            while total_receive < file_size:
                data = s.recv(buffer_size)
                total_receive += len(data)
                f.write(data)
                # print "{0:.2f}".format((total_receive / float(file_size)) * 100) + "% Done"
            print "Download Complete!"
            f.close()
        else:
            print "File Does Not Exist!"

    s.close()


if __name__ == '__main__':
    main()
