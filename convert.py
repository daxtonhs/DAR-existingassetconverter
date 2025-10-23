import os

path = "/home/datd-tech/Data/3d Models"

skipped = 0

folders = [os.path.join(path, f) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

for folder in folders:

    print(folder)

    allowed_ext = ["jpg", "png"]

    images = [image for image in os.listdir(folder) if image.split(".")[-1] in allowed_ext]

    if(len(images) > 0):
        thumbnail = max((os.path.join(folder, f) for f in images), key=os.path.getsize)
        print(thumbnail)
    else:
        skipped += 1