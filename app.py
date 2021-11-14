import os

try:
    if os.environ['USERDOMAIN'] == 'DEZIO':
        print("Local Testing")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./keys/FbAdminConfig.json"
    else:
        raise ValueError("Not running on DEZIO")
except:
    print("Production")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./keys/dark-sensor-263608-firebase-adminsdk-2k627-a8d8040fe7.json"

if "PORT" in os.environ:
    PORT = os.environ["PORT"]
else:
    PORT = 8080

from flask import Flask, request

