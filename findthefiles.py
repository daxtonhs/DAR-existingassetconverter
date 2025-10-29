import os
import mariadb


lookpath = "/home/datd-tech/Data/3d Models"

conn = mariadb.connect(
    user="assetrepo",
    password="RedR0cks%%",
    host="localhost",
    port=3306, 
    database="assets"
)

cur = conn.cursor()

contents = os.listdir(lookpath)
for item in contents:
    print(item)
    fullpath = os.path.join(lookpath, item)
    if(os.path.isdir(fullpath)):
        assetName = os.path.basename(fullpath)

        files = os.listdir(fullpath)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        thumbnail = None
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
                    if(check in os.path.basename(file).lower() and tag not in tagsList):
                        tagsList.append(tag)

        tags = ','.join(tagsList)
        title = assetName
        imagePath = thumbnail if thumbnail else ""
        assetPath = fullpath

        print(tags, title, imagePath, assetPath)
        input()

        cur.execute(
            """
            insert into AssetList (Title, ImagePath, Tags, AssetPath)
            values (?, ?, ?, ?)
            """,
            (title, imagePath, tags, assetPath)
        )

conn.commit()

