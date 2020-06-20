from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

web_url = "http://results.cgg.gov.in/TS_First_Year_General.do"
browser = webdriver.Chrome()


browser.get(web_url)
time.sleep(3)

def wait():
	while(1):
		msg = browser.find_element_by_id("msg")
		report = browser.find_element_by_id("report")
		if(msg.text.strip() != '' or report.text.strip() != ''):
			return msg, report

def valid(hallticket, file1, file2):
	hallticket_box = browser.find_element_by_id("hallticket_no")
	hallticket_box.clear()

	result_button =  browser.find_element_by_class_name("button")
	hallticket_box.send_keys(hallticket)
	result_button.click()
	msg, report = wait()
	if msg.text.strip() == '':
		file1.write(hallticket+"\n")
		file2.write(report.text+"\n\n")
		return True
	return False


def getContent():
	i = int(input("Enter district code: "))
	file1 = open('halltickets'+str(i)+'.txt','w')
	file2 = open('data'+str(i)+'.txt','w')
	cnt = 0
	hallticket = "20"
	hallticket += str(i)
	hallticket += "1"
	j = 0
	step = 0
	while(j < 50000):
		stud_id = "00000"+str(j)
		n = len(stud_id)
		stud_id = stud_id[n-5:n]
		print("retrieving "+hallticket+stud_id+" cnt: "+str(cnt)+" step: "+str(step))
		validate = valid(hallticket + stud_id, file1, file2)
		if not validate:
			cnt += 1
		else:
			cnt = 0
			step = 0
		if(cnt >= 20):
			j += 79
			step += 1
			cnt = 0
		if step >= 5:
			break
		j += 1

getContent()
