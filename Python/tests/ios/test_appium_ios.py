import os
import time
import unittest
from appium import webdriver
from tests.appium_base import TestAppiumBase


class TestAppiumiOS(TestAppiumBase):
    def setUp(self):
        self.dc.clear()
        local_env = os.getenv('LOCAL_DEV_ENV')
        if local_env == '1':
            self.dc['automationName'] = 'XCUITest'
            self.dc['platformName'] = 'iOS'
            self.dc['platformVersion'] = '{OS_Version}'
            self.dc['deviceName'] = "{Device_name}"
            self.dc['udid'] = '{Device_udid}'
            self.dc['bundleId'] = '{Bundle_id}'

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.dc)

    def testFirstAutomation(self):
        self.driver.find_element_by_accessibility_id("NavButton").click()

    def testSecondAutomation(self):
        self.driver.find_element_by_accessibility_id("NavButton").click()
        time.sleep(1)
        self.driver.find_element_by_accessibility_id("BackButton").click()


if __name__ == '__main__':
    unittest.main()
