import os
import shutil


def dataset_to_subset(dataset_path: str, set_name: str, start, size):
    img_dir = os.scandir(dataset_path + "/images")
    label_dir = list(os.scandir(dataset_path + "/labels"))

    os.makedirs(set_name)
    os.makedirs(set_name + "/images")
    os.makedirs(set_name + "/labels")

    for i, img in enumerate(img_dir, start=start):
        if i == start + size:
            break

        label = label_dir[i]

        shutil.copyfile(img.path, set_name + "/images/" + img.name)
        shutil.copyfile(label.path, set_name + "/labels/" + label.name)


dataset_to_subset("rsd_xml", "train", start=0, size=745)

