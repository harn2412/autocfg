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
    fw_dir = os.path.join(install_dir, "files", "firmware")

    # Thu muc chua cac tap tin sao luu cau hinh
    cfg_dir = os.path.join(install_dir, "files", "configuration")

    # Thu muc chua danh sach dia chi IP
    hosts_dir = os.path.join(install_dir, "hosts")


def when_start():
    """In mot vai thong tin khi chuong trinh khoi dong"""

    print(f"{'=' * shutil.get_terminal_size()[0]}")
    print(Info.name)
    print(f"Version: {Info.version}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * shutil.get_terminal_size()[0]}")


def when_end(success_list, false_list):
    """In mot vai thong tin sau khi chuong trinh hoat dong"""
    print(f"{'=' * shutil.get_terminal_size()[0]}")
    print("Da hoan thanh cong viec")
    print(f"Thanh cong: {len(success_list)}")
    print(f"That bai: {len(false_list)}")
    print(f"{'=' * shutil.get_terminal_size()[0]}")

    more_detail = input("Ban co muon xem chi tiet (y/n): ") or False
    if more_detail == "y":
        print(f"{'=' * shutil.get_terminal_size()[0]}")
        print("Danh sach thiet bi thanh cong:")
        for i, host in enumerate(success_list, 1):
            print(f"{i} - {host}")

        print(f"{'=' * shutil.get_terminal_size()[0]}")
        print("Danh sach thiet bi that bai:")
        for i, host in enumerate(false_list, 1):
            print(f"{i} - {host}")

    print(f"{'=' * shutil.get_terminal_size()[0]}")
    input("Nhan Enter de thoat chuong trinh")


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

        if option == "1":
            action_code = "update_firmware"
            action_title = "Nang Cap Firmware"
        elif option == "2":
            action_code = "restore_cfg"
            action_title = "Khoi Phuc Sao Luu Cau Hinh"
        elif option == "3":
            action_code = "reset_default"
            action_title = "Khoi Phuc Cau Hinh Mac Dinh"
        else:
            action_code = None
            action_title = None

        if action_code is not None:
            break

    print(f'Chuan bi tien hanh "{action_title}" hang loat cho cac thiet bi...')

    # Bien duoc chuan bi de luu du lieu file Firmware hoac file sao luu cau hinh
    temp_files = {}

    # Danh sach cac thiet bi thanh cong
    success_list = []

    # Danh sach cho cac thiet bi that bai
    false_list = []

    for host in hosts:
        print(f"{'=' * shutil.get_terminal_size()[0]}")
        print(f"Device Name: {host['device_name']}")
        print(f"Address: {host['addr']}")

        # Lay cac thong tin co ban
        host_info = {
            "addr": host["addr"],
            "user": host["user"],
            "password": host["password"],
        }

        # Kiem tra xem cong viec co can den file du lieu khong
        need_file_actions = {
            "update_firmware": Dirs.fw_dir,
            "restore_cfg": Dirs.cfg_dir,
        }

        if action_code in need_file_actions.keys():
            while True:
                # Qua trinh khai bao file du lieu can thiet cho cong viec
                parent_file_dir = need_file_actions[action_code]

                # B1: Thu xem co thong tin file trong co so du lieu khong?
                if host[action_code]:
                    file_path = os.path.join(parent_file_dir, host[action_code])

                    if not os.path.exists(file_path):
                        print("File duoc khai bao khong ton tai")
                    else:
                        break

                # B2: Kiem tra xem trong danh sach file tam co khai bao chua
                device_info = (
                    host["manufactory"],
                    host["model"],
                )

                if device_info in temp_files.keys():
                    print(
                        "Tien hanh su dung file da duoc khai bao truoc do trong danh sach tam"
                    )
                    file_path = temp_files[device_info]
                    break

                # B3: Trong truong hop danh sach tam chua co file thi tien hanh khai bao bang tay
                while True:
                    file_name = input("Vui long nhap vao ten file muon su dung: ")
                    file_path = os.path.join(parent_file_dir, file_name)

                    if not os.path.exists(file_path):
                        print("Tap tin khong ton tai vui long kiem tra lai")
                        continue
                    else:
                        add_to_temp = (
                            input(
                                "Ban co muon su dung file nay lam mac dinh cho cac thiet bi cung loai khong (y/n)?"
                            )
                            or False
                        )

                        if add_to_temp == "y":
                            temp_files[device_info] = file_path
                    break

                break

            # Them duong dan file vao danh sach thong so can khai bao
            host_info["file_path"] = file_path

            print(f"File duoc su dung la: {file_path}")

        # Lay script tuong ung voi thiet bi
        # Chon nha san xuat
        try:
            manufactory = getattr(scripts, host["manufactory"])
        except AttributeError:
            print("Khong tim thay nha san xuat nay\n" "Tien hanh bo qua ...")
            continue

        # Lay danh sach script tuong ung voi model
        try:
            scripts_name = manufactory.index[host["model"]]
        except KeyError:
            print(
                "Khong tim thay model nay trong danh sach scrip\n"
                "Tien hanh bo qua ..."
            )
            continue

        script = getattr(manufactory, scripts_name)

        # Chon worker tuong ung voi cong viec can thuc hien
        worker = getattr(script, action_code)

        print("Chuan bi tien hanh cong viec")
        try:
            worker.run(**host_info)
            print("Hoan tat")
            print("Chuan bi chuyen qua thiet bi khac ...")
            success_list.append(host["device_name"])
        except ConnectionError:
            print(
                "Khong ket noi / dang nhap duoc thiet bi. Vui long kiem tra lai.\n"
                "Tien hanh bo qua ..."
            )
            false_list.append(host["device_name"])

    when_end(success_list, false_list)


if __name__ == "__main__":
    main()
