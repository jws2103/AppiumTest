import os
import unittest
import time
from appium import webdriver
from tests.appium_base import TestAppiumBase


class TestAppiumAndroid(TestAppiumBase):
    def setUp(self):
        self.dc.clear()
        local_env = os.getenv('LOCAL_DEV_ENV')
        if local_env == '1':
            self.dc['app'] = "{PATH_OF_APK_FILE}"
            self.dc['platformName'] = 'Android'
            self.dc['deviceName'] = "{NAME_OF_ANDROID_EMULATOR}"

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.dc)

    def testFirstAutomation(self):
        self.driver.find_element_by_accessibility_id("NavButton").click()

    def testSecondAutomation(self):
        self.driver.find_element_by_accessibility_id("NavButton").click()
        time.sleep(1)
        self.driver.find_element_by_accessibility_id("BackButton").click()


if __name__ == '__main__':
    unittest.main()
