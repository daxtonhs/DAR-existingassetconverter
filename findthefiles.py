import os

lookpath = "/home/datd-tech/Data/3d Models"

contents = os.listdir(lookpath)
for item in contents:
    print(item)
    fullpath = os.path.join(lookpath, item)
    if(os.path.isdir(fullpath)):
        assetName = os.path.basename(fullpath)

        files = os.listdir(fullpath)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if image_files:
            thumbnail = min(image_files)
        else:
            continue

        tags = {
            "3D Model": [".fbx", ".obj", ".stl", ".glb"],
            "Normal": ["normal"],
            "Ambient Occlusion": ["ao", "ambient"],
            "Metallic": ["metallic"],
        }

        tagsList = ["Asset"]

        for file in files:
            for tag in tags:
                for check in tags[tag]:
                    print(check, os.path.basename(file).lower())
                    if(check in os.path.basename(file).lower() and tag not in tagsList):
                        tagsList.append(tag)

        print(tagsList)
        input()
