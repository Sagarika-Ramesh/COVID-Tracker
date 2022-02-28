from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4
import pandas as pd
import time
import numpy as np

url = "https://www.mohfw.gov.in/"
data_headings = ["State/UT","Active Cases","Cured/Discharged/Migrated","Deaths"]
data = []

Options = Options()
Options.add_argument('--headless')
driver = webdriver.Chrome('chromedriver.exe', options=Options)
driver.get(url)
time.sleep(2)
r = driver.page_source
soup = bs4.BeautifulSoup(r, "html.parser")
table_content = soup.find("table",{"class":"statetable table table-striped"})
tbody = table_content.tbody
rows = tbody.find_all("tr")

for i in range(36):
    row = rows[i]
    td = row.find_all("td")
    state = td[1].text
    cases_total = td[2].text
    cured_dis_mig_total = td[4].text
    deaths_total = td[6].text
    data.append([state, cases_total, cured_dis_mig_total, deaths_total])

driver.close()
data = np.array(data)
dataframe = pd.DataFrame(data, columns=data_headings)
dataframe.to_excel("dataset/Covid_data_India.xlsx")
print("Covid File Created!!")
