import telegram
import schedule
import time
import os

#token bot
token = "xxxxx"
#create directory
try:
    # Create target Directory
    os.mkdir("data")
    print("[info] - Directory data Created ") 
except FileExistsError:
    print("[info] - Directory data already exist") 

try:
    # Create target Directory
    os.mkdir("data/"+token)
    print("[info] - Directory data Created ") 
except FileExistsError:
    print("[info] - Directory data already exist") 


def job(): 
    print("[info] - Get messages")
    data = telegram.getMessage(token,True)
    print("[info] - Save messages")
    telegram.saveDataJson(token,data)
    message = [
        {
            "key": "test",
            "text": "test passed",
        },
        {
            "key": "button",
            "text": "choose a button",
            "inline" : {
                "inline_keyboard":
                    [
                        [
                            {
                            "text": "button1",
                            "callback_data" : "pressed1"
                            }
                        ],
                        [
                            {
                            "text": "button2",
                            "callback_data" : "pressed2"
                            }
                        ]
                    ]
                }   
        },
        {
            "key": "pressed1",
            "text": "button 1 work",
        },
        {
            "key": "pressed2",
            "text": "button 2 work",
        }
    ]
    print("[info] - Reply to messages")
    telegram.sendMessage(token,message)


schedule.every(2).seconds.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)


