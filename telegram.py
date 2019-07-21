
# importing the requests library 
import requests
#import json to save message 
import json
#import to create directory
import os
import random
  
#return message with standard formate
def getMessage(token,semplify):
    # api-endpoint to send message, choose correctly your token
    URL = "https://api.telegram.org/bot"+ token + "/getUpdates"

    # sending get request and saving the response as response object 
    r = requests.get(url=URL) 
    
    # extracting data in json format 
    data = r.json() 

 
    #outpu is used to parse json and semplify data if it is necessary
    output = []

    if(semplify == True):
        #read all message from the GET result
        for message in data["result"]:
            #if message is standard (not an inline button, photo or video) choose this json pattern
            try:
                newMessage = {
                    "id": message["message"]["message_id"],
                    "text": message["message"]["text"],
                    "first_name": message["message"]["chat"]["first_name"],
                    "last_name": message["message"]["chat"]["last_name"],
                    "chatId": message["message"]["chat"]["id"],
                    "date": message["message"]["date"]
                }
                output.append(newMessage)
            except KeyError:  #if message is a button response choose this json pattern
                newMessage = {
                    "id": message["callback_query"]["message"]["message_id"],
                    "text": message["callback_query"]["data"],
                    "first_name": message["callback_query"]["from"]["first_name"],
                    "last_name": message["callback_query"]["from"]["last_name"],
                    "chatId": message["callback_query"]["from"]["id"],
                    "date": message["callback_query"]["message"]["date"]
                }
                output.append(newMessage)
            #TODO correctly catch all kind of message (video, gif image etc)
    else:
        output = data["result"]

    # return the output 
    return output


def saveDataJson(token,data):
    #open json and save message  in the data directory 
    fileName = "data/"+token
    try:
        #open the old message 
        with open(fileName +"/old.json") as json_file:  
            #message in the old.json
            oldData = json.load(json_file)
            #new message
            newData = []
            #filter with the new one to not create duplicate response
            for message in data:
                find = False
                
                #check if message exist in the old message
                for oldMessage in oldData:
                    if message["id"] == oldMessage["id"]:
                        find = True
                
                #if not exist, save  it in newData
                if not find:
                    #if not exist in the old.json, it is a new message, so server can response to it
                    print("[info] - Received new message! " + message["text"] + " from " + message["first_name"] + " " + message["last_name"])
                    newData.append(message)
        
        #save new message in the new.json
        with open(fileName +"/new.json", 'w') as outfile:  
            json.dump(newData, outfile, indent=4)       

    #if file not exists, create a new one
    except FileNotFoundError:
        with open(fileName +"/new.json", 'w') as outfile:  
            json.dump(data, outfile, indent=4)


def sendMessage(token,message):
    #load all new message from new.json
    fileName = "data/"+token
    try:
        with open(fileName +"/new.json") as json_file:  
            #json of new message
            data = json.load(json_file)
            #reply to all message
            for client in data:
                #send "typing" to bot to create a more human interaction
                URL = "https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+str(client["chatId"])+"&action=typing"
                requests.get(url=URL) 
                
                #check if exist a correct answer to the message
                found = False
                for mex in message:
                    if mex["key"] in client["text"].casefold():
                        messageToSend = mex["text"]
                        try:
                            inline = json.dumps(mex["inline"])
                        except KeyError:
                            inline = False
                        found = True
                
                #if not exist, reply with an automatic 404 message
                if not found:
                    inline = False
                    messageToSend = "Sorry we can't help you, try with another supported message"
    
                #if inline is null reply qith a simply message, and if it is nt null reply with a button answer
                if not inline :
                    URL = "https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+str(client["chatId"])+"&text="+messageToSend
                else:
                    URL = "https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+str(client["chatId"])+"&text="+messageToSend+"&reply_markup=" + inline
            
                
                # sending get request and saving the response as response object 
                r = requests.get(url=URL) 
                
                print("[info] - Send message:\""+messageToSend+"\" to " + client["first_name"] + " " + client["last_name"] )

            if len(data) > 0:
                try:
                    #open the old.json and save the add this messages
                    with open(fileName+"/old.json") as json_file:  
                        #message in the old.json
                        print("old.json already exist")
                        oldData = json.load(json_file)  
                        for client in oldData:
                            data.append(client)   
                except FileNotFoundError:
                    pass
                finally:
                    with open(fileName+"/old.json", 'w') as output:
                        json.dump(data, output, indent=4)   
    
                #delete the new.json becouse there isnt new message
                os.remove(fileName +"/new.json")

    except FileNotFoundError:
        print("[error] - File not found")

