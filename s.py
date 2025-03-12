from jsonrpcserver import Success, method, serve
import sys
import os
import subprocess
import socket

if len(sys.argv) > 1:
    serverNumber = sys.argv[1]
else:
    print("sorry you forgot to add a server number... shutting down")
    quit()

myFriends = list()

@method
def ping():
    return Success("pong")

@method
def printName(name):

    return Success(f"hello {name}")

# method for making a folder
@method 
def makeFolder(folder_name):
    try:
        os.makedirs(folder_name, exist_ok=True)
        return Success(f"Folder successfully made. ^-^")
    except Exception as e:
        return Success(f"Failed to make folder : {str(e)}")

# method for deleting a folder
@method 
def deleteFolder(folder_name):
    try:
        os.rmdir(folder_name)
        return Success(f"Folder successfully removed. ^-^")
    except Exception as e:
        return Success(f"Failed to remove folder : {str(e)}")

# method for whoareyou - 
# The server should return with thier number e.g 1,2,3 
# and the port number they are running on
@method
def whatServer():
    return Success(f"Server number {serverNumber} running on port {5000 + int(serverNumber)}")


# method for get_version - Finding out what py ver is running on
@method
def getVersion():
    try:
        result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
        return Success(f"Python Version: {result.stdout}")
    except Exception as e:
        return Success(f"Failed to get Python Version : {str(e)}")

# method for search XXXXX - 
# The server should search for the filename the user has sent in the current directory
@method
def searchFile(filename):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return Success(f"File '{filename}' found in the directory.")
    else:
        return Success(f"File not found in the directory.")

# method for startup X - if X = 2, a new server should start on port 5002
@method
def startUP(server_num):
    try: 
        port = 5000 + int(server_num)
        
        subprocess.Popen(["python3", "server.py", str(server_num)])
        return Success(f"Server {server_num} started on port {port}")
    
    except Exception as e:
        return Success(f"Failed to start server: {str(e)}")
        
# method for shutdown X - A message should be sent to the server that is running on port X to shutdown, where X is the last number added to the port,  500X.
# This should also trigger an offline command as shown below.

# method for list_friends - The current server should return a list of port numbers it knows other servers are running on. 
# E.g., the server’s friends.

# method for online X - When this command is received by a server, the server should attempt to tell all the other servers it is now online and they should add this port to their list of friends.

# method for offline X - When this command is received by a server, it should tell all the other servers that the server on the defined port has shutdown and remove it from their list of friends.

# method for heartbeat - When a client sends this command to a server, the server should ping all its server friends and return the result to the client.

# method for pass msg X - msg is a text-based message.
# x is the server number we want to send the message to.
# When the client sends a pass command, it should go to the first server. If this server number does not match, it should pass the message on to the next server (one of his friends).
  
if __name__ == "__main__":

    print(f"server number {serverNumber} running.....")

    portNumber = '500' + serverNumber

    serve(port=int(portNumber))