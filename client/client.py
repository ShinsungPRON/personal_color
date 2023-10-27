# +-------------+--------------+-----------------------------------------------------------------+
# |   Author    |     Date     |                            Changed                              |
# +-------------+--------------+-----------------------------------------------------------------+
# |   Andrew A  |  2023/10/11  | Initial release                                                 |
# +-------------+--------------+-----------------------------------------------------------------+

import configparser
import socket
import json
import os
import io

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "conf.conf"))
data_path = os.path.join(os.path.dirname(__file__), "data.dat")


def send():
    # conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # conn.connect((config["DEFAULT"]["ServerAddr"], int(config["DEFAULT"]["ServerPort"])))
    #
    # with open(data_path, 'r') as f:
    #     dat = f.read().split("\n")
    #
    # data = json.dumps(
    #     {
    #         "ClientName": config['DEFAULT']['ClientName'],
    #         "data": {
    #             "CustomerName": dat[0],
    #             "ColorCode": dat[1]
    #         }
    #     },
    #     ensure_ascii=False
    # )
    #
    # conn.send(data.encode())
    pass


def update_name(name):
    with io.open(data_path, 'r', encoding='utf-8') as f:
        data = f.read().strip().split('\n')

    data[0] = name

    with io.open(data_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(data))


def update_color(color):
    with io.open(data_path, 'r', encoding='utf-8') as f:
        data = f.read().strip().split('\n')

    data[1] = color

    with io.open(data_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(data))


def get_chromebook_id():
    return config['DEFAULT']['ClientName']


def get_client_name():
    with io.open(data_path, 'r', encoding='utf-8') as f:
        data = f.read().strip().split("\n")

    return data[0]


if __name__ == '__main__':
    print(get_chromebook_id())
    print(get_client_name())