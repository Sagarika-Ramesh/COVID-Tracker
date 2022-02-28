from io import BytesIO
import requests
import PyPDF2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import numpy as np

url = "https://www.mohfw.gov.in/"
Options = Options()
Options.add_argument('--headless')
driver = webdriver.Chrome('chromedriver.exe', options=Options)
driver.get(url)
time.sleep(2)
url = driver.find_element_by_xpath("/html/body/div/div/div/section[1]/div/div/div[2]/div[3]/ul/li/a").get_attribute("href")
driver.close()
print(url)
file = BytesIO(requests.get(url, stream=True).content)
pdf_reader =  PyPDF2.PdfFileReader(file)
page_content = pdf_reader.getPage(0).extractText()
page_content = page_content.split("\n")
page_content = page_content[31:]
page_content = page_content[:-15]

data_headings = ["State/UT","18+ 1st Dose","18+ 2nd Dose","15-18 1st Dose","15-18 2nd Dose","Precaution Dose","Total Doses"]
data = []
i = 0
counter = 0

while counter<38:
    if counter==7:
        state = page_content[i+1] + page_content[i+2]
        i += 1
    else:
        state = page_content[i + 1]
    eighteen_plus_first = page_content[i+2]
    eighteen_plus_second = page_content[i+3]
    eighteen_less_first = page_content[i+4]
    eighteen_less_second = page_content[i+5]
    precaution_dose = page_content[i+6]
    total_doses = page_content[i+7]
    data.append([state, eighteen_plus_first, eighteen_plus_second, eighteen_less_first, eighteen_less_second, precaution_dose, total_doses])
    i += 8
    counter += 1

data = np.array(data)
dataframe = pd.DataFrame(data, columns=data_headings)
dataframe.to_excel("dataset/Vaccine_data_India.xlsx")
print("Vaccination File Created!!")
