import os

print(os.listdir())

if "user.json" in os.listdir():
    print("FOUND")