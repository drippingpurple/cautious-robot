from . import login_utils


class Scraper(object):
    driver = None

    def is_signed_in(self):
        try:
            self.driver.find_element_by_id(login_utils.VERIFY_LOGIN_ID)
            return True
        except:
            pass
        return False

    def __find_element_by_class_name__(self, class_name):
        try:
            self.driver.find_element_by_class_name(class_name)
            return True
        except:
            pass
        return False

    def __find_element_by_xpath__(self, tag_name):
        try:
            self.driver.find_element_by_xpath(tag_name)
            return True
        except:
            pass
        return False

    def __find_enabled_element_by_xpath__(self, tag_name):
        try:
            element = self.driver.find_element_by_xpath(tag_name)
            return element.is_enabled()
        except:
            pass
        return False

    @classmethod
    def __find_first_available_element(cls, *args):
        for element in args:
            if element:
                return element[0]


class Organization(object):
    organization_name = None
    website = None
    industry = None
    type = None

    def __init__(self,
                 name=None,
                 website=None,
                 industry=None,
                 type=None
                 ):
        self.name = name
        self.website = website
        self.industry = industry
        self.type = type


class Experience(Organization):
    start_date = None
    end_date = None
    role_title = None
    duration = None

    def __init__(self,
                 start_date=None,
                 end_date=None,
                 role_title=None,
                 duration=None
                 ):
        self.start_date = start_date
        self.end_date = end_date
        self.role_title = role_title
        self.duration = duration

    def __repr__(self):
        return "{role_title} at {organization} from {start_date} to {end_date} for {duration}".format(
            role_title=self.role_title,
            organization=self.organization_name,
            start_date=self.start_date,
            end_date=self.end_date,
            duration=self.duration
        )


class Education(Organization):
    start_date = None
    end_date = None
    degree = None

    def __init__(self,
                 start_date=None,
                 end_date=None,
                 degree=None):
        self.start_date = start_date
        self.end_date = end_date
        self.degree = degree

    def __repr__(self):
        return "{degree} at {organization} from {start_date} to {end_date}".format(
            degree=self.degree,
            organization=self.organization_name,
            start_date=self.start_date,
            end_date=self.end_date
        )

