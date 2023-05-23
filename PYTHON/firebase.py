import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class CloudData:
    def __init__(self, reference):
        cred_obj = credentials.Certificate(
            "F:\Fight land slide\CODE\Github\SERVER\landslide-predict-firebase-adminsdk-xe9ri-b4a5498257.json"
        )

        self.default_app = firebase_admin.initialize_app(
            cred_obj,
            {"databaseURL": "https://landslide-predict-default-rtdb.firebaseio.com/"},
        )
        self.ref = db.reference(reference)

    def upload(self, Input, Color, Time):
        data = {
            "realtime_data": {
                "node": {
                    "r": Input[0],
                    "m": Input[1],
                    "x": Input[2],
                    "y": Input[3],
                    "z": Input[4],
                    "color": Color,
                    "time": Time,
                },
            }
        }
        self.ref.set(data)


# import json
# with open("book_info.json", "r") as f:
# file_contents = json.load(f
