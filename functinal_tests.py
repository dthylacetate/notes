from selenium import webdriver
import unittest

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
        self.fail('Finish the test!')

        #应用有一个输入待办事项的文本框，邀请他输入一个待办事项

        #他在文本框里输入了“Buy flowers” (买花)

        #当他按下回车键后，页面更新了，待办事项表格里显示了“1: Buy flowers”

        #页面又显示了一个文本框，可以输入其他的待办事项
        #他在文本框里输入了“Send a gift to lisi” (送礼物给李四)

        #页面再次更新，清单里显示了这两个待办事项

        #张三想知道这个网站是否会记住他的待办事项，他看到页面上有一个唯一的URL链接指向这个待办事项清单
        #他访问了这个URL，发现他的待办事项清单还在

if __name__ == '__main__':
    unittest.main()