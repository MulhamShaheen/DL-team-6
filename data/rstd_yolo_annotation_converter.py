import os
import csv
from PIL import Image
import shutil


def create_yolo_labels(images_path, csv_path, label_path):
    with open(csv_path) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            file_name = row[0]
            image_path = images_path + file_name
            if not os.path.exists(image_path):
                continue
            img = Image.open(images_path + file_name)
            img_width, img_height = img.size

            x_min = int(row[1])
            y_min = int(row[2])
            x_max = x_min + int(row[3])
            y_max = y_min + int(row[4])

            x_center = (x_min + x_max) / 2 / img_width
            y_center = (y_min + y_max) / 2 / img_height

            width = (x_max - x_min) / img_width
            height = (y_max - y_min) / img_height

            yolo_txt_path = file_name.replace(".jpg", ".txt")

            if os.path.exists(label_path + yolo_txt_path):
                data = f"\n{int(row[-1])} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
            else:
                data = f"{int(row[-1])} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
            txt_f = open(label_path + yolo_txt_path, "a+")
            print(data)
            txt_f.write(data)
            txt_f.close()


# get_image_size("E:/AI Talent Hub/Deep Learning/Traffic Signs Data/rtsd-public/detection/rtsd-d3-frames/rtsd-d3-frames/rtsd-d3-frames/test/",
#                "E:/AI Talent Hub/Deep Learning/Traffic Signs Data/rtsd-public/detection/rtsd-d3-gt/test.csv",
#                "rtsd_detection/test/labels/")

def copy_images(images_path, output, filenames):
    f = open(filenames, "r")
    reader = csv.reader(f)
    for line in reader:
        src = line[0].strip()
        shutil.copyfile(images_path + src, output + src)


# copy_images("E:/AI Talent Hub/Deep Learning/Traffic Signs Data/rtsd-public/detection/rtsd-d3-frames/rtsd-d3-frames/rtsd-d3-frames/train/",
#             "rtsd_detection/train/images/",
#             "E:/AI Talent Hub/Deep Learning/Traffic Signs Data/rtsd-public/detection/rtsd-d3-gt/train.csv")


def validate_dataset(images, labels):
    dir_labels = os.scandir(labels)
    count = 0
    for f in dir_labels:
        target = f.name.replace(".jpg", ".txt")
        if not os.path.exists(images+target):
            print(target)
            print(++count)


validate_dataset("rtsd_detection/test/labels/", "rtsd_detection/test/images/")