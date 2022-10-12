# library-booking

**qdu library booking and sign in**

- main.py 预约主程序，在配置区填写账号密码，还有预约座位信息
- library.py 实现登录，预约功能, 查询房间预约情况
- signin.py 签到功能
- config.py 房间信息
- Booking 预约成功后储存的信息
- send_email.py 实现发送邮件功能

Booking文件夹内储存了预约成功的时间段和座位id，文件格式为‘2022-xx-xx.json’

文件内为main.py 运行后生成的字典，‘[
  {
    "pm": "008"
  },
  {
    "am": "009"
  }
]’

供 signin.py 调用
 
登录预约部分转载自 https://syhu.com.cn/archives/tu-shu-guan-wei-zhi-yu-yue