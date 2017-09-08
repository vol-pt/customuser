from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('http://localhost:8000/login/')
el = driver.find_element_by_name("username")
el.send_keys("zaq3@wp.pl")
password = driver.find_element_by_name('password')
password.send_keys("zaqmko123")
button = driver.find_element_by_tag_name("button")
button.send_keys(Keys.ENTER)
from time import sleep

sleep(5)
driver.quit()
