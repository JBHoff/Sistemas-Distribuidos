import datetime

def timestamp():
    return datetime.datetime.now().isoformat() #2025-10-19T19:30:45.123456

def log(msg):
    print(f"[{timestamp()}] {msg}") #Util para debugging y auditoria