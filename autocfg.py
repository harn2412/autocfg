"""Chuong trinh ho tro thao tac cau hinh tu dong nhieu thiet bi"""
import scripts
import csv
import os
import shutil
from datetime import datetime


class Info:
    """Thong tin cua chuong trinh"""
    # Ten chuong trinh
    name = "Auto Configure Multi Devices"
    # Phien ban
    version = "beta 1"
    # Description
    description = "Chuong trinh ho tro cau hinh tu dong cho nhieu thiet bi dong thoi"


class Dirs:
    """Chua cac thu muc va duong dan tap tin"""
    # Thu muc cai dat
    install_dir = os.path.dirname(os.path.abspath(__file__))

    # Thu muc chua cac tap tin firmware
    scripts_dir = os.path.join(install_dir, "files", "firmware")

    # Thu muc chua cac tap tin sao luu cau hinh
    cfg_dir = os.path.join(install_dir, "files", "configuration")

    # Thu muc chua danh sach dia chi IP
    hosts_dir = os.path.join(install_dir, "hosts")


def when_start():
    """In mot vai thong tin khi chuong trinh khoi dong"""

    print(f"{'='*shutil.get_terminal_size()[0]}")
    print(Info.name)
    print(f"Version: {Info.version}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*shutil.get_terminal_size()[0]}")


def main():
    when_start()

    # Danh sach cac thiet bi muon thao tac
    hosts_file_name = input("Nhap vao ten danh sach cac thiet bi muon thao tac: ")
    hosts = []
    with open(os.path.join(Dirs.hosts_dir, hosts_file_name)) as hosts_file:
        file_reader = csv.DictReader(hosts_file)
        for row in file_reader:
            hosts.append(row)

    # Chon thao tac muon thuc hien
    print(
        "Vui long chon cac thao tac ban muon thuc hien: \n"
        "\t[1] - Nang cap Firmware\n"
        "\t[2] - Khoi phuc file cau hinh\n"
        "\t[3] - Khoi phuc cau hinh mac dinh"
    )

    while True:
        option = input("Tuy chon: ")

        if option == '1':
            print("Chuan bi tien hanh nang cap Firmware hang loat cho cac thiet bi...")
            action = "update_firmware"
        elif option == '2':
            print("Chuan bi tien hanh khoi phuc sao luu cau hinh hang loat cho cac thiet bi...")
            action = "restore_cfg"
        elif option == '3':
            print("Chuan bi tien hanh khoi phuc cau hinh mac dinh hang loat cho cac thiet bi...")
            action = "reset_default"
        else:
            action = None

        if action is not None:
            break

    for host in hosts:
        print(f"{'=' * shutil.get_terminal_size()[0]}")
        print(f"Chuan bi tien hanh nang cap firmware")

    for host in hosts:
        print(host.values())


main()
