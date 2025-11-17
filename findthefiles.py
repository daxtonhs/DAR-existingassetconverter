import os, mariadb, shutil


lookpath = "/home/datd-tech/Data/3d Models"

conn = mariadb.connect(
    user="assetrepo",
    password="RedR0cks%%",
    host="localhost",
    port=3306, 
    database="assets"
)

cur = conn.cursor()

thumbnailPath = os.path.join(lookpath, "thumbnails")

os.makedirs(thumbnailPath, exist_ok=True)


contents = os.listdir(lookpath)
for item in contents:
    print(item)
    fullpath = os.path.normpath(os.path.join(lookpath, item))
    if(os.path.isdir(fullpath)):
        assetName = os.path.basename(fullpath)

        files = os.listdir(fullpath)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        thumbnail = None
        if image_files:
            thumbnail = min(image_files)
        else:
            continue
        
        
        finalThumbnail = os.path.join(thumbnailPath, thumbnail)
        origThumbnail = os.path.join(fullpath, thumbnail)

        shutil.copyfile(origThumbnail, finalThumbnail) #copying thumbnail to thumbnail path

        fileCheckTags = {
            "Model": [".fbx", ".obj", ".stl", ".glb"],
            "Texture": ["texture","tex","t_map","map","diffuse","albedo","basecolor","normal","n_map","nm","bump","bump_map","roughness","r_map","gloss","gloss_map","metallic","metal","metal_map","specular","spec_map","emissive","emission","emit","self_illum","selfillum","height","hmap","displacement","disp","alpha","a_map","opacity","mask","ao","ambient_occlusion","occlusion"],
            "Normal": ["normal","n_map","normal_map","nm","nrm","bump","bump_map","tangent","tangent_space"],
            "Ambient Occlusion": ["ambient_occlusion","ao","ao_map","occlusion","ao_mask","ambient_occl","ambient_occl_map"],
            "Roughness": ["roughness","r_map","rough","roughness_map","rough_map","gloss","glossiness","gloss_map"],
            "Metallic": ["metallic","metalness","m_map","metal","metalness_map","metal_map","specular","spec_map"],
            "Alpha": ["alpha","a_map","opacity","mask_alpha","transparency","trans","opacity_map","cutout","mask","clip"],
            "Specular": ["spec", "specular", "gloss", "rough", "reflect", "metal"],
            "Emission": ["emissive","emission","emit","self_illum","selfillum","self_emission","em","e_map","em_map","illum","illumination","lightmap_emission","mask_emissive"],
            "Height": ["height","hmap","displacement","disp","d_map","heightmap","height_map","displace","elevation","zmap"],
            "Displacement": ["displacement","disp","d_map","displace","disp_map","displacement_map","subdiv","subdivision","tessellation","tess_map"],
            "Audio": [".mp3", ".wav", ".ogg", ".m4a"],
            ".obj": [".obj"],
            ".fbx": [".fbx"],
            ".gltf": [".gltf"],
            ".blend": [".blend"],
            ".ma": [".ma"],
            ".max": [".max"],
            ".usdz": [".usdz"],
            ".3ds": [".3ds"],
            ".dae": [".dae"],
            ".png": [".png"],
            ".jpg": [".jpg"],
            ".bmp": [".bmp"],
            ".hdr": [".hdr"],
            ".exr": [".exr"],
            ".pfm": [".pfm"],
            "HDRI": ["hdri","env","environment","envmap","env_map","sky","skybox","lighting","light_probe","lightprobe","panorama","panoramic","360","spherical","exr","hdr"]
        }

        tagsList = ["Asset"]

        for file in files:
            for tag in  fileCheckTags:
                for check in  fileCheckTags[tag]:
                    if(check in os.path.basename(file).lower() and tag not in tagsList):
                        tagsList.append(tag)

        #Minor post processing
        if("Model" in tagsList and "Texture" in tagsList):
            """Removing the texture tag from the object if it contains
            3D models as the textures always relate to the 3D model and
            will cause confusion when being marked as an object & texture
            """
            tagsList.remove("Texture") 

        tags = ','.join(tagsList)

        rootpath = os.path.dirname(fullpath)

        print("rp", rootpath, "fp", fullpath)

        shutil.make_archive(assetName, 'zip', root_dir=rootpath, base_dir=fullpath)

        title = assetName
        imagePath = finalThumbnail
        
        assetPath = fullpath + ".zip"

        print(tags, title, imagePath, assetPath)
        cur.execute(
            """
            insert into AssetList (Title, ImagePath, Tags, AssetPath)
            values (?, ?, ?, ?)
            """,
            (title, imagePath, tags, assetPath)
        )

conn.commit()

