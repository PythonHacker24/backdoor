//// Reading and Writing files in Python - Download and Upload function in backdoor ////

File Download : 

A file is a series of characters.

Therefore to transfer a file we need to: 

1. Read the file as a sequence of characters.
2. Send this sequence of characters.
3. Create a new empty file at destination.
4. Store the transferred sequence of characters in the new file.

//// Read file function

    def read_file(self, path):
        with open(path, "rb") as file:                                       # Read the file as binary
            return file.read()

//// Write file function

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(content)
            return "[+] Download successful."

//// Read file function with Base64 Encoding

    def read_file(self, path):  
        with open(path, "rb") as file:                                       # Read the file as binary
            return base64.b64encode(file.read())                             # Base64 encoding the file to avoid Bad characters in file that will throw error in json packing [UnicodeDecodeError]

//// Write file function with Base64 Decoding

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))                            # Base64 decode the data as the backdoor is going to encode it 
            return "[+] Download successful."

////
