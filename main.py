import os
from multiprocessing import Process

import pytest


def main(path,report):
    pytest.main(['%s' % path, '--html=%s.html' % report, '--self-contained-html', '--capture=sys'])
    # pytest testcase\大回归\小回归\冒烟1  --html=report.html --self-contained-html --capture=sys

if __name__ == '__main__':
    # 大回归
    test_case = Process(target=main, args=("E:\proj\\pySelenium\\testcase\\大回归\\小回归\\冒烟1", "report1"))
    test_case.start()
    # test_case.join()
    # 小回归
    test_case2 = Process(target=main, args=("E:\proj\\pySelenium\\testcase\\大回归\\小回归\\冒烟2", "report2"))
    test_case2.start()

    test_case.join()
    test_case2.join()
    # 冒烟
    ...
