from selenium import webdriver

driver = webdriver.Chrome()


def expand_section(link):
    driver.get(link)
    experience_section = driver.find_element_by_id("experience-section")
    button_section = experience_section.find_element_by_class_name("pv-profile-section__see-more-inline")
    status = button_section.text
    while status is not 'Show fewer experiences':
        button_section.click()
        button_section = experience_section.find_element_by_class_name("pv-profile-section__see-more-inline")
        status = button_section.text
