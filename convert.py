import os
from rapidfuzz import fuzz, process

path = "/home/datd-tech/Data/3d Models"

skipped = 0

folders = [os.path.join(path, f) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

#thank you chat gpt 
def find_thumbnail_for_model_dir(model_dir):
    dir_name = os.path.basename(model_dir)
    images = []

    for root, _, files in os.walk(model_dir):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                images.append(os.path.join(root, f))

    if not images:
        return None, 0

    best_match = process.extractOne(
        dir_name,
        images,
        scorer=lambda a, b: fuzz.ratio(os.path.splitext(os.path.basename(b))[0], a)
    )

    return best_match[0], best_match[1]


for folder in folders:

    thumbnail, score = find_thumbnail_for_model_dir(folder)

    if(thumbnail):
        print(thumbnail)
    else:
        skipped += 1

print(skipped)