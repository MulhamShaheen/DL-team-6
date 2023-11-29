import os
import xmltodict


def xml_to_yolo(xml_dir: str, yolo_dir: str, class_mapping: dict):
    for filename in os.listdir(xml_dir):
        if filename.endswith(".xml"):
            with open(os.path.join(xml_dir, filename), 'r') as file:
                data = xmltodict.parse(file.read())

            img_width = int(data['annotation']['size']['width'])
            img_height = int(data['annotation']['size']['height'])

            yolo_txt_path = os.path.join(yolo_dir, filename.replace(".xml", ".txt"))

            with open(yolo_txt_path, 'w') as file:
                objects = data['annotation']['object']
                if type(objects) is not list:
                    objects = [objects]
                for obj in objects:
                    class_name = obj['name']
                    class_id = class_mapping.get(class_name)

                    if class_id is not None:
                        x_min = int(obj['bndbox']['xmin'])
                        y_min = int(obj['bndbox']['ymin'])
                        x_max = int(obj['bndbox']['xmax'])
                        y_max = int(obj['bndbox']['ymax'])

                        x_center = (x_min + x_max) / 2 / img_width
                        y_center = (y_min + y_max) / 2 / img_height
                        width = (x_max - x_min) / img_width
                        height = (y_max - y_min) / img_height

                        file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")


class_mapping = {
    'trafficlight': 0,
    'stop': 1,
    'crosswalk': 2,
    'speedlimit': 3,
}


input_dir = 'archive_xml/labels'
output_dir = 'archive_yolo/labels'

xml_to_yolo(input_dir, output_dir, class_mapping)