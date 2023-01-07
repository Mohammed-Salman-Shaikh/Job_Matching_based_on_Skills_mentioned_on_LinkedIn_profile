import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

print('- Finish importing packages')

DRIVER_PATH = ChromeDriverManager().install()
EMAIL = "Your Email"
PASSWORD = "Your Password"

options = Options()
options.add_argument("--start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-session-crashed-bubble")
options.add_argument("--disable-notifications")
options.add_argument("--suppress-message-center-popups")
options.add_argument('--disable-logging')
options.add_argument("--disable-translate")
options.add_argument("--no-first-run")
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("disable-infobars")
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-logging", "test-type"])

MAX_JOBS = 10

browser = webdriver.Chrome(DRIVER_PATH, options=options)
print('- Finish initializing a driver')

wait = WebDriverWait(browser, 60)

# Task 1: Login to Linkedin

# Task 1.1: Open Chrome and Access Linkedin login site
browser.get("https://www.linkedin.com/")

# Task 1.2: Key in login credentials
wait.until(EC.presence_of_element_located((By.NAME, 'session_key')))
browser.find_element(By.NAME, 'session_key').send_keys(EMAIL)
print('- Finish keying in email')

wait.until(EC.presence_of_element_located((By.NAME, 'session_password')))
browser.find_element(By.NAME, 'session_password').send_keys(PASSWORD)
print('- Finish keying in password')

# Task 1.2: Click the Login button
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sign-in-form__submit-button')))
login_button = browser.find_element(By.CLASS_NAME, 'sign-in-form__submit-button')
login_button.click()

print('- Finish Task 1: Login to Linkedin')

# Goto user profile
profile = input('Enter Linkedin profile link: ')
# profile = 'https://www.linkedin.com/in/username/'
skill_profile = profile + 'details/skills/'

# Opening the link
browser.get(skill_profile)
print('- Opened the skills details page')
skills_list_raw = []  # Empty list to further append the data

# Extracting the skill categories from top to traverse them
wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main"]/section/div[2]/div/button')))
skill_category_buttons = browser.find_elements(By.XPATH, '//*[@id="main"]/section/div[2]/div/button')
print('- Now Extracting skills from profile')

# Traversing the buttons
for button in skill_category_buttons:
    button.click()

    # Extracting the skills from the particular category
    wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@data-field="skill_page_skill_topic"]/div/span/span[1]')))
    skill_elements = browser.find_elements(By.XPATH, '//*[@data-field="skill_page_skill_topic"]/div/span/span[1]')

    for skill in skill_elements:
        # Appending the skills to list
        skills_list_raw.append(skill.text)

print('- Extraction of skills completed')

# Removal of duplicates from list, if any
print('- Removing duplicate skills if any')
all_skills = [*set(skills_list_raw)]

# To remove any empty value from the list
if "" in all_skills:
    all_skills.remove("")

# Creation of dataframe from the list
print('- Creating a dataframe of skills')
df = pd.DataFrame(all_skills, columns=['Skills'])

# Saving the dataframe as csv
print('- Saving the dataframe as csv')
df.to_csv(f"{profile.split('/')[-2]}.csv", index=False)

search_skill = input("Enter the Job Role: ")
location_skill = input("Enter the Loaction: ")
# search_skill = "Software Developer"
# location_skill = "Vadodara, Gujarat, India"

browser.get("https://www.linkedin.com/jobs/")

wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="relative"]/input')))
skill_search = browser.find_element(By.XPATH, '//*[@class="relative"]/input')
skill_search.click()
skill_search.send_keys(search_skill)
time.sleep(1)
skill_search.send_keys(Keys.ENTER)
# location_search = browser.find_element(By.XPATH, '//*[@id="jobs-search-box-location-id-ember25"]')
# location_search.send_keys(location_skill)
# time.sleep(1)
# location_search.send_keys(Keys.ENTER)

max_flag = False
page_counter = 1
job_links = []


def look_for_skills():
    time.sleep(3)
    wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@class="scaffold-layout__list-container"]/li')))
    wait.until(
        EC.visibility_of_all_elements_located((By.XPATH, '//*[@class="scaffold-layout__list-container"]/li')))
    job_cards = browser.find_elements(By.XPATH, '//*[@class="scaffold-layout__list-container"]/li')
    for job_card in job_cards:
        try:
            job_card.click()
            # getting the tile and the URL of the job
            time.sleep(1)
            details_text = browser.find_element(By.ID, 'job-details').text
            for skill in df.values.tolist():
                if skill[0] in details_text:
                    print(skill[0])
                    job_links.append(
                        'https://www.linkedin.com/jobs/view/' + job_card.get_attribute('data-occludable-job-id'))
                    print('https://www.linkedin.com/jobs/view/' + job_card.get_attribute('data-occludable-job-id'))
                    print("found")
                    break
        except Exception as error:
            print(f"Error while traversing a record \n{error}")


look_for_skills()
while True:
    if MAX_JOBS <= len(job_links):
        print(len(job_links))
        print(MAX_JOBS)
        print("Task Completed")
        profile_jobs_df = pd.DataFrame({'Job Links': job_links})
        profile_jobs_df.to_csv(f"Job_Links_for_{search_skill}.csv", index=False)
        print(f"Data Scraped in: Job_Links_for_{search_skill}.csv")
        break
    else:
        print(f"Incomplete job list {len(job_links)}")
        page_counter = page_counter+1
        wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@aria-label="Page {page_counter}"]')))
        next_page_button = browser.find_element(By.XPATH, f'//*[@aria-label="Page {page_counter}"]')
        next_page_button.click()
        look_for_skills()
