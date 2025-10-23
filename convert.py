import os

path = "/home/datd-tech/data"

folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

for folder in folders:
    print(folder)