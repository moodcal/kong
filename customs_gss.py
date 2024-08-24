from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time
import csv
import datetime
import pandas as pd
import subprocess

# Step 1: Use Selenium to open the page and get cookies and the verification token
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Runs Chrome in headless mode.
driver = webdriver.Chrome(options=options)

driver.get("http://gss.customs.gov.cn/clsouter2020/Home/ClassifyYCDSearch")

# Get the token from the page source
soup = BeautifulSoup(driver.page_source, 'html.parser')

token_input = soup.find('input', {'name': '__RequestVerificationToken'})
verification_token = token_input['value']

# Get cookies from the browser session
cookies = driver.get_cookies()
driver.quit()
print(cookies)

time.sleep(3)

# Step 2: Convert cookies to a format usable by requests
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# Step 3: Set up headers and payload
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'http://gss.customs.gov.cn/CLSouter2020/Search/GetQuerySearchList',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'X-Requested-With': 'XMLHttpRequest'
}

payload = {
    '__RequestVerificationToken': verification_token,
    'page': 1,  # Example: requesting page 2
    'pageSize': 50,
    'Type': 'YCD',
    'SourceNo': '',
    'GName': '',
    'CodeTS': '',
    'GMdel': '',
    'EngName': '',
    'OtherName': ''
}

# Step 4: Make the POST request with the dynamic token
post_url = "http://gss.customs.gov.cn/CLSouter2020/Search/GetQuerySearchList"
response = session.post(post_url, headers=headers, data=payload)

# Step 5: Check the response
if response.status_code == 200:
    print(response.json())  # or response.json() if the response is JSON
else:
    print("Failed to fetch data:", response.status_code)

data = response.json()['data']  # Change response to response.json()

# Extracting specific fields from each data entry
extracted_data = []
for entry in data:
    extracted_entry = {
        '相关编号': entry['SOURCE_NO'],
        '决定税号': entry['CODE_TS'],
        '商品名称（中文）': entry['G_NAME'],
        '商品名称（英文）': entry['G_NAME_EN'],
        '商品名称（其他）': entry['G_NAME_OTHER'],
        '商品描述': entry['G_DESCRIPTION'],
        '发布单位': entry['DEPARTMENT'],
        # '时间': entry['INURE_TIME']
    }
    extracted_data.append(extracted_entry)

# Converting '/Date(-62135596800000)/' to datetime format
# for entry in extracted_data:
#     entry['时间'] = datetime.datetime.fromtimestamp(int(entry['时间'][6:-2]) / 1000).strftime('%Y-%m-%d %H:%M:%S')

# Writing extracted data to a CSV file with Chinese titles
date_name = datetime.datetime.now().strftime("%Y-%m-%d")
csv_file_path = date_name + '.csv'
excel_file_path = date_name + '.xlsx'

df = pd.DataFrame(extracted_data)
df.to_csv(csv_file_path, index=False)
df.to_excel(excel_file_path, index=False)

# 保存文件后执行以下代码

# 添加文件到暂存区
subprocess.run(["git", "add", "."])

# 提交到本地仓库
subprocess.run(["git", "commit", "-m", "Add new files"])

# 推送到GitHub
subprocess.run(["git", "push", "origin", "main"])