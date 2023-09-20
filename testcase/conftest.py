import logging
import time

import pytest
from selenium import webdriver
from py._xmlgen import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

se_driver = None

@pytest.fixture(scope='session', autouse=True)
def driver():
    global se_driver
    chrome_exe = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe"
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_exe
    chrome_driver = r"E:\proj\pySelenium\exe\chromedriver.exe"
    se_driver = webdriver.Chrome(chrome_driver, options=options)
    se_driver.maximize_window()
    # se_driver.implicitly_wait(30)
    login(se_driver)
    yield se_driver
    # se_driver.close()
    se_driver.quit()


def login(driver):
    driver.get("http://www.shikun.work:8001/#/login")
    time_out = 10
    # 用户名文本框
    usr_locator = (By.XPATH, "//input[@type='text']")
    # 密码文本框
    pwd_locator = (By.XPATH, "//input[@type='password']")
    # 登录
    lg_locator = (By.XPATH, "//button[1]")
    # 检查登录是否成功
    ch_locator = (By.XPATH, "//span[contains(text(),'注销')]")
    WebDriverWait(driver, time_out).until(
        EC.visibility_of_element_located(usr_locator)
    )
    WebDriverWait(driver, time_out).until(
        EC.visibility_of_element_located(pwd_locator)
    )
    WebDriverWait(driver, time_out).until(
        EC.visibility_of_element_located(lg_locator)
    )
    time.sleep(1)

    driver.find_element(*usr_locator).click()
    driver.find_element(*usr_locator).send_keys("test1")
    time.sleep(1)

    driver.find_element(*pwd_locator).click()
    driver.find_element(*pwd_locator).send_keys("123456")
    time.sleep(1)

    driver.find_element(*lg_locator).click()
    # WebDriverWait(driver, time_out).until(
    #     EC.visibility_of_element_located(ch_locator)
    # )
    WebDriverWait(driver, time_out).until(
        lambda x:driver.find_element(*ch_locator)
    )
    logging.info("登录成功")


@pytest.fixture(scope='function', autouse=True)
def home_page(driver):
    driver.get("http://www.shikun.work:8001/#/welcome")


@pytest.fixture
def click_element(driver):
    def _click_element(locator, time_out=10):
        """
        封装点击事件
        button_locator = (By.CSS_SELECTOR, "#myButton")
        click_element(button_locator)
        :param locator:
        :return:
        """
        # 使用 Selenium 的 find_element 方法找到元素并进行点击操作
        WebDriverWait(driver, time_out).until(
            EC.visibility_of_element_located(locator)
        )
        element = driver.find_element(*locator)
        time.sleep(2)
        element.click()

    return _click_element


@pytest.fixture
def find_x_element(driver):
    def _find_x_element(locator, timeout=10):
        """

        :param locator:  定位的元素
        :param timeout:
            element_locator = (By.CSS_SELECTOR, "#myElement")
            element = find_element(element_locator)

        :return:
        """
        # 使用 Selenium 的 WebDriverWait 来等待元素可见，并返回查找到的元素
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

        return element

    return _find_x_element


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    """
    #添加summary内容
    """
    prefix.extend([html.p("所属部门: 测试组")])
    prefix.extend([html.p("框架设计: XXX")])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """

    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()

    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            screen_img = _capture_screenshot(se_driver)
            if screen_img:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:1024px;height:768px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))  # 表头添加Description
    cells.pop(-1)  # 删除link


def pytest_html_results_table_row(report, cells):
    """新增用例描述内容，来自于用例的注释"""
    # cells.insert(1, html.td(report.description))  # 用例的描述
    cells.pop(-1)  # 删除link


def pytest_html_results_table_html(report, data):
    """
    去除执行成功用例的log输出
    """
    if report.passed:
        del data[:]
        data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))
    pass


def pytest_html_report_title(report):
    report.title = "pytest示例项目测试报告"

# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     '''收集测试结果'''
#     # print(terminalreporter.stats)
#     passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
#     failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
#     error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
#     # skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
#     # print('成功率：%.2f' % (len(terminalreporter.stats.get('passed', []))/terminalreporter._numcollected*100)+'%')
#     # terminalreporter._sessionstarttime 会话开始时间
#     duration = time.time() - terminalreporter._sessionstarttime


def _capture_screenshot(driver):
    """
    截图保存为base64
    :return:
    """
    return driver.get_screenshot_as_base64()
