from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
import datetime
import json
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def json_to_dict(json_file):
    f = open(json_file, 'r', encoding='utf-8')
    dict = json.load(f)
    # print(dict)
    return dict

username = config.username
password = config.password
# 获取当前签到日期
signin_time = datetime.datetime.now().date()
# 构造对应json文件路径
json_file = 'Booking/' + str(signin_time) + '.json'
dict = json_to_dict(json_file)

# 获取当前hour判断am or pm，从而输出正确的id
now_time = datetime.datetime.now().hour
if (now_time < int(12)):
    id = dict[1]['am']
else:
    id = dict[0]['pm']
# 如果获取的座位id为空，则停止运行
if id == ' ':
    exit(0)

seat = 100455976 + int(id)
url = 'http://update.unifound.net/wxnotice/s.aspx?c=100455521_Seat_' + str(seat) + '_1KD'
logger.info(f'座位ID为：{id}')
# logger.info(f'换算网址为：{url}')
# 浏览器配置
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--no-sandbox')
browser = webdriver.Chrome(options=options)
browser.set_window_size(1920, 1080)
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})

# 记得写完整的url 包括http和https
browser.get(url)

browser.find_element(By.ID, 'username').send_keys(username)
browser.find_element(By.ID, 'password').send_keys(password)
browser.find_element(By.XPATH, '//*[@id="casLoginForm"]/div[4]/div/button').click()
logger.info("登录完成")

try:
    browser.find_element(By.XPATH, '/html/body/div/div[3]/button').click()
    browser.close()
    logger.info("签到成功")
    subject = f'签到成功，座位ID{id}'
    content = f'{str(signin_time)}'
    config.sendEMail(subject, content)
except:
    browser.close()
    logger.info("签到失败")
    subject = f'签到失败！'
    content = f'{str(signin_time)}'
    config.sendEMail(subject, content)
