import os
# 强制让 Selenium 进入离线模式，直接使用你刚才已经下载好的本地 148 驱动
os.environ["SE_OFFLINE"] = "true"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10



class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID,'id_list_table')
                rows = table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID,'id_list_table')
        rows = table.find_elements(By.TAG_NAME,'tr')
        self.assertIn(row_text, [row.text for row in rows])
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        #张三听说有一个在线代办事项应用
        #他去看了这个应用的首页
        self.browser.get(self.live_server_url)

        #他注意到网页里包含了“To-Do”这个词
        self.assertIn('To-Do', self.browser.title),"browser title was " + self.browser.title
        header_text=self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do', header_text)

        #应用有一个输入待办事项的文本框，邀请他输入一个待办事项
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')
        #他在文本框里输入了“Buy flowers” (买花)
        inputbox.send_keys('Buy flowers')
        #当他按下回车键后，页面更新了，待办事项表格里显示了“1: Buy flowers”
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')

        #页面又显示了一个文本框，可以输入其他的待办事项
        #他在文本框里输入了“Send a gift to lisi” (送礼物给李四)
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Send a gift to lisi')
        inputbox.send_keys(Keys.ENTER)

        #页面再次更新，清单里显示了这两个待办事项
        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Send a gift to lisi')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #张三新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_for_row_in_list_table('1: Buy flowers')

        #他注意到这个清单有唯一的url
        zhangsan_list_url=self.browser.current_url
        self.assertRegex(zhangsan_list_url,'/lists/.+')

        #现在一个叫王五的新用户访问了这个应用
        #我们使用一个新的浏览器会话
        #确保张三的信息不会从cookie里泄露出来
        self.browser.quit()
        self.browser=webdriver.Chrome()

        #王五访问首页，首页没有张三的待办事项
        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertNotIn('Send a gift to lisi', page_text)

        #王五输入一个新的待办事项，新建一个清单
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #这个页面还是没有张三的清单
        page_text=self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertIn('Buy milk', page_text)

        #两个人都很满意，去睡觉了

    def test_layout_and_styling(self):
        #张三访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        #他看到输入框完美地居中显示在页面上
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        #他新建了一个清单，看到输入框仍然完美地居中显示在页面上
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
            )
        
