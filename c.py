from jsonrpcclient import request, parse, Ok
import requests
import base64
import os

myFriends = list()
myFriends.append(5001)
myFriends.append(5002)


def sendPing():
    # send a request to the server
    print("what is the servers port?")
    
    portToCall = int(input())
    try:

         response = requests.post(f"http://localhost:{portToCall}/", json=request("ping"))
         parsed = parse(response.json())
         print(parsed.result)

    except:

         print(" ----- Are you sure that port and function exist?")

def sayHello(personName):
    # send a request to the server

    print("what is the servers port?")

    portToCall = int(input())

    try:
        response = requests.post(f"http://localhost:{portToCall}/", json=request("printName", params={"name": personName}) )

        parsed = parse(response.json())

        print(parsed.result)

    except:

        print(" ------ Are you sure that port and function exist?")
        
def mkFolder():
    print("What is the server's port?")
    portToCall = int(input())
    print("Enter folder name.")
    folderName = input().strip()
    
    if not folderName:
        folderName = "new_folder"    
    try:
        response = requests.post(f"http://localhost:{portToCall}/", json=request("makeFolder", params={"folder_name": folderName}) )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port exists?")

def delFolder():
    print("What is the server port?")
    portToCall = int(input())
    print("Enter folder name.")
    folderName = input().strip()
    
    try:
        response = requests.post(f"http://localhost:{portToCall}/", json=request("deleteFolder", params={"folder_name": folderName}) )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port exists?")

def askWhoAreYou():
    print("What is the server's port?")
    portToCall = int(input())

    try:
        response = requests.post(f"http://localhost:{portToCall}/", json=request("whatServer") )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port exists?")

def askVersion():
    print("What is the server's port?")
    portToCall = int(input())
    
    try:
        response = requests.post(f"http://localhost:{portToCall}/", json=request("getVersion") )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are your sure that port exists?")

def searchForFile():
    print("What is the server's port?")
    portToCall = int(input().strip())
    
    print("Enter the filename to search for: ")
    filename = input().strip()
    
    try: 
        response = requests.post(f"http://localhost:{portToCall}/", json=request("searchFile", params={"filename": filename}))
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port exists?")

def startNewServer():
    print("Enter server number to start: ")
    s_num = input().strip()

    print("Which server should handle this request?")
    portToCall = input().strip()

    try:
        response = requests.post(f"http://localhost:{portToCall}/", json=request("startUP", params={"server_num": s_num}))
        parsed = parse(response.json())
        print(parsed.result)
    except Exception as e:
        print("Are you sure that port exists?")

def notifyOnline():
    portToCall = input()
    for friend_port in myFriends:
        try:
            response = requests.post(f'http://localhost:{friend_port}/online', json={'port': portToCall})
            if response.status_code == 200:
                print(f"Notified server on port {friend_port} that client {portToCall} is online.")
        except Exception as e:
            print(f"Failed to notify server on port {friend_port}: {str(e)}")

def shutDownServer():

    print("Enter server number to shutdown: ")
    portToCall = input().strip()
    requests.post(f"http://localhost:{portToCall}/", json=request("shutDOWN"))
    
    # Notify friends that this client is going offline
    for friend_port in myFriends:
        try:
            response = requests.post(f'http://localhost:{friend_port}/offline', json={'port': current_port})
            if response.status_code == 200:
                print(f"Notified server on port {friend_port} that client {portToCall} is offline.")
        except Exception as e:
            print(f"Failed to notify server on port {friend_port}: {str(e)}")


print("Welcome!")

while True:
    print("please type a menu option")
    print("1. send ping")
    print("2. say hello")
    print("3. Make a folder")
    print("4. Delete a Folder")
    print("5. Who are you?")
    print("6. Get server Python Version")
    print("7. Search for a file")
    print("8. Start a new server")
    print("9. Shutdown the server")
    print("10. List Friends")
    print("11. Add Friend")
    print("12. Remove Friend")

    print("11. Notify Friends That You're Online")
    print("12. Notify Friends That You're Offline")


    option = input().strip()
    
    if option.isdigit():
        option = int(option)
    else:
        print("Invalid input")

    if option == 1:
        sendPing()
        
    elif option == 2:
        sayHello('john')
        
    elif option == 3:
        mkFolder()
        
    elif option == 4:
        delFolder()
    
    elif option == 5:
        askWhoAreYou()
    
    elif option == 6:
        askVersion()
    
    elif option == 7:
        searchForFile()
    
    elif option == 8:
        startNewServer()
    
    elif option == 9:
        shutDownServer()
    
    elif option == 10:
        list_friends()
    
    elif option == 11:
        notifyOnline()
