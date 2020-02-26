"""Khoi phuc cau hinh mac dinh cua router"""
from selenium import webdriver
from selenium.common import exceptions
import os


def run(addr, user, password):
    """Chuong trinh xu ly chinh"""
    driver = webdriver.Firefox(service_log_path=os.devnull)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(3)

    try:
        # Truy cap thiet bi
        driver.get(f"http://{user}:{password}@{addr}")

        # Chon Frame chua menu va vao muc reboot
        driver.switch_to.frame(driver.find_element_by_xpath('//frame[@src="treeapp.asp"]'))
        driver.find_element_by_xpath('.//li[@id="A_sys"]').click()
        driver.find_element_by_xpath('.//li[@id="sys_reboot"]').click()

        # Chuyen ve trang noi dung chinh
        driver.switch_to.default_content()

        # Chon Frame chua noi dung va tien hanh thao tac reset default
        driver.switch_to.frame(driver.find_element_by_xpath('//frame[@src="adm/sys.asp"]'))
        driver.find_element_by_xpath('//input[@type="radio" and @value="Default"]').click()
        driver.find_element_by_xpath('//input[@id="rebootApply"]').click()
        driver.switch_to.alert.accept()

        # Tra ve trang thai thanh cong
        print("Da reset default thiet bi thanh cong")
        return True

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
