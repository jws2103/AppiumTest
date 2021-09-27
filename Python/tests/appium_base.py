import os
import unittest
from appium.webdriver import webdriver


class TestAppiumBase(unittest.TestCase):
    dc = {}
    driver = None;

    def setUp(self):
        self.driver = None;

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()