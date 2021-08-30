from . import login_utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep


#  loads login information from ../configuration.txt
def load_email_and_password():
    file = open('configuration.txt', 'r')
    lines = file.readlines()
    username = lines[0]
    password = lines[1]
    file.close()
    return username, password


def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'


def login(driver, cookie=None, timeout=10):
    if cookie is not None:
        return _login_with_cookie(driver, cookie)

    email, password = load_email_and_password()

    driver.get('https://www.linkedin.com/uas/login')
    element = WebDriverWait(driver, timeout).until(expected_conditions.presence_of_element_located((By.ID, 'username')))

    driver.find_element_by_id('username').send_keys(email)
    sleep(3)
    driver.find_element_by_id('password').send_keys(password)
    sleep(3)
    driver.find_element_by_id('password').submit()

    try:
        if driver.url == 'https://www.linkedin.com/checkpoint/lg/login-submit':
            remember = driver.find_element_by_id(login_utils.REMEMBER_PROMPT)
            if remember:
                remember.submit()
            element = WebDriverWait(driver, timeout).until(expected_conditions.presence_of_element_located((By.ID, login_utils.VERIFY_LOGIN_ID)))
    except: pass


def _login_with_cookie(driver, cookie):
    driver.get('https://www.linkedin.com/uas/login')
    driver.add_cookie({
        'name': 'li_at',
        'value': cookie
    })
