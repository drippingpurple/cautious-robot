import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from . import selectors_for_updates
from .scraper import Experience
from .scraper import Education
from .scraper import Scraper


class Manager(Scraper):
    __TOP_CARD = 'pv-top-card'
    __WAIT_FOR_ELEMENT_TIMEOUT = 5

    def __init__(self,
                 linkedin_url=None,
                 name=None,
                 about=None,
                 careers=None,
                 educations=None,
                 current_company=None,
                 current_title=None,
                 driver=None,
                 get=True,
                 scrape=True,
                 close_on_complete=False,
                 ):
        self.linkedin_url = linkedin_url
        self.name = name
        self.about = about or []
        self.careers = careers or []
        self.educations = educations or []

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") is None:
                    driver_path = os.path.join(
                        os.path.dirname(__file__), 'drivers/chromedriver'
                    )
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                    driver = webdriver.Chrome("CHROMEDRIVER")
            except:
                driver = webdriver.Chrome()

        if get:
            driver.get(linkedin_url)

        self.driver = driver

        if scrape:
            self.scrape(close_on_complete)

    def add_careers(self, career):
        self.careers.append(career)

    def add_education(self, education):
        self.educations.append(education)

    def scrape(self, close_on_complete=False):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete)
        else:
            print('Not Logged In')
            self.scrape_logged_in(close_on_complete=close_on_complete)

    def _click_see_more_by_class_name(self, class_name):
        try:
            _ = WebDriverWait(self.driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, class_name)))

            div = self.driver.find_element_by_class_name(class_name)
            div.find_element_by_class_name('pv-profile-section__see-more-inline').click()
        except Exception as e:
            pass

    def scrape_logged_in(self, close_on_complete=False):
        driver = self.driver
        duration = None

        root = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, self.__TOP_CARD)))

        self.name = root.find_element_by_class_name(selectors_for_updates.NAME).text.strip()

        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")

        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight*3/5));")

        self._click_see_more_by_class_name("pv-experience-section__see-more")

        try:
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, "experience-section")))
            exp = driver.find_element_by_id("experience-section")
        except:
            exp = None

        if exp is not None:
            for roles in exp.find_elements_by_class_name("pv-position-entity"):
                role_title = roles.find_element_by_tag_name("h3").text.strip()

                try:
                    company = roles.find_elements_by_tag_name("p")[1].text.strip()
                    duration_area = str(
                        roles.find_elements_by_tag_name("h4")[0]
                        .find_elements_tag_name("span")[1]
                        .text.strip()
                    )
                    start_date = " ".join(duration_area.split(" ")[:2])
                    end_date = " ".join(duration_area.split(" ")[3:])
                    duration = (
                        roles.find_elements_by_tag_name("h4")[1]
                        .find_elements_by_tag_name("span")[1]
                        .text.strip()
                    )

                except:
                    company = None
                    start_date = None
                    end_date = None
                    duration = None

                experience = Experience(
                    role_title=role_title,
                    start_date=start_date,
                    end_date=end_date,
                    duration=duration,
                )
                experience.organization_name = company
                self.add_careers(experience)

            self._click_see_more_by_class_name("pv-education-section__see-more")
            try:
                _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                    expected_conditions.presence_of_element_located(
                        (By.ID, "education-section")))
                edu = driver.find_element_by_id("education-section")

            except:
                edu = None

            if edu:
                for school in edu.find_elements_by_class_name("pv-profile-section__list-item"):
                    university = school.find_element_by_class_name("pv-entity__school-name").text.strip()

                    try:
                        degree = (
                            school.find_element_by_class_name("pv-entity__degree-name")
                            .find_elements_by_tag_name("span")[1]
                            .text.strip()
                        )
                        duration_area = (
                            school.find_element_by_class_name("pv-entity__dates")
                            .find_elements_by_tag_name("span")[1]
                            .text.strip()
                        )
                        start_date, end_date = (duration_area.split(" ")[0], duration_area.split(" ")[2])

                    except:
                        degree = None
                        start_date = None
                        end_date = None

                    education = Education(start_date=start_date, end_date=end_date, degree=degree)
                    education.organization_name = university
                    self.add_education(education)
