# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    #Prepare a server socket
    serverSocket.bind(("", port))
    serverSocket.listen(1)

    while True:
        #Establish the connection
        #print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        try:

            try:
                message = connectionSocket.recv(1024)
                filename = message.split()[1]
                f = open(filename[1:])
                output = f.read().splitlines()
                f.close()

                headers = ['HTTP/1.1 200 OK\r\n', 'Connection: Close\r\n', 'Content-Encoding: UTF-8\r\n', 'Content-Type: text/html\r\n' '\r\n']
                output = headers + output


                #Send the content of the requested file to the client
                for i in range(0, len(output)):
                    connectionSocket.send(output[i].encode())

                connectionSocket.send("\r\n".encode())
                connectionSocket.close()
            except IOError:
                # Send response message for file not found (404)
                connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())
                connectionSocket.send('Connection: Close\r\n'.encode())
                connectionSocket.send('Content-Encoding: UTF-8\r\n'.encode())


                #Close client socket

                connectionSocket.send("\r\n".encode())
                connectionSocket.close()


        except (ConnectionResetError, BrokenPipeError):
            pass

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)
