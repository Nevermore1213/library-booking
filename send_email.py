import smtplib
# 处理邮件内容的库，email.mine
from email.mime.text import MIMEText
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SendMsg:
    def __init__(self, userName_SendMail, received_mail, userName_AuthCode, content):
        '''

        :param userName_SendMail: 发件人
        :param received_mail: 收件人
        :param userName_AuthCode: 授权码
        :param content: 发送内容
        '''
        self.userName_SendMail = userName_SendMail
        self.received_mail = received_mail
        self.userName_AuthCode = userName_AuthCode
        self.content = content

    def send_msg(self):
        # 邮箱属性配置
        # 邮箱服务端
        mailserver = 'smtp.qq.com'
        # 纯文本形式的邮件内容的定义，通过MIMEText进行操作，plain为默认的文本的展示形式
        email = MIMEText(self.content, 'plain', 'utf-8')
        email['Subject'] = '图书馆预约'  # 定义邮件主题
        email['From'] = self.userName_SendMail  # 发件人
        email['To'] = ','.join(self.received_mail)  # 收件人（可以添加多个，若只有一个收件人，可直接写邮箱号）
        # 发送邮件
        # QQ邮箱的端口号是465，其他邮箱的端口号可自行百度，非QQ邮箱，一般使用SMTP即可，不需要有SSL
        smtp = smtplib.SMTP_SSL(mailserver, port=465)
        smtp.login(self.userName_SendMail, self.userName_AuthCode)
        smtp.sendmail(self.userName_SendMail, ','.join(self.received_mail), email.as_string())
        smtp.quit()
        logger.info('邮件发送成功')


if __name__ == '__main__':
    # 发件人-填写自己的邮箱
    userName_SendMail = ''
    # 邮箱发件授权码-为发件人生成的授权码
    userName_AuthCode = ''
    # 定义邮件的接收者
    received_mail = ['']
    content = ' '
    smtp = SendMsg(userName_SendMail, received_mail, userName_AuthCode, content)
    smtp.send_msg()
# # 邮箱属性配置
# # 邮箱服务端
# mailserver = 'smtp.qq.com'
# # 发件人-填写自己的邮箱
# userName_SendMail = '3086151468@qq.com'
# # 邮箱发件授权码-为发件人生成的授权码
# userName_AuthCode = 'pmjktlouptvgdege'
# # 定义邮件的接收者-我随便写的，若收件人较多，可用列表表示
# received_mail = ['2139511496@qq.com']
#
# # 发送一封简单的邮件，处理邮件内容
# content = '这是一封纯粹的文本信息内容！来自ITester软测试小栈的CoCo'
# # 纯文本形式的邮件内容的定义，通过MIMEText进行操作，plain为默认的文本的展示形式
# email = MIMEText(content, 'plain', 'utf-8')
# email['Subject'] = '这是邮件的主题-By ITester软测试小栈'  # 定义邮件主题
# email['From'] = userName_SendMail  # 发件人
# email['To'] = ','.join(received_mail)  # 收件人（可以添加多个，若只有一个收件人，可直接写邮箱号）
#
#
# # 发送邮件
#
# # QQ邮箱的端口号是465，其他邮箱的端口号可自行百度，非QQ邮箱，一般使用SMTP即可，不需要有SSL
# smtp = smtplib.SMTP_SSL(mailserver, port=465)
# smtp.login(userName_SendMail, userName_AuthCode)
# smtp.sendmail(userName_SendMail, ','.join(received_mail), email.as_string())
#
# smtp.quit()
# print('恭喜🎉，邮件发送成功了')
