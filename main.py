from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

print('- Finish importing packages')

DRIVER_PATH = ChromeDriverManager().install()
EMAIL = "salluarsh.786@gmail.com"
PASSWORD = "x%$fjm-9R(yHE38"

browser = webdriver.Chrome(DRIVER_PATH)
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
skill_profile = profile+'details/skills/'

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
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@data-field="skill_page_skill_topic"]/div/span/span[1]')))
    skill_elements = browser.find_elements(By.XPATH, '//*[@data-field="skill_page_skill_topic"]/div/span/span[1]')

    for skill in skill_elements:

        # Appending the skills to list
        skills_list_raw.append(skill.text)

print('- Extraction of skills completed')

# Removal of duplicates from list, if any
print('- Removing duplicate skills if any')
all_skills = [*set(skills_list_raw)]

# Creation of dataframe from the list
print('- Creating a dataframe of skills')
df = pd.DataFrame(all_skills, columns=['Skills'])

# Saving the dataframe as csv
print('- Saving the dataframe as csv')
df.to_csv(f"{profile.split('/')[-2]}.csv", index=False)
# print(df)

