import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "darkpatternDB"

DEFAULT_CSV = os.path.join(BASE_DIR, "online_shoppers_intention.csv")