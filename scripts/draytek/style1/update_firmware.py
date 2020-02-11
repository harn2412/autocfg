"""Nang cap firmware cho thiet bi"""
from selenium import webdriver
from selenium.common import exceptions
import os
import time


def run(addr, user, password, fw_path, check_success=False):
    """Chuong trinh xu ly chinh"""
    # Thoi gian cho trong qua trinh nang cap firmware
    upgrade_wt = 30

    # Thoi gian cho trong qua trinh kiem tra xem firmware nang cap thanh cong chua
    check_success_wt = 180

    driver = webdriver.Firefox(service_log_path=os.devnull)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(3)

    try:
        # Truy cap thiet bi
        driver.get(f"http://{user}:{password}@{addr}")

        # Chon Frame chua menu va vao muc nang cap firmware
        driver.switch_to.frame(driver.find_element_by_xpath('//frame[@src="treeapp.asp"]'))
        driver.find_element_by_xpath('.//li[@id="A_sys"]').click()
        driver.find_element_by_xpath('.//li[@id="sys_fwup"]').click()

        # Chuyen ve trang noi dung chinh
        driver.switch_to.default_content()

        # Chon Frame chua noi dung va tien hanh thao tac nang cap firmware
        driver.switch_to.frame(driver.find_element_by_xpath('//frame[@src="adm/sys.asp"]'))
        # b1: dien duong dan file firmware muon su dung
        firmware_input = driver.find_element_by_xpath('//input[@name="filename"]')
        firmware_input.clear()
        firmware_input.send_keys(fw_path)
        # b2: nhan nut apply
        driver.find_element_by_xpath('//input[@id="uploadFWApply"]').click()
        # b3: kiem tra xem da tai firmware len thiet bi hay chua
        check_time = 0
        while check_time <= upgrade_wt:
            if "The uploaded firmware image is being transferred to flash." in driver.page_source:
                print("Da hoan tat viec tai Firmware len thiet bi")
                if check_success is False:
                    time.sleep(3)
                    return True
                else:
                    break  # Thoat ra de tien hanh kiem tra viec nang cap firmware
            else:
                time.sleep(1)
                check_time += 1
        else:
            print("Qua trinh nang cap firmware qua lau, tien hanh thoat chu dong")
            return False

        # ghi nhan ket qua nang cap thanh cong
        if check_success is True:
            print("Dang kiem tra ket qua nang cap firmware. Vui long cho ...")
            check_time = 0
            while check_time <= check_success_wt:
                try:
                    alert = driver.switch_to.alert

                    if "Firmware Upgrade success." in alert.text:
                        print("Firmware da duoc nang cap thanh cong")
                        alert.accept()
                        return True
                    elif "Warning!The firmware didn't change." in alert.text:
                        print("Firmware khong co su thay doi")
                        alert.accept()
                        return False
                    else:
                        print("Khong hieu thong bao tra ve")
                        print(alert.text)
                        return False

                except exceptions.NoAlertPresentException:
                    time.sleep(1)
                    check_time += 1
            else:
                print("Qua trinh kiem tra dien ra qua lau, tien hanh thoat chu dong")

    except exceptions.WebDriverException:
        raise ConnectionError('Khong ket noi duoc den thiet bi')

    finally:
        driver.quit()


def main():
    # Thu muc chua tap tin firmware
    parent_dir = os.path.abspath(os.path.join("..", "..", ".."))
    fw_dir = os.path.join(parent_dir, "files", "firmware")

    # Khai bao cac thong so
    addr = input("Dia chi muon ket noi den: ")
    user = input("User dang nhap: ")
    password = input("Password dang nhap: ")
    fw_file_name = input("Ten firmware muon su dung: ")
    fw_path = os.path.join(fw_dir, fw_file_name)

    run(addr, user, password, fw_path)


def debug():
    fw_path = "/home/dungnguyen/PycharmProjects/autocfg/files/firmware/ap910c_r11412_131.all"
    # fw_path = "/home/dungnguyen/PycharmProjects/autocfg/files/firmware/ap910c_r11127_130.all"
    addr = "192.168.88.243"
    user = "admin"
    password = "admin"

    run(addr, user, password, fw_path)


if __name__ == '__main__':
    main()
    # debug()
