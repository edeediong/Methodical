"""
TEAM B TASK 6
"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=%27computer+science+lecturers%27&after_author=8ZYAAInO__8J&astart=10
# This block of code is used to block the notification popup which is generated by site
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument("--disable-notifications")
# to open chrome webbrowser and maximize the window
DRIVER = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=OPTIONS)
DRIVER.maximize_window()
#Implicit Wait when element is taking time to load
DRIVER.implicitly_wait(20)
# connect to the root web address
DRIVER.get("https://scholar.google.com/citations?view_op=search_authors&mauthors=%27computer+science+lecturers%27&hl=en&oi=drw")
#we define a variable for list of links so that after getting all links
#we loop through it to extract name and h-index
LIST_OF_LINKS = []
TOTAL_NAME = []
TOTAL_BIO = []
TOTAL_H_INDEX = []
H_INDEX_2014 = []
TOTAL_I_10_INDEX = []
I_10_INDEX_2014 = []
TOTAL_CITATIONS = []
USER_IDS = []
#the for loop allows the code to run across 25 pages
#this part is just to collect the urls
for i in range(50):
    print("collecting page "+str(i+1))
    #adds 1 since programming starts counting from 0
    try:
        next_page = DRIVER.find_element_by_xpath("//div/button[2]")
    except NoSuchElementException:
        break
#locates the next page button
    time.sleep(4)
#time.sleep() is to create delay to avoiding google flagging
    profileList = DRIVER.find_elements_by_xpath("//div/h3/a")
    time.sleep(6)
    for profile in profileList:
        time.sleep(3)
        p_url = profile.get_attribute("href")
#this extracts the attribute of h ref which is the profile link
        time.sleep(3)
        LIST_OF_LINKS.append(p_url)
        time.sleep(3)
    next_page.send_keys(Keys.END)
#goes down to where next page is if not stale element error will occur
    next_page.click() #clicks the next page
    time.sleep(10)
print("You have "+str(len(LIST_OF_LINKS))+" queries")
#this is just the beginning of scraping each of them to extract the name and h-index
for each in LIST_OF_LINKS:
    print("collecting data of "+str(int(LIST_OF_LINKS.index(each))+1))
    DRIVER.get(each) #goes to each link
    try:
        h_index_path = "//*[@id='gsc_rsb_st']/tbody/tr[2]/td[2]"
        h_index = DRIVER.find_element_by_xpath(h_index_path).text
        test = int(h_index)
        if(test<10):
            continue
#gets the container of total h-index and the text which is the total h-index
        TOTAL_H_INDEX.append(h_index)
        time.sleep(10)
    except Exception as _e:
        TOTAL_H_INDEX.append("No Data") #inserts no data in list in a case whereby
    try:
        splitted_url = each.split("=en&user=")
        lecturer_id = splitted_url[1]
        USER_IDS.append(lecturer_id)
    except Exception as _e:
        USER_IDS.append("No Data")
    try:
        name_path = "gsc_prf_in"
        name = DRIVER.find_element_by_id(name_path).text
        #gets the container of name and the text which is the name
        TOTAL_NAME.append(name)
        time.sleep(6)
    except Exception as _e:
        TOTAL_NAME.append("No Data")
#inserts no data in list in a case whereby it doesn't find name to prevent the code from crashing
    time.sleep(7)
    try:
        bio_path = "//*[@id='gsc_prf_i']/div[2]"
        bio = DRIVER.find_element_by_xpath(bio_path).text
        TOTAL_BIO.append(bio)
    except Exception as _e:
        TOTAL_BIO.append("No Data")
#it doesn't find h-index to prevent the code from crashing
    try:
        h_index_2014_path = "//*[@id='gsc_rsb_st']/tbody/tr[2]/td[3]"
        each_h_index_2014 = DRIVER.find_element_by_xpath(h_index_2014_path).text
#gets the container of 2014 h-index and the text which is the 2014 h-index
        H_INDEX_2014.append(each_h_index_2014)
        time.sleep(10)
    except Exception as _e:
        H_INDEX_2014.append("No Data")
#inserts no data in list in a case whereby it doesn't find h-index to prevent the code from crashing
    try:
        i_10_index_path = "//*[@id='gsc_rsb_st']/tbody/tr[3]/td[2]"
        i_10_index = DRIVER.find_element_by_xpath(i_10_index_path).text
        #gets the container of h-index and the text which is the h-index
        TOTAL_I_10_INDEX.append(i_10_index)
        time.sleep(10)
    except Exception as _e:
        TOTAL_I_10_INDEX.append("No Data")
#inserts no data in list in a case whereby it doesn't find h-index to prevent the code from crashing
    try:
        i_10_index_2014_path = "//*[@id='gsc_rsb_st']/tbody/tr[3]/td[3]"
        each_i_10_index_2014 = DRIVER.find_element_by_xpath(i_10_index_2014_path).text
        #gets the container of h-index and the text which is the h-index
        I_10_INDEX_2014.append(each_i_10_index_2014)
        time.sleep(10)
    except Exception as _e:
        I_10_INDEX_2014.append("No Data")
#inserts no data in list in a case whereby it doesn't find h-index to prevent the code from crashing
    try:
        each_total_citations_path = "//*[@id='gsc_rsb_st']/tbody/tr[1]/td[2]"
        each_total_citations = DRIVER.find_element_by_xpath(each_total_citations_path).text
        #gets the container of h-index and the text which is the h-index
        TOTAL_CITATIONS.append(each_total_citations)
        time.sleep(10)
    except Exception as _e:
        TOTAL_CITATIONS.append("No Data")
#inserts no data in list in a case whereby it doesn't find h-index to prevent the code from crashing
time.sleep(10)
print(TOTAL_NAME)
print(TOTAL_BIO)
print(TOTAL_H_INDEX)
print(H_INDEX_2014)
print(TOTAL_I_10_INDEX)
print(I_10_INDEX_2014)
print(TOTAL_CITATIONS)
print(USER_IDS)
DF = pd.DataFrame({'Names': TOTAL_NAME,
                   'Scholar ID':USER_IDS,
                   'Bio Data': TOTAL_BIO,
                   'H Index': TOTAL_H_INDEX,
                   'H Index sice 2014': H_INDEX_2014,
                   'I-10 Index': TOTAL_I_10_INDEX,
                   'I-10 Index since 2014': I_10_INDEX_2014,
                   'Citation': TOTAL_CITATIONS,
                   })  #defines columns for storing the Names and H-index using pandas.
DF.to_csv('output1.csv') #specifies the name of the csv file
