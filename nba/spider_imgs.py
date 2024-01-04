import os
import time

import requests


def download_and_rename_image(url, destination_folder, player_name, team, img_id):
    response = requests.get(url)
    time.sleep(3)
    new_filename = os.path.join(destination_folder, f"{player_name}_{team}_{img_id}")
    if response.status_code == 200:

        # 拼接保存路径
        save_path = os.path.join(destination_folder, f"{player_name}_{team}_{img_id}.png")

        # 保存图片
        with open(save_path, 'wb') as f:
            f.write(response.content)
            print(f"图片已成功下载并保存为: {new_filename}.png")
        img_files = sorted(
            [file for file in os.listdir(destination_folder) if file.startswith(f"{player_name}_{team}_2")],
            reverse=True)
        if len(img_files) >= 10:
            for img in img_files[10:]:
                os.remove(os.path.join(destination_folder, img))
                print("删除过时的照片：", img)

    else:
        print(f"无法下载图片，HTTP状态码: {response.status_code}")


if __name__ == '__main__':
    for num in range(1):
        url = 'https://china.nba.cn/cms/v1/news/list'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': 'privacyV2=true; _ga=GA1.2.902210438.1697680174; _ga_H1HTS9RJXW=GS1.2.1697680174.1.1.1697680248.0.0.0; i18next=zh_CN; locale=zh_CN; countryCode=CN; AMCVS_248F210755B762187F000101%40AdobeOrg=1; AMCV_248F210755B762187F000101%40AdobeOrg=-1712354808%7CMCIDTS%7C19676%7CMCMID%7C48517773620589826003359889172843151504%7CMCAAMLH-1700533635%7C9%7CMCAAMB-1700533635%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1699936035s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.3.0; s_cc=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218b370b56581cf-00a9790305208498-26031151-2073600-18b370b565964f%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThiMzcwYjU2NTgxY2YtMDBhOTc5MDMwNTIwODQ5OC0yNjAzMTE1MS0yMDczNjAwLTE4YjM3MGI1NjU5NjRmIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218b370b56581cf-00a9790305208498-26031151-2073600-18b370b565964f%22%7D; acw_tc=0b328f1a16999361542693684ec52f42de0b4308374dc01e31de7e16f43721',
            'Referer': 'https://china.nba.cn/news/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

        params = {
            'column_id': '57',
            'page_size': '24',
            'page_no': f'{num+1}',
            'team_ids': '',
            'app_key': 'tiKB2tNdncnZFPOi',
            'os_type': '3',
            'os_version': '10.0',
            'app_version': '1.0.0',
            'install_id': '202111201544',
            'network': 'wifi',
            't': '1699936213349',
            'device_id': '79db9f4a29d2eed042c4d8f00b1e3ee2',
            'channel': 'nba',
            'sign': '7bede85ffcb18606d4393d50a2321558'
        }

        response = requests.get(url, headers=headers, params=params)
        SRC_PATH = 'F:\\pycharm_workspace\\venus\\nba\\img'
        if response.status_code == 200:
            data = response.json().get('data')
            for msg in data:
                print(msg)
                if len(msg.get('ext').get('players')):

                    player_code = msg.get('ext').get('players')[0].get('player_code')
                    if len(msg.get('ext').get('teams')) == 1:
                        team = msg.get('ext').get('teams')[0].get('team_abbr')
                        news_id = msg.get('news_id')
                        img_url = msg.get('thumbnail_2x')
                        download_and_rename_image(img_url, SRC_PATH, player_code, team, news_id)
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.text)
        time.sleep(10)
