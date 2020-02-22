"""Su dung file sao luu de phuc hoi cau hinh thiet bi"""
from selenium import webdriver
from selenium.common import exceptions
import os
import time


def run(addr, user, password, file_path):
    """Chuong trinh xu ly chinh"""

    # Thoi gian cho de tai file cau hinh len thiet bi
    up_file_wt = 10

    driver = webdriver.Firefox(service_log_path=os.devnull)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(3)

    try:
        # Truy cap thiet bi
        driver.get(f"http://{user}:{password}@{addr}")

        # Chon Frame chua menu va vao muc khoi phuc / sao luu file cau hinh
        driver.switch_to.frame(driver.find_element_by_xpath('//frame[@src="treeapp.asp"]'))
        driver.find_element_by_xpath('.//li[@id="A_sys"]').click()
        driver.find_element_by_xpath('.//li[@id="sys_backup"]').click()

        # Chuyen ve trang noi dung chinh
        driver.switch_to.default_content()

        # Chon Frame chua noi dung va tien hanh thao tac khoi phuc file cau hinh
        driver.switch_to.frame(driver.find_element_by_xpath('//frame[@src="adm/sys.asp"]'))
        # b1: dien duong dan file cau hinh muon su dung
        cfg_file_input = driver.find_element_by_xpath('//input[@name="filename"]')
        cfg_file_input.clear()
        cfg_file_input.send_keys(file_path)
        # b2: nhan nut apply
        driver.find_element_by_xpath('//input[@id="cfgRestoreBtn"]').click()
        # b3: kiem tra xem da tai file cau hinh len thiet bi hay chua
        check_time = 0
        while check_time <= up_file_wt:
            if "Congratulation!" in driver.page_source:
                print("Da hoan tat viec tai file cau hinh len thiet bi")
                break  # Thoat ra de tien hanh khoi dong lai thiet bi
            else:
                time.sleep(1)
                check_time += 1
        else:
            print("Qua trinh tai file cau hinh qua lau, tien hanh thoat chu dong")
            return False
        # b4: reboot lai thiet bi
        print("Dang khoi dong lai thiet bi")
        driver.find_element_by_xpath('//input[@id="cfgRestReboot"]').click()
        return True

    except exceptions.WebDriverException:
        raise ConnectionError('Khong ket noi duoc den thiet bi')

    finally:
        driver.quit()


def main():
    # Thu muc chua tap tin cau hinh
    parent_dir = os.path.abspath(os.path.join("..", "..", ".."))
    cfg_dir = os.path.join(parent_dir, "files", "configuration")

    # Khai bao cac thong so
    addr = input("Dia chi muon ket noi den: ")
    user = input("User dang nhap: ")
    password = input("Password dang nhap: ")
    cfg_file_name = input("Ten firmware muon su dung: ")
    cfg_path = os.path.join(cfg_dir, cfg_file_name)

    run(addr, user, password, cfg_path)


def debug():
    cfg_path = "/home/dungnguyen/PycharmProjects/autocfg/files/configuration/AP910C_20200210.cfg"
    addr = "192.168.88.243"
    user = "admin"
    password = "admin"

    run(addr, user, password, cfg_path)


if __name__ == '__main__':
    # main()
    debug()
