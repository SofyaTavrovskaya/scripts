import yaml
import sys


def create(file_open, file_write):
    with open(file_open) as file_open, open(file_write, 'w') as file_write:
        img = yaml.safe_load(file_open)
        for types in img:
            file_write.write(img[types].get('url') + '\n')


create(sys.argv[1], sys.argv[2])