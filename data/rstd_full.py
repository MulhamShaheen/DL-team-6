import os
import csv
from PIL import Image

CLASS_DICT = {
    "blue_border": 0,
    "blue_rect": 1,
    "danger": 2,
    "main_road": 3,
    "mandatory": 4,
    "prohibitory": 5,
}


def copy_csv_files(path):
    root = os.scandir(path)
    test_writer = csv.writer(open(path + "test.csv", "w", newline=''))
    train_writer = csv.writer(open(path + "train.csv", "w", newline=''))
    for folder in root:
        if os.path.isfile(folder):
            continue
        files = os.scandir(folder.path)
        for t in files:
            f = open(t, "r")
            reader = csv.reader(f)

            for i, line in enumerate(reader):
                line.append(folder.name.split("-")[0])
                line.append(CLASS_DICT[folder.name.split("-")[0]])
                if i == 0:
                    continue
                if "test" in f.name:
                    test_writer.writerow(line)

                if "train" in f.name:
                    train_writer.writerow(line)


def rtsd_full_normalizer(csv_path, output_csv):
    output_file = open(output_csv, "w", newline="")
    writer = csv.writer(output_file)
    count_dict = {

    }
    with open(csv_path) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            # class_name = row[5].split("_")[0] + "_" + row[5].split("_")[1]
            class_name = row[5]

            if class_name not in count_dict.keys():
                count_dict[class_name] = 1
            else:
                if count_dict[class_name] == 500:
                    continue
                count_dict[class_name] += 1

            print(row)
            writer.writerow(row)


    output_file.close()
    print(count_dict)


rtsd_full_normalizer("full-frames/full-gt.csv", "full-frames/normalized.csv")
