import time

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import schedule
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta


def request_url(url):
    # google_translate = "https://translate.google.com/?hl=zh-CN&sl=auto&tl=zh-CN&op=websites"
    driver = webdriver.Firefox()
    driver.minimize_window()
    # 打开Google网站
    driver.get(url)
    # wait = WebDriverWait(driver, 10)
    # input_element = wait.until(EC.presence_of_element_located((By.ID, "i48")))
    # input_element.send_keys(url)
    # button = driver.find_element(By.XPATH, "//button[@data-idom-class='yHy1rc eT1oJ mN1ivc zhBWDc']")
    #
    # # 点击按钮
    # button.click()
    time.sleep(5)
    # driver.switch_to.window(driver.window_handles[1])
    # 最大化
    # driver.maximize_window()
    # 最小化
    # driver.minimize_window()
    # 等待一些时间以确保搜索结果加载完成
    driver.implicitly_wait(60)
    # 获取搜索结果
    body = driver.find_element("tag name", "body")
    body.send_keys(Keys.END)  # 模拟按下“End”键

    # 等待一些时间以加载更多数据
    time.sleep(20)  # 这里可以根据您的需求进行调整
    search_results = driver.page_source

    # 检查请求是否成功

    soup = BeautifulSoup(search_results, 'html.parser')
    # 找到所有具有特定类名的标签
    target_tags = soup.find_all('div', class_='newsdeskContentEntry')
    current_datetime = datetime.now()
    date_string = current_datetime.strftime("%Y-%m-%d-%H")

    file_name = f"F:\\notebooks\\其他\\daily\\{date_string}_rotoballer.md"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("<center>" + date_string + " Daily </center>\n\n")
        i = 1
        for target_tag in target_tags:

            # 找到上一个h4标签
            date_time = target_tag.find('span', class_='newsDate').text
            if "day" not in date_time:
                previous_h4 = target_tag.find_previous('h4')
                if previous_h4:
                    head = soup.find('div', class_='shareBox').get_text()
                    title = previous_h4.text
                    news_text = target_tag.get_text().replace(head, "").replace(date_time, "")
                    news_text = news_text.split("--")[0]
                    file.write(f"{str(i)}. {title}\n")  # 写入标题，注意要加上Markdown标题的格式
                    file.write(news_text + "\n")  # 写入内容
                    i += 1
                else:
                    print("未找到上一个h4标签")

    with open(file_name, 'r', encoding='utf-8') as f:
        topic = date_string + " rotoballer Daily"
        msg = f.read()
        send_email(topic, msg)


def send_email(topic, msg):
    # 设置发件人和收件人的邮箱地址
    sender_email = '847634038@qq.com'
    receiver_email = '847634038@qq.com'

    # 创建邮件内容
    subject = topic

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # 添加文本内容
    message.attach(MIMEText(msg, 'plain'))
    smtp_port = 465  # QQ邮箱的SMTP端口号

    # 请注意，您需要启用QQ邮箱的SMTP授权码，而不是QQ邮箱的登录密码
    smtp_username = '847634038@qq.com'
    smtp_password = 'yovtxvhipavhbcag'  # QQ邮箱的SMTP授权码

    # 连接到SMTP服务器
    with smtplib.SMTP_SSL('smtp.qq.com', smtp_port) as server:
        server.login(smtp_username, smtp_password)  # 登录到SMTP服务器
        server.sendmail(sender_email, receiver_email, message.as_string())


def my_task():
    url = "https://www.rotoballer.com/player-news?sport=nba"
    request_url(url)


if __name__ == '__main__':
    my_task()
    # schedule.every().day.at("06:15").do(my_task)
    # schedule.every().day.at("12:15").do(my_task)
    # schedule.every().day.at("18:15").do(my_task)
    # schedule.every().day.at("22:15").do(my_task)
    # while True:
        # 运行待执行的任务
        # schedule.run_pending()
        # time.sleep(1)
