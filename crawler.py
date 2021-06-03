#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import requests
import smtplib

from bs4 import BeautifulSoup
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


r = requests.get("https://banqiao.health.ntpc.gov.tw/content/")
soup = BeautifulSoup(r.text, "lxml")
res = soup.find("div", {"id": "box_center_content"})

if "COVID-19" in res.text or "疫苗接種" in res.text:
	raw = res.find("div", {"id": "date"}).contents
	date = raw[0].split(":")[1]
	current_date = datetime.today().strftime('%Y/%m/%d')
	if current_date == date:		

		mail_content = res.text
		#The mail addresses and password
		sender_address = "sender_address"
		sender_pass = 'sender_pass'
		receiver_address = "receiver_address"
		#Setup the MIME
		message = MIMEMultipart()
		message['From'] = sender_address
		message['To'] = receiver_address
		message['Subject'] = 'A Vaccine alert sent by Dannie.'   #The subject line
		#The body and the attachments for the mail
		message.attach(MIMEText(mail_content.encode('utf-8'), 'plain'))
		#Create SMTP session for sending the mail
		session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
		session.starttls() #enable security
		session.login(sender_address, sender_pass) #login with mail_id and password
		text = message.as_string()
		session.sendmail(sender_address, receiver_address, text)
		session.quit()
		print('Mail Sent!')
