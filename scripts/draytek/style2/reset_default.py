"""Khoi phuc cau hinh mac dinh cua router"""
from selenium import webdriver
from selenium.common import exceptions
import os
import time


def run(addr, user, password):
    """Chuong trinh xu ly chinh"""
    driver = webdriver.Firefox(service_log_path=os.devnull)
    driver.set_page_load_timeout(30)
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

        # Chon Frame chua menu va vao muc reboot
        driver.switch_to.frame(driver.find_element_by_xpath('//frame[@name="menu"]'))
        driver.find_element_by_xpath('.//a[@name="#System Maintenance"]').click()
        driver.find_element_by_xpath('.//a[@name="#Reboot System"]').click()

        # Chuyen ve trang noi dung chinh
        driver.switch_to.default_content()

        # Chon Frame chua noi dung va tien hanh thao tac reset default
        driver.switch_to.frame(driver.find_element_by_xpath('//frame[@name="main"]'))
        driver.find_element_by_xpath('//input[@type="radio" and @value="Default"]').click()
        driver.find_element_by_xpath('//input[@name="submitbnt"]').click()

        # Tra ve trang thai thanh cong
        for i in range(5):
            if "Router is restarting" in driver.page_source:
                print("Da reset default thiet bi thanh cong")
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
    # url = input("Dia chi muon ket noi den :")
    # user = input("User dang nhap: ")
    # password = input("Password dang nhap: ")
    # run(url, user, password)
    run("192.168.1.1", "admin", "admin")


if __name__ == '__main__':
    main()
