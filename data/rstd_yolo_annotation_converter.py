import os
import csv
from PIL import Image



def get_image_size(images_path, csv_path, label_path):

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
            txt_f = open(label_path + yolo_txt_path, "a")
            data = f"{row[5][0]} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
            print(data)
            txt_f.write(data)
            txt_f.close()



get_image_size("rtsd-d1-frames/test/", "rtsd-d1-frames/full-gt.csv", "rtsd-d1-frames/test_labels/")