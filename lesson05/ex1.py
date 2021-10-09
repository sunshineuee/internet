from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import time
chrome_options = Options()

chrome_options.add_argument('start-maximized')

client = MongoClient('localhost', 27017)
mongo_base = client['mails']

driver = webdriver.Chrome()

driver.get('https://mail.ru/')
elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172')
elem.send_keys(Keys.RETURN)
time.sleep(1)
elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)

mail = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']"))
 )
mail.click()

while True:
    mail_dict = {}
    time.sleep(1)
    contact = driver.find_element_by_class_name('letter-contact').text
    date = driver.find_element_by_class_name('letter__date').text
    theme = driver.find_element_by_tag_name('h2').text
    text_body = driver.find_element_by_class_name('letter__body').text

    mail_dict['contact'] = contact
    mail_dict['date'] = date
    mail_dict['theme'] = theme
    mail_dict['text_body'] = text_body
    mongo_base.mail.insert_one(mail_dict)

    next = driver.find_element_by_xpath("//div[@class='portal-menu-element portal-menu-element_next portal-menu-element_expanded portal-menu-element_not-touch portal-menu-element_pony-mode']")
    next.click()
