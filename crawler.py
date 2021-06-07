#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import smtplib

from bs4 import BeautifulSoup
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main():
	r = requests.get("https://banqiao.health.ntpc.gov.tw/content/")
	soup = BeautifulSoup(r.text, "lxml")
	res = soup.find("div", {"id": "box_center_content"})

	if "COVID-19" in res.text or "疫苗" in res.text or "接種" in res.text:
		# skip the duplicate content
		post_content = res.text.encode('utf-8')
		with open("./prev_content.txt", "r") as f:
			prev_content = f.read()
		if len(prev_content)>0 and prev_content == post_content:
			return
		with open("./prev_content.txt", "w") as f:
			f.write(post_content)

		mail_content = post_content
		#The mail addresses and password
		sender_address = "sender_address"
		sender_pass = 'sender_pass'
		receiver_address = "receiver_address"
		#Setup the MIME
		message = MIMEMultipart()
		message['From'] = sender_address
		message['To'] = receiver_address
		message['Subject'] = 'Vaccine Tracker Notification'
		message.attach(MIMEText(mail_content, 'plain'))
		#Create SMTP session for sending the mail
		session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
		session.starttls() #enable security
		session.login(sender_address, sender_pass) #login with mail_id and password
		text = message.as_string()
		session.sendmail(sender_address, receiver_address, text)
		session.quit()
		print('Mail Sent!')

if __name__ == '__main__':
	main()
