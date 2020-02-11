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
    install_dir = os.path.abspath(os.path.abspath(__file__))

    # Thu muc chua cac tap tin firmware
    scripts_dir = os.path.join(install_dir, "files", "firmware")

    # Thu muc chua cac tap tin sao luu cau hinh
    cfg_dir = os.path.join(install_dir, "files", "configuration")

    # Thu muc chua danh sach dia chi IP
    hosts_dir = os.path.join(install_dir, "hosts")


def main():
    print(f"{'='*shutil.get_terminal_size()[0]}")
    print(Info.name)
    print(f"Version: {Info.version}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*shutil.get_terminal_size()[0]}")


main()
