from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

username = '16605407609'
password = 'Liming2002'
#获取当前签到日期
signin_time = datetime.datetime.now().date()
#读取座位id构造签到网址
f = open(f'{signin_time}.txt',encoding='utf-8')
id = ''
for i in f:
    id += i
Seat = int(id)
seat = 100455976 + Seat
url = 'http://update.unifound.net/wxnotice/s.aspx?c=100455521_Seat_'+str(seat)+'_1KD'
logger.info(f'座位ID为：{id}')
#logger.info(f'换算网址为：{url}')
#浏览器配置
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--no-sandbox')
#options.add_argument('--proxy-server=http://' + proxy)
browser = webdriver.Chrome(options=options)
browser.set_window_size(1920, 1080)
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})

# 记得写完整的url 包括http和https
browser.get(url)


browser.find_element(By.ID, 'username').send_keys(username)
browser.find_element(By.ID, 'password').send_keys(password)
browser.find_element(By.XPATH,'//*[@id="casLoginForm"]/div[4]/div/button').click()
logger.info("登录完成")

try:
    browser.find_element(By.XPATH, '/html/body/div/div[3]/button').click()
    # browser.get_screenshot_as_file('3.png')
    browser.close()
    logger.info("签到成功")
except:
    logger.info("签到失败")
    browser.close()

