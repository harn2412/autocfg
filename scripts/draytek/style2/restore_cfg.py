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
    driver.implicitly_wait(3)

    try:
        # Truy cap thiet bi
        driver.get(f"http://{addr}")

        # Dang nhap vao thiet bi
        user_field = driver.find_element_by_xpath('.//input[@name="sUserName"]')
        user_field.send_keys(user)

        pass_field = driver.find_element_by_xpath('.//input[@name="sSysPass"]')
        pass_field.send_keys(password)

        driver.find_element_by_xpath('.//input[@name="btnOk"]').click()

        # Bo qua thong bao luc dang nhap
        try:
            alert = driver.switch_to.alert
            alert.dismiss()
        except exceptions.NoAlertPresentException:
            pass

        # Chon Frame chua menu va vao muc restore file cau hinh
        driver.switch_to.frame(driver.find_element_by_xpath('//frame[@name="menu"]'))
        driver.find_element_by_xpath('.//a[@name="#System Maintenance"]').click()
        driver.find_element_by_xpath('.//a[@name="#Configuration Backup"]').click()

        # Chuyen ve trang noi dung chinh
        driver.switch_to.default_content()

        # Chon Frame chua noi dung va tien hanh thao tac restore file cau hinh
        driver.switch_to.frame(driver.find_element_by_xpath('//frame[@name="main"]'))
        driver.switch_to.frame(driver.find_element_by_xpath('//frame[@name="cfgMain"]'))
        file_field = driver.find_element_by_xpath('.//input[@class="file" and @name="sdata"]')
        file_field.clear()
        file_field.send_keys(file_path)

        driver.find_element_by_xpath('.//input[@class="btnw3" and @name="attach"]').click()

        # Tra ve trang thai thanh cong
        for i in range(up_file_wt):
            if "Congratulation!" in driver.page_source:
                print("Da tai file sao luu cau hinh len thiet bi thanh cong")
                driver.find_element_by_xpath('//input[@value="Restart"]').click()
                driver.switch_to.alert.accept()
                return True
            else:
                time.sleep(1)
        else:
            print("Chua reset default duoc")
            return False

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
    cfg_path = "/home/dungnguyen/PycharmProjects/autocfg/files/configuration/V2952_20200222_DrayTek_r88607_beta.cfg"
    addr = "192.168.1.1"
    user = "admin"
    password = "admin"

    run(addr, user, password, cfg_path)


if __name__ == '__main__':
    # main()
    debug()
