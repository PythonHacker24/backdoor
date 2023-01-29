//// TCP protocol working and problems that are faced while communication that has to be fixed in the backdoor program ////

The way that the TCP protocol works is in STREAM and not in MESSAGES. TCP protocol is like a pipe with water in it. The amount of data send depends by the server to the
client does not affect the client. 

For example : buffer size of listner is 1024 but the server sends 2000 bytes, then the client will accept 1024 bytes and tge remaining 976 bytes will be left in the pipe. After first 1024 bytes is recieved, and the listner wants to get more, it will get the further 1024 bytes into it.

Now the problem is when we sned a lot of data from the server, the client will not recieve the data as whole and may get broken down into pieces.

To avoid this, there are 3 methods.

1. Calculate the amount of data sent by the server in the server and add the amount of data in the begining of each stream of data sent. This will specify the client how much to expect from the server for the whole amount of data to be recieved at once.

For example : 2000 + " ALL THE REST OF THE DATA " //// Now the client knows that it has to recieve 2000 bytes of data and it will accept the 2000 bytes of data as a whole packet of information.

2. At the end of every message, add a tag to it. The client will keep collecting the data until the tag is detected in the message and will pack the data recieved as one single packet of information.

For example : " ALL THE REST OF THE DATA " + XXXX //// Now the client will read the data and at the point of tag [XXXX], the data will be considered as one single packet.

3. Serialization : Take the data and store it in one box (analogy). This box will be sent as whole. The client will recieve the box as a discrete element (How can someone accept half box!). This whole box will be opened by the client and the data is recieved.

//// Backdoor Serialization ////

Implementation : 

1. Json and Pickle are common solutions.
2. Json (Javascript Object Notation) is implemented in many programming languages.
3. Represents objects as text.
4. Widely used when transfering data between clients and servers. 

////

    def reliable_send(self, data):                                          # It will convert the data into json format and send it to desired location
        json_data = json.dumps(data)                                        # json.dumps encodes the data in json format
        self.connection.send(json_data)

    def reliable_receive(self):                                             # It will recieve the json format data and decode it to normal form of data
        json_data = self.connection.recv(1024)                               
        return json.loads(json_data)                                        # json.loads decodes the json data in normal format

//// Modification in the reliable_receive function

    def reliable_receive(self):                         
        while True:                                                          # Start a infinite loop
            json_data = ""                                                   # Initialize the variable json_data to a empty string
            try:                                                             # Try to run the given code
                json_data = json_data + self.connection.recv(1024)           # json_data + the recieved connection
                return json.loads(json_data)                                 # return the json_data value
            except ValueError:                                               # Except a ValueError occurs, execute the following code
                continue                                                     # continue to the code (In this case it will get back in the loop and whill try to recieve more data)

////

This is to eliminate the error that was going to occur when large amount of data is recieved and previous function of reliable_receive was used.
When a large amount of data is sent and recieved, the package is broken as 1024 is the limit and then, json.loads(json_data) will try to decode and it will fail.
The error thrown will be a ValueError and hence, we need to eliminate it by getting the package as whole.
To do this, we try to execute the json.loads(json_data) and as soon as we get a ValueError, we use exception to it by continuing to the further code (that is where function code ends and hence we go to the start as a while loops is implemented).
This allows the program to receive more data and hence the json_data will be now whole and then again it will be decoded and if successful, the value will be returned or the loop we go on until the ValueError is eliminated.

