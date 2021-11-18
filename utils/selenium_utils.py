import os
import sys

from selenium import webdriver


width, height  = (1400, 700)

argument = {
    '--headless': False,
    '--no--sandbox': True,
}

def extract(path, driver=None, how='xpath', attrib="text", multiple=False):
    x = "s" if multiple else ""

    base = "driver.find_element{}_by_{}('{}'){}"

    if multiple:
        expr = base.format(x, how, path, "")
        try:
            result = [
                eval(
                    f'x.get_attribute("{attrib}")' if attrib != "text" else "x.text"
                )
                for x in eval(expr)
            ]
        except Exception:
            result = []

        return [i.strip() for i in result if i]

    if attrib == "text":
        expr = base.format(x, how, path, f".{attrib}")
    else:
        expr = base.format(x, how, path, f'.get_attribute("{attrib}")')

    print(expr)

    try:
        result = eval(expr)
    except Exception:
        result = ""
    return result


class DriverBuilder():
    def __init__(self, driver_path=None, headless=False):
        self.headless = headless
        self.driver_path = driver_path

    def get_driver(self):
        chrome_options = webdriver.ChromeOptions()

        if self.headless:
            argument['--headless'] = True

        for key, val in argument.items():
            if val:
                chrome_options.add_argument(key)
        
        chrome_prefs = {
                "profile.default_content_settings": {"images": 2},
                "profile.managed_default_content_settings": {"images": 2},
        }

        chrome_options.experimental_options["prefs"] = chrome_prefs

        if not self.driver_path:
            dir_path = os.path.dirname(os.path.realpath('__file__'))
            self.driver_path = os.path.join(dir_path, "chromedriver")

            if sys.platform.startswith("win"):
                self.driver_path += ".exe"

        driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=chrome_options)
        driver.set_window_size(width, height)

        return driver 


