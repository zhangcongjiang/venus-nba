import time
import uuid

import requests
import schedule
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    driver.implicitly_wait(5)
    # 获取搜索结果
    body = driver.find_element("tag name", "body")
    body.send_keys(Keys.END)  # 模拟按下“End”键

    # 等待一些时间以加载更多数据
    time.sleep(5)  # 这里可以根据您的需求进行调整
    search_results = driver.page_source

    # 检查请求是否成功

    soup = BeautifulSoup(search_results, 'html.parser')
    # 找到所有具有特定类名的标签
    target_tags = soup.find_all('div', class_='article')
    current_datetime = datetime.now()
    date_string = current_datetime.strftime("%Y-%m-%d-%H")
    file_name = f"F:\\notebooks\\其他\\daily\\{date_string}_realgm.md"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("<center>" + date_string + " Daily </center>\n\n")
        i = 1
        for target_tag in target_tags:

            if target_tag.find('p', class_='author-details'):
                news_date = target_tag.find('p', class_='author-details').text
                title = target_tag.find_next('a').text
                img_div = target_tag.find('div', class_='lead-photo')
                img_url = "https://basketball.realgm.com" + img_div.find_next('img').get('src')
                response = requests.get(img_url)

                if response.status_code == 200:
                    # 从响应中获取图像内容
                    image_data = response.content
                    img_id = str(uuid.uuid4())
                    # 将图像保存到本地文件
                    with open(f"F:\\notebooks\\其他\\img\\{img_id}.jpg", "wb") as image_file:
                        image_file.write(image_data)

                article_body = target_tag.find('div', class_='article-body')
                news_text = article_body.text

                file.write(f"{str(i)}. {title}\n")  # 写入标题，注意要加上Markdown标题的格式
                file.write(f"![](F:\\notebooks\\其他\\img\\{img_id}.jpg)")
                file.write(news_text + "\n")  # 写入内容
                i += 1

    with open(file_name, 'r', encoding='utf-8') as f:
        topic = date_string + " realgm Daily"
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
    url = "https://basketball.realgm.com/nba/news"
    request_url(url)


if __name__ == '__main__':
    my_task()
    # schedule.every().day.at("06:00").do(my_task)
    # schedule.every().day.at("12:00").do(my_task)
    # schedule.every().day.at("18:00").do(my_task)
    # schedule.every().day.at("22:00").do(my_task)
    # while True:
    #     # 运行待执行的任务
    #     schedule.run_pending()
    #     time.sleep(1)
