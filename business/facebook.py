import random
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import shutil
import requests
from pyjpgclipboard import clipboard_load_jpg

from business import sheets
from misc.models import Task

POSTER_URL = 'https://www.facebook.com/'


class Facebook:
    def __init__(self, task: Task):
        self.task = task
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(chrome_options)

    def close(self):
        try:
            self.driver.quit()
        except:
            pass

    def login(self) -> bool:
        self.driver.get(POSTER_URL)
        self.driver.find_element(By.ID, 'email').send_keys(self.task.worker.email)
        self.driver.find_element(By.ID, 'pass').send_keys(self.task.worker.password)
        self.driver.find_element(By.ID, 'loginbutton').click()
        time.sleep(5)
        return 'We suspended your account' not in self.driver.page_source and 'Неверные данные' not in self.driver.page_source and 'Неправильный пароль' not in self.driver.page_source and 'Check your email' not in self.driver.page_source

    def _scroll(self):
        page_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_amount = 0

        for _ in range(random.randint(3, 10)):
            scroll_new = random.randint(page_height // 4, page_height // 2)
            for _ in range(10):
                scroll_amount += scroll_new / 10
                self.driver.execute_script("window.scrollTo(0, {})".format(scroll_amount))
                time.sleep(0.1)
            time.sleep(random.randint(3, 6))

    def subscribe_group(self):
        self._scroll()
        self.driver.get(self.task.link)
        time.sleep(3)
        span_element = self.driver.find_element(By.XPATH, "//span[text()='Присоединиться к группе']")
        if span_element is None:
            span_element = self.driver.find_element(By.XPATH, "//div[@aria-label='Join Group']")
        print(span_element)
        if span_element is not None:
            span_element.click()
        time.sleep(3)

    def check_subscription(self):
        self.driver.get(self.task.link)
        time.sleep(3)
        try:
            span_element = self.driver.find_element(By.XPATH, "//span[text()='Присоединиться к группе']")
        except:
            return True
        print(span_element)
        return span_element is None

    def download_image(self, link: str):
        link = link.split('d/')[1].split('/')[0]
        link = f'https://drive.usercontent.google.com/u/0/uc?id={link}&export=download'
        response = requests.get(link, stream=True)
        with open('1.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        clipboard_load_jpg("1.jpg")

    def create_post(self):
       # self._scroll()
        self.driver.get(self.task.link)
        #self._scroll()
        self.driver.execute_script("window.scrollTo(0, 0)")
        span = self.driver.find_element(By.XPATH, "//span[text()='Напишите что-нибудь...']")
        span.click()
        time.sleep(8)
        try:
            span = self.driver.find_element(By.XPATH, "//div[@aria-label='Напишите что-нибудь...']")
        except:
            span = self.driver.find_element(By.XPATH, "//div[@aria-label='Создайте общедоступную публикацию…']")
        time.sleep(5)
        span.send_keys("""Universal
. Invest in peace of mind with our high-performance doors and windows, engineered
for superior security and energy efficiency. Experience the difference of quality
craftsmanship and professional installation.
. Illuminate your space with our premium windows and doors, designed to maximize
natural light and ventilation while minimizing energy costs. Trust our expert team to
deliver unmatched quality and service.
. Embrace superior comfort and savings with our energy-efficient windows and doors,
crafted with the highest quality materials and technology. Trust our expert team to
deliver unparalleled performance and service.
. Make a grand entrance with our elegant doors, meticulously crafted for timeless
beauty and performance. Experience superior quality and service with our expert
installation.
Illuminate your space with our energy-efficient windows and doors, designed to
enhance your home's comfort and beauty. Trust our expert team to deliver superior
quality and professional installation.
Telephone- 0800 448 0252
Mobile- 07917 483148
Email- info@pcsgaragedoors.co.uk""")
        time.sleep(1)
        self.download_image(sheets.get_random_banner_link())
        try:
            span.send_keys(Keys.COMMAND, 'v')
        except:
            pass
        span.send_keys(Keys.CONTROL, 'v')
        time.sleep(3)
        self.driver.find_element(By.XPATH, "//div[@aria-label='Отправить']").click()
