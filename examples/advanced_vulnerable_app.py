import os
import pickle
import requests
import logging
import hashlib
import jwt

DEBUG = True

password = "123456"
token = "abc.def.ghi"

user_input = input("Enter your command: ")
eval(user_input)

os.system(user_input)

file_path = "../../etc/passwd"
open(file_path, "r")

url = "http://internal.api/" + user_input
requests.get(url)

data = pickle.loads(user_input)

hashed = hashlib.md5(password.encode()).hexdigest()

decoded = jwt.decode(token, options={"verify": False})

logging.info("Logging sensitive info: password=%s", password)
