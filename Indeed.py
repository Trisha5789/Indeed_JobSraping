import time

import DateTime.DateTime
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date, datetime

# Chrome options
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument("--incognito")
options.add_argument('--disable-gpu')

# creating driver
driver = webdriver.Chrome(executable_path="C:\Selenium\chromedriver_win32\chromedriver.exe", options=options)

# Opening the URL
url = "https://indeed.com"
driver.get(url)
driver.maximize_window()
wait = WebDriverWait(driver, 5)


# check if there is popup
def popup_close():
    if driver.find_elements_by_class_name('popover-x-button-close').__len__() > 0:
        if driver.find_element_by_class_name('popover-x-button-close').is_displayed():
            driver.find_element_by_class_name('popover-x-button-close').click()


def handle_job_alert():
    if driver.find_elements_by_id('jobalerts').__len__() > 0:
        driver.refresh()


# scrape jobs
def scrape_jobs():
    # locating job title bar
    print(datetime.now())
    search_bar = driver.find_element_by_name("q")
    search_bar.clear()
    # time.sleep(3)
    WebDriverWait(driver, 5)
    # type your job
    keyword = "Postman or APITesting or Selenium or RESTAssured"
    # time.sleep(3)
    search_bar.send_keys(keyword)
    # time.sleep(3)

    # locating where input box
    where_bar = driver.find_element_by_xpath('//*[@id="text-input-where"]')
    # clearing the where input box
    where_bar.send_keys(Keys.CONTROL + "a")
    where_bar.send_keys(Keys.BACKSPACE)

    # click search button
    search_bar.send_keys(Keys.RETURN)
    time.sleep(1)

    date_dropdown = driver.find_element_by_xpath('//*[@id="filter-dateposted"]')
    time.sleep(1)
    date_dropdown.send_keys(Keys.ARROW_DOWN)
    date_dropdown.find_element_by_xpath('//*[@id="filter-dateposted-menu"]/li[1]/a').click()

    time.sleep(1)

    # date_dropdown.find_element_by_xpath('//*[@id="filter-dateposted-menu"]/li[1]/a').click()
    # more_data_url = driver.current_url + "&limit=50"
    # driver.get(more_data_url)

    title = []
    company = []
    location = []
    description = []
    category = []
    link = []
    position_id = []
    date_posted = []

    df_da = pd.DataFrame()

    popup_close()
    exit_var = 2
    while exit_var > 1:
        try:
            popup_close()
            job_cards = driver.find_elements_by_xpath("//*[@class='resultContent']/div/h2/span")
            i = 0

            for job_card in job_cards:
                popup_close()

                job_title = driver.find_elements_by_xpath("//*[@class='resultContent']/div/h2/span").__getitem__(i).text
                # print(f"\nJob Title : {job_title}")
                title.append(job_title)

                job_location = driver.find_elements_by_class_name("companyLocation").__getitem__(i).text
                # print(f" Job location : {job_location}")
                location.append(job_location)

                company_name = driver.find_elements_by_class_name("companyName").__getitem__(i).text
                # print(f"Company Name :{company_name}")
                company.append(company_name)

                job_date_posted = driver.find_elements_by_xpath('//span[@class="date"]').__getitem__(i).text
                date_posted.append(job_date_posted)

                popup_close()
                job_card.click()
                handle_job_alert()
                time.sleep(10)
                driver.switch_to.frame(driver.find_element_by_id("vjs-container-iframe"))
                # job_title = driver.find_element_by_class_name("jobsearch-JobInfoHeader-title-container").text
                if driver.find_elements_by_xpath(
                        "//div[@class='jobsearch-JobDescriptionSection-sectionItem']/div[2]").__len__() > 0:
                    job_type = driver.find_element_by_xpath(
                        "//div[@class='jobsearch-JobDescriptionSection-sectionItem']/div[2]").text
                else:
                    job_type = ""
                    # print(f"Job Category : {job_type}\n")

                category.append(job_type)

                if driver.find_elements_by_xpath('//*[@id="jobDescriptionText"]/div/p[1]').__len__() > 0:
                    job_position_id = driver.find_element_by_xpath('//*[@id="jobDescriptionText"]/div/p[1]').text
                else:
                    job_position_id = ""

                position_id.append(job_position_id)

                # extracting Job description
                job_desc = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text
                # print(f"Job Description : {job_desc}")
                handle_job_alert()
                description.append(job_desc)

                # extraction of Job Link
                if driver.find_elements_by_xpath('//*[@id="applyButtonLinkContainer"]/div/div[1]/a').__len__() > 0:
                    job_link = driver.find_element_by_xpath(
                        '//*[@id="applyButtonLinkContainer"]/div/div[2]/a').get_attribute(
                        'href')
                elif driver.find_elements_by_xpath('//*[@id="indeedApplyWidget"]').__len__() > 0:
                    job_link = driver.find_element_by_xpath('//*[@id="indeedApplyWidget"]').get_attribute(
                        'data-indeed-apply-joburl')
                else:
                    job_link = ""

                link.append(job_link)

                driver.switch_to.default_content()
                i = i + 1

            next_page = driver.find_element_by_xpath('//ul[@class="pagination-list"]//a[@aria-label="Next"]')
            next_page.click()
            time.sleep(10)
        except NoSuchElementException:
            exit_var = 1
            print("end of all pages")

    df_da['Title'] = title
    df_da['Company'] = company
    df_da['Location'] = location
    handle_job_alert()
    df_da['Description'] = pd.Series(description)
    df_da['Category'] = pd.Series(category)
    df_da['Job Link'] = pd.Series(link)
    df_da['Job Position id'] = pd.Series(position_id)
    df_da['Date Posted'] = date_posted
    df_da['Job Extract Date'] = date.today()
    df_da.to_csv(r'C:\Users\trish\Desktop\JobSearch_Indeed.csv', index=False, header=True)

    # driver.close()
    # river.quit()


scrape_jobs()
print(datetime.now())
