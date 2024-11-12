import sys 
import time
import os
import json
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

geckodriver_path = "/media/deekshith/98780182-61f7-48a6-8b81-ceba0d56e430/College/Project/Dependencies/geckodriver-v0.35.0-linux64/geckodriver"
crawled_data = {}

# Function to store HTML responses and additional information
def store_response(url, response, session_number, method="GET", status_code=200, cookies=None, headers=None):
    domain = url.split("//")[-1].split("/")[0]

    if domain not in crawled_data:
        crawled_data[domain] = []

    entry = {
        "url": url,
        "http_method": method,
        "status_code": status_code,
        "cookies": cookies,
        "headers": headers,
        "html_content": response
    }

    crawled_data[domain].append(entry)

    with open("second_crawled.json", "w", encoding="utf-8") as f:
        json.dump(crawled_data, f, ensure_ascii=False, indent=4)

def extract_input_fields(soup):
    input_fields = []
    file_upload_fields = []

    forms = soup.find_all('form')
    for form in forms:
        for input_tag in form.find_all('input'):
            input_type = input_tag.get('type', 'text')
            input_name = input_tag.get('name', '')
            if input_type == 'file':
                file_upload_fields.append(input_name)
            else:
                input_fields.append(input_name)

    return input_fields, file_upload_fields

def crawl_with_login(driver, base_url, session_number):
    visited_urls = set()
    to_visit = [base_url]

    while to_visit:
        url = to_visit.pop(0)
        if url in visited_urls:
            continue

        driver.get(url)
        time.sleep(2)
        response_text = driver.page_source

        status_code = driver.execute_script("return window.document.readyState")  # Assuming page load status
        cookies = driver.get_cookies()
        headers = driver.execute_script("return JSON.stringify(window.performance.getEntries())")  # Example for headers

        store_response(url, response_text, session_number, method="GET", status_code=200, cookies=cookies, headers=headers)
        
        soup = BeautifulSoup(response_text, 'html.parser')

        input_fields, file_upload_fields = extract_input_fields(soup)

        for link in soup.find_all('a', href=True):
            new_url = urljoin(base_url, link['href'])
            if base_url in new_url and new_url not in visited_urls:
                to_visit.append(new_url)

        visited_urls.add(url)


def crawl_and_find_login(base_url, driver, session_number):
    """
    Function to crawl the website and find the login page.
    Assumes that the login page has forms with input fields such as 'username' or 'password'.
    """
    visited_urls = set()
    to_visit = [base_url]

    while to_visit:
        url = to_visit.pop(0)
        if url in visited_urls:
            continue

        driver.get(url)
        response_text = driver.page_source

        soup = BeautifulSoup(response_text, 'html.parser')
        forms = soup.find_all('form')

        for form in forms:
            inputs = form.find_all('input')
            input_names = [input_tag.get('name', '').lower() for input_tag in inputs]

            # Check if the form contains fields that are likely related to login
            if any("user" in name for name in input_names) and any("pass" in name for name in input_names):
                print(f"Session {session_number} - Login form found at: {url}")
                return url  # Return the login page URL

        for link in soup.find_all('a', href=True):
            new_url = urljoin(base_url, link['href'])
            if base_url in new_url and new_url not in visited_urls:
                to_visit.append(new_url)

        visited_urls.add(url)

    print(f"Session {session_number} - No login form found.")
    return None  # Return None if no login form is found


def login_to_application(driver, login_url, username, password, session_number):
    """
    Logs into the web application by filling the login form and submitting it.
    """
    driver.get(login_url)

    # Find input fields for username and password
    try:
        username_field = driver.find_element(By.NAME, "username")  # Adjust 'username' as per the actual input name attribute
        password_field = driver.find_element(By.NAME, "password")  # Adjust 'password' as per the actual input name attribute

        # Enter the credentials
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Submit the form
        password_field.submit()

        print(f"Session {session_number} - Logged in successfully with username: {username}")

    except Exception as e:
        print(f"Session {session_number} - Error during login: {e}")


def main(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        url = lines[5].strip()  # 6th line is the 2nd URL
        username = lines[6].strip()  # 7th line is the 2nd username
        password = lines[7].strip()  # 8th line is the 2nd password

    base_url = url.strip()
    if not base_url.startswith('http'):
        base_url = 'http://' + base_url

    try:
        options = Options()
        options.headless = True

        service = Service(executable_path=geckodriver_path)
        driver = webdriver.Firefox(service=service, options=options)

        login_url = crawl_and_find_login(base_url, driver, session_number=2)

        if login_url:
            login_to_application(driver, login_url, username, password, session_number=2)
            crawl_with_login(driver, base_url, session_number=2)
        else:
            print(f"Session 2 - No login page found on the website.")

    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    input_file = sys.argv[1]
    main(input_file)

