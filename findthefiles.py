import os

lookpath = "/home/datd-tech/Data/3d Models"

contents = os.listdir(lookpath)
for item in contents:
    if(os.path.isdir(item)):
        assetName = os.path.basename(item)

        files = os.listdir(item)
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
                    if(check in os.path.basename(file) and tag not in tagsList):
                        tagsList.append(tag)

        print(tagsList)
        input()
