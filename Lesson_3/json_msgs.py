import time

presence_msg = {
    "action": "presence",
    "time": time.time(),
    "type": "status",
    "user": {
        "account_name": "Avalon",
        "status": "I'm here!"
    }
}
response_200_msg = {
    "response": 200,
    "time": time.time(),
}
