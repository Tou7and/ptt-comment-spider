import os
from glob import glob
from shutil import move

articles = glob("./data/article/*.txt")

good_dir = "data/article/good"
normal_dir = "data/article/normal"
bad_dir = "data/article/bad"

# os.mkdir(good_dir)
# os.mkdir(normal_dir)
# os.mkdir(bad_dir)

for article in articles:
    score = os.path.basename(article).replace(".txt", "").split("-")[1]
    # print(score)
    if "X" in score:
        move(article, bad_dir)
    elif "爆" in score:
        move(article, good_dir)
    else:
        score = int(score)
        if score > 30:
            move(article, good_dir)
        elif score > 5:
            move(article, normal_dir)
        else:
            move(article, bad_dir)

goods = glob(good_dir+"/*.txt")
normals = glob(normal_dir+"/*.txt")
bads = glob(bad_dir+"/*.txt")
print("goods: {}".format(len(goods)))
print("normals: {}".format(len(normals)))
print("bads: {}".format(len(bads)))

