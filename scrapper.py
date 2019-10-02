import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = 'https://www.amazon.in/dp/B0791YHVMK?pf_rd_p=ef7fc439-1c48-44b1-8eaa-053f869441fe&pf_rd_r=ZHSMVT7675TQTDTC2EQW'
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

mail_id = 'X1'
password = 'password'
to_mail_id = 'X2'
my_price = 3000
title = ''


def price_check():
    page = requests.get(URL, headers=headers)
    content = BeautifulSoup(page.content, 'html.parser')
    global title
    title = (content.find(id='productTitle').get_text()).strip()

    price = content.find(id='priceblock_ourprice').get_text()
    price_int = int(price[2:7].replace(',', ''))

    print(title)
    print(price_int)

    if (price_int < my_price):
        send_mail()


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(mail_id, password)

    subject = "Amazon price drop"
    global title

    body = ' check this link to buy ' + title + "\n" + URL
    msg = f"Subject:{subject} \n\n {body}"

    server.sendmail(mail_id, to_mail_id, msg)

    print("Mail has been sent")

    server.quit()


while(True):
    price_check()
    time.sleep(3600)
