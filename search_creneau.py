#!/usr/bin/python
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import re
import smtplib
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PATH = "/local/home/ronan/soft/COVID/chromedriver_linux64/chromedriver"
driver = webdriver.Chrome(PATH)

url = 'https://www.doctolib.fr/vaccination-covid-19/morlaix?ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005&ref_visit_motive_ids[]=7107'
#url = 'https://www.doctolib.fr/vaccination-covid-19/marseille?ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005&ref_visit_motive_ids[]=7107'
driver.get(url)

print(driver.title)
print("..found")

time.sleep(5)

dispo = False

documents = driver.find_elements_by_class_name("dl-search-result-calendar")
for document in documents:
   m = re.search('\d\d:\d\d',document.text)
   if m != None:
     print ('Dispo trouvée',m)
     dispo = True

if dispo == True:

          # -------------------------- Send email to contact
           toaddr = "ronan@colmou.fr"
           fromaddr = "aurocherie3@gmail.com" 
           # instance of MIMEMultipart
           msg = MIMEMultipart()
           # storing the senders email address
           msg['From'] = fromaddr
           # storing the receivers email address
           msg['To'] = toaddr
           # storing the subject
           msg['Subject'] = "Créneau vaccination COVID trouvé"
           # string to store the body of the mail
           body = "Créneau vaccin trouvé sur "+url
           # attach the body with the msg instance
           msg.attach(MIMEText(body, 'plain'))
           # open the file to be sent
           #filename = "result_"+x[1]+"_html.html"
           #attachment = open(filename, "rb")
           # instance of MIMEBase and named as p
           #p = MIMEBase('application', 'octet-stream')
           # To change the payload into encoded form
           #p.set_payload((attachment).read())
           # encode into base64
           #encoders.encode_base64(p)
           #p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
           # attach the instance 'p' to instance 'msg'
           #msg.attach(p)
           # creates SMTP session
           s = smtplib.SMTP('smtp.gmail.com', 587)
           # start TLS for security
           s.starttls()
           # Authentication
           s.login(fromaddr, "auroch")
           # Converts the Multipart msg into a string
           text_mail = msg.as_string()
           # sending the mail
           s.sendmail(fromaddr, toaddr, text_mail)
           # terminating the session
           #attachment.close()
           s.quit()

           print ('Email sent!')
else:
  print('Pas de dispo trouvée')

driver.quit()

