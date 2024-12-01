import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

print(f"SECRET_KEY {SECRET_KEY}")
print(f"ALGORITHM {ALGORITHM}")
print(f"MONGO_URI {MONGO_URI}")
print(f"DB_NAME {DB_NAME}")
