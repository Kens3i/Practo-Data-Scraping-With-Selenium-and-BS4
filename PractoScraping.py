#Code Developed By Kens

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import pandas as pd

#opeing chrome from selenium
driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#maximizing the window
driver.maximize_window()

#opening the link
driver.get("https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22doctor%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22type%22%7D%5D&city=Delhi")
time.sleep(30)

#parsing the page via bs4
soup = BeautifulSoup(driver.page_source, "html.parser")

#selecting all doctors
elem_list = soup.find_all("div", {"class":"u-border-general--bottom"})

name=[]
degree=[]
speciality=[]
experience=[]
address=[]
geoLoc=[]
fee=[]

#this function is for extracting each doctors, link by link
def extract(link,name):
    #opening the link
    driver2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver2.maximize_window()
    driver2.get(link)
    time.sleep(5)
    soup2 = BeautifulSoup(driver2.page_source, "html.parser")

    #getting the name
    name.append(soup2.find("h1", {"data-qa-id":"doctor-name"}).text)
    print("Names:", name)

    #getting the degree
    try:
        degree.append(soup2.find("p", {"data-qa-id":"doctor-qualifications"}).text)
    except AttributeError:
        degree.append("NA")
    print("Degree:", degree)

    #getting the address
    address.append(soup2.find("p", {"data-qa-id":"clinic-address"}).text)
    print("Address:", address)

    #getting the address link
    try:
        geoLoc.append(soup2.find("a", {"data-qa-id": "get-directions"}).get("href"))
    except AttributeError:
        geoLoc.append("NA")
    print("Geo Link:", geoLoc)

    try:
    #getting the fees
        feeTemp=soup2.find("span", {"data-qa-id":"consultation_fee"}).text
        feeFinal=""
        #as fees data is mixed with other random elements I am extracting only the number portion
        for f in feeTemp:
            #48 to 57 is ASCII 0-9 so only allowing numbers to add up in the string
            if ord(f) >= 48 and ord(f) <= 57:
                feeFinal=feeFinal+f
            else:
                pass

        fee.append(feeFinal)
    except AttributeError:
        fee.append("NA")

    print("Fees", fee)


for i in elem_list:
    #getting the link for each doctor
    linkP=i.find("div",{"class":"info-section"})
    link=linkP.a.get("href")
    link="https://www.practo.com/"+link

    #here I am extracting elements from the link
    extract(link,name)

    #getting the speciality
    try:
        specP=i.find("div", {"class":"info-section"})
        specP2=specP.find("div", {"class":"u-d-flex"})
        spec=specP2.span.text
        speciality.append(spec)
    except AttributeError:
        speciality.append("NA")
    print("Speciality:", speciality)

    #getting the experience
    try:
        expP=i.find("div", {"data-qa-id":"doctor_experience"})
        exp=expP.div.text
        finalExp=""

        #as experience data is mixed with other random elements I am extracting only the number portion
        for x in exp:
            if ord(x)>= 48 and ord(x)<= 57:
                finalExp=finalExp+x
            else:
                break

        experience.append(finalExp)

    except AttributeError:
        experience.append("NA")

    print("Year of Experience: ", experience)

#converting data to dataframe and then to csv
doctors_df=pd.DataFrame({"Name":name, "Degree":degree, "Speciality":speciality, "Years of Experience":experience, "Clinic Address":address, "Clinic Address Link":geoLoc,"Fees":fee})
print(doctors_df)
doctors_df.to_csv('PractoScrappedData.csv', index=False)