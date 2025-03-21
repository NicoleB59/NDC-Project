from ast import parse
import threading
from jsonrpcserver import Success, method, serve
import sys
import os
import subprocess
import socket

import requests

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
        port = 5000 + int(server_num)  # Determine port number
        os.system(f"start cmd /k python {sys.argv[0]} {server_num}")  # Start new server
        print("Server started up!")
        return Success(f"Server {server_num} started on port {port}")
    except Exception as e:
        return Success(f"Failed to start server: {str(e)}")
        
# method for shutdown X - A message should be sent to the server that is running on port X to shutdown, where X is the last number added to the port,  500X.
# This should also trigger an offline command as shown below.
@method
def shutDOWN():
    try:
        print("Shutdown.")
        os._exit(0) # terminates the whole program
    except Exception as e:
        return Success(f"Server failed to shutdown...  >:(")
    

# method for list_friends - The current server should return a list of port numbers it knows other servers are running on. 
# E.g., the server’s friends.
@method
def list_friends():
    return Success(myFriends)

# method for online X - When this command is received by a server, the server should attempt to tell all the other servers it is now online and they should add this port to their list of friends.
@method
def online(port):
    new_friend = f"{port}"
    if new_friend not in myFriends:
        myFriends.append(new_friend)  # Add to friends list
        # Notify all other friends about the new server
        for friend in myFriends:
            if friend != new_friend:  # Avoid notifying the server that just came online
                try:
                    requests.post(f"http://localhost:{friend}/", json=requests.request("online", {"port": port}))
                except Exception:
                    continue
    return Success(f"Server on port {new_friend} is now online")

    
# method for offline X - When this command is received by a server, it should tell all the other servers that the server on the defined port has shutdown and remove it from their list of friends.
@method
def offline(port):
    if port in myFriends:
        myFriends.remove(port)
    return Success(f"Server {port} removed from friends list!!")

@method
def offline(port):
    if port in myFriends:
        myFriends.remove(port)
        return Success(f"Server {port} removed from friends list. Current friends: {myFriends}")
    return Success(f"Server {port} was not in the friends list.")

# method for heartbeat - When a client sends this command to a server, the server should ping all its server friends and return the result to the client.
@method
def heartbeat():
    results = {}
    for friend in myFriends:
        try:
            response = requests.post(f"http://localhost:{friend}/", json=requests.request("ping"))
            parsed = parse(response.json())
            results[friend] = parsed.result
        except:
            results[friend] = "offline"
    return Success(results)

# method for pass msg X - msg is a text-based message.
# x is the server number we want to send the message to.
# When the client sends a pass command, it should go to the first server. If this server number does not match, it should pass the message on to the next server (one of his friends).
@method
def pass_msg(server_num, message):
    if int(server_num) == int(serverNumber):
        return Success(f"Message received: {message}")
    
    for friend in myFriends:
        try:
            response = requests.post(f"http://localhost:{friend}/", json=request("pass_msg", params={"server_num": server_num, "message": message}))
            parsed = parse(response.json())
            return parsed.result
        except:
            pass
    return Success("Message could not be delivered.")
  
if __name__ == "__main__":

    print(f"server number {serverNumber} running.....")
    
    portNumber = '500' + serverNumber
    
    serve(port=int(portNumber))

# it gives this error OverflowError: bind(): port must be 0-65535. basically means that the port is too big.
   