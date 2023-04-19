import schedule
import requests
import time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import json
import datetime 
API_CMT ="http://10.207.112.55:8001/ocr"
API_KM ="http://10.207.112.55:8002/check_face"
ocr ={
    "id_request": "folder_test",
    "user": "VCC"
    }
km ={"id_request": "folder_test"}
def message(subject="He thong eKYC dai hoi co dong"):
    msg = MIMEMultipart()
    # Add Subject
    msg['Subject'] = subject  
 
    try:
        response_ocr = requests.post(API_CMT,json=ocr)
        s= ""
        if response_ocr.status_code == 200:
            s = "API trich xuat thong tin hoat dong binh thuong. Ma code: " + str(json.loads(response_ocr.text)["code"])
        else:
            s = "API trich xuat thong tin hoat dong binh thuong. Ma code: " + str(json.loads(response_ocr.text)["code"])
    except BaseException as e:
        s = "API trich xuat thong tin khong hoat dong"
        print(s)

    try:
        response_km = requests.post(API_KM,json=km)
        s1=""
        if response_km.status_code == 200:
            s1 = "API so khop khuon mat hoat dong binh thuong. Ma code: "+ str(json.loads(response_km.text)["code"])
        else:
            s1 = "API so khop khuon mat hoat dong binh thuong: Ma code: " + str(json.loads(response_km.text)["code"])
    except BaseException as e:
        s1 = "API trich xuat khuon mat khong hoat dong"
        print(s1)
    time.sleep(1)
        
    text = s + "\n"+ s1
    msg.attach(MIMEText(text)) 
    return msg
  
  
def mail():
    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        
        smtp.login('trinhhoanganh0510@gmail.com', 'jczstdzzqntmmuop')
    
        # Call the message function
        msg = message("He thong eKYC dai hoi co dong")
        to = ["dinhquanghuy1107@gmail.com","dangduyhung@gmail.com", "nguyenhuudat031198@gmail.com"]
    
        smtp.sendmail(from_addr="trinhhoanganh0510@gmail.com",
                    to_addrs=to, msg=msg.as_string())
        smtp.quit()  
        date_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print("date and time:",date_time)
    except BaseException as e:
        print("Error", str(e))
    	
# schedule.every(1).minutes.do(mail)
# schedule.every().hour.do(mail)
schedule.every().day.at("08:00").do(mail)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)