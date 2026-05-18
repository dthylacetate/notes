import os
# 强制让 Selenium 进入离线模式，直接使用你刚才已经下载好的本地 148 驱动
os.environ["SE_OFFLINE"] = "true"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        #张三听说有一个在线代办事项应用
        #他去看了这个应用的首页
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)
        table = self.browser.find_element(By.ID,'id_list_table')
        rows = table.find_elements(By.TAG_NAME,'tr')
        self.assertIn('1: Buy flowers', [row.text for row in rows])

        #页面又显示了一个文本框，可以输入其他的待办事项
        #他在文本框里输入了“Send a gift to lisi” (送礼物给李四)
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Send a gift to lisi')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #页面再次更新，清单里显示了这两个待办事项
        table = self.browser.find_element(By.ID,'id_list_table')
        rows = table.find_elements(By.TAG_NAME,'tr')
        self.assertIn('1: Buy flowers', [row.text for row in rows])
        self.assertIn('2: Send a gift to lisi', [row.text for row in rows])

        #张三想知道这个网站是否会记住他的待办事项，他看到页面上有一个唯一的URL链接指向这个待办事项清单
        #他访问了这个URL，发现他的待办事项清单还在
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()