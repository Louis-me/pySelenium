## 概述
- 实现都设备并发谷歌浏的web自动化测试 
- 环境信息：win10 python 3.7.9 pytest pytest-html
- 谷歌浏览器版本：114.0.5735.199
## 说明
- 实现多设备并行chrome 浏览器自动化
- 写用例如下
```buildoutcfg
from selenium.webdriver.common.by import By
def test_001_open_usr3(driver, click_element, find_x_element):
    click_element((By.XPATH, '//span[contains(text(),"用例管理")]'))
    click_element((By.XPATH, '//span[contains(text(),"用例列表")]'))
    click_element((By.XPATH, '//span[contains(text(),"用户管理")]'))
    click_element((By.XPATH, '//span[contains(text(),"用户列表")]'))
    find_x_element((By.CSS_SELECTOR, "input")).send_keys("test2")
    click_element((By.XPATH, '//i[@class="el-icon-search"]'))
    find_x_element((By.XPATH, "//div[contains(text(), 'test2')]"))
    driver.get("http://www.shikun.work:8001/#/users"
```
- 代码入口在main.py



