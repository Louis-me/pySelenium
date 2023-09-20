import time

from selenium.webdriver.common.by import By

def test_001_open_usr2(driver, click_element, find_x_element):
    click_element((By.XPATH, '//span[contains(text(),"用户管理")]'))
    click_element((By.XPATH, '//span[contains(text(),"用户列表")]'))
    find_x_element((By.CSS_SELECTOR, "input")).send_keys("test1")
    click_element((By.XPATH, '//i[@class="el-icon-search"]'))
    find_x_element((By.XPATH, "//div[contains(text(), 'test1')]"))