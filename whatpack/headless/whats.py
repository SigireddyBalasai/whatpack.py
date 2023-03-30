"""THis is the selenium base used by us to do all whatsapp related tasks"""

import os
import time
import pathlib
from selenium.webdriver.common.by import By
import selenium.webdriver.support.wait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class WhatsApp:
    """THis class will allow us to do log in to whatsapp web and then send messages
    to the user and send images and documents and do other utility functions"""

    def __init__(self, headless: bool = True):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        useragent = "user-agent=Mozilla/5.0 (X11; Linux i686; rv:77.0) Gecko/20100101 Firefox/77.0"
        chrome_options.add_argument(useragent)
        path = str(pathlib.Path('../chrome-data').resolve())
        chrome_options.add_argument(fr"user-data-dir={path}")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.login()

    def login(self):
        """This is used either to do log in the user or ensure that is user is already logged in"""
        driver = self.driver
        try:
            driver.get('https://web.whatsapp.com/')
            selenium.webdriver.support.wait.WebDriverWait(driver, 60).until(
                ec.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/'
                                                          'div[3]/div[1]/div/div/div'
                                                          '[2]/div/canvas')))
            selenium.webdriver.support.wait.WebDriverWait(driver, 60). \
                until(ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/div/span')))
            print('qr found')
            qrcode = driver.find_element(By.XPATH,
                                         '//*[@id="app"]/div/div/div[3]'
                                         '/div[1]/div/div/div[2]/div/canvas')
            print(qrcode.screenshot("hello.png"))
            self.driver = driver
            time.sleep(30)
            return self.login()
        except NoSuchElementException as problem:
            print(problem)
            selenium.webdriver.support.wait.WebDriverWait(driver, 60).until(
                ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div/div/div[3]/header/div[2]/div/span/div[4]/div')))
            self.driver = driver
            return True

    def get_pending_chats(self):
        """THis is used to get the pending chats and return them as a list"""
        driver = self.driver
        driver.get('https://web.whatsapp.com/')
        selenium.webdriver.support.wait.WebDriverWait(driver, 60).until(
            ec.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[1]/div/button')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[3]/div/div[1]/div/button')
        element.click()
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div')
        print(element)
        self.driver = driver
        time.sleep(2)

    def send_user_message(self, phone: str, message: str):
        """This is used to send message to the user"""
        driver = self.driver
        phone = phone.replace(" ", "")
        driver.get(f'https://web.whatsapp.com/send?phone={phone}&text={message}')
        selenium.webdriver.support.wait.WebDriverWait(driver, 60).until(
            ec.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/'
                           'div[1]/div/span[2]/div/div[2]/div['
                           '2]/button')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[4]/div/'
                                      'footer/div[1]/div/span[2]/div/div['
                                      '2]/div['
                                      '2]/button')
        element.click()
        self.driver = driver
        time.sleep(2)

    def send_document(self, phone: str,
                      file_list: list[str] = None,
                      filename: str = None,
                      folder_name: str = None):
        """This will send document to the user"""
        driver = self.driver
        phone = phone.replace(" ", "")
        driver.get(f'https://web.whatsapp.com/send?phone={phone}')
        selenium.webdriver.support.wait.WebDriverWait(driver, 60).until(
            ec.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer'
                           '/div[1]/div/span[2]/div/div[1]/div[2]/div/div')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[4]/div/'
                                      'footer/div[1]/div/span[2]/div/div['
                                      '1]/div['
                                      '2]/div/div')
        element.click()
        print('window opened')
        selenium.webdriver.support.wait.WebDriverWait(driver, 60).until(
            ec.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/'
                           'div[1]/div/span[2]/div/div[1]/div['
                           '2]/div/span/div/div/ul/li[4]/button/input')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[4]/div/'
                                      'footer/div[1]/div/span[2]/div/div['
                                      '1]/div['
                                      '2]/div/span/div/div/ul/li[4]/button/input')
        print("file menu opened")
        if folder_name:
            file_list = [x for x in pathlib.Path(folder_name).iterdir() if not x.is_dir()]
        if filename:
            element.send_keys(str(pathlib.Path(filename)))
        else:
            for i in file_list:
                element.send_keys(str(pathlib.Path(i)))
        selenium.webdriver.support.wait.WebDriverWait(driver, 60).until(
            ec.presence_of_element_located(
                (By.XPATH,
                 '/html/body/div[1]/div/div/div[2]/div[2]/span/div'
                 '/span/div/div/div[2]/div/div[2]/div[2]/div/div')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[2]'
                                      '/div[2]/span/div/span/div/div/div['
                                      '2]/div/div[2]/div[2]/div/div')
        element.click()
        self.driver = driver
        time.sleep(10)

    def send_image(self, phone: str, filename: str):
        """This function will send an image from our default path in the browser"""
        driver = self.driver
        phone = phone.replace(" ", "")
        driver.get(f'https://web.whatsapp.com/send?phone={phone}')
        selenium.webdriver.support.wait.WebDriverWait(driver, 60).until(
            ec.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div[4]/div/'
                           'footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[4]/div/'
                                      'footer/div[1]/div/span[2]/div/div['
                                      '1]/div['
                                      '2]/div/div')
        element.click()
        path_of_file = pathlib.Path(filename)
        selenium.webdriver.support.wait.WebDriverWait(driver, 60).until(
            ec.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/'
                           'div[1]/div/span[2]/div/div[1]/div['
                           '2]/div/span/div/div/ul/li[1]/button/input')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[4]/'
                                      'div/footer/div[1]'
                                      '/div/span[2]/div/div['
                                      '1]/div['
                                      '2]/div/span/div/div/ul/li[1]/button/input')
        element.send_keys(str(path_of_file.resolve()))
        selenium.webdriver.support.wait.WebDriverWait(driver, 60).until(
            ec.presence_of_element_located(
                (By.XPATH,
                 '/html/body/div[1]/div/div/div[2]/div[2]/span'
                 '/div/span/div/div/div[2]/div/div[2]/div[2]/div/div')))
        element = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/div/div/div[2]/div[2]'
                                      '/span/div/span/div/div/div['
                                      '2]/div/div['
                                      '2]/div[2]/div/div')
        element.click()
        self.driver = driver
        time.sleep(7)

    def __del__(self):
        driver = self.driver
        driver.close()
        self.driver = driver
