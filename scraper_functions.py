import ssl
import json
import time
from time import sleep
from collections import deque
import selenium.webdriver.remote.webelement
from selenium.webdriver.chrome.options import Options
# import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
# from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import chromedriver_autoinstaller

from access import credentials,urls

class ScrapeBusinessCentral:

    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        chromedriver_autoinstaller.install()

        # Set Chrome options to manage browser behavior
        options = Options()
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')


        # Create a Chrome WebDriver instance
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 60)  # 10 seconds timeout
        self.credentials = [credentials.name, credentials.password]
        # Navigate to a website
        # https://act.epcargo.com/BC_CLI/?company=EP%20Cargo%20Trucking%20CZ&page=4062297&filter=Vehicle_acx.External%20IS%20%270%27%20AND%20Vehicle_acx.%27No.%27%20IS%20%27111002%7c111006%7c111014%7c111025%7c111040%7c111044%7c111056%7c111067%7c111075%7c111077%7c112006%7c112009%7c112018%27&dc=0&bookmark=23%3bmvs9AAJ7BjEAMQAxADAAOAAy
        # "https://act.epcargo.com/BC_CLI/?company=EP%20Cargo%20Trucking%20CZ&node=003dfb46-7078-0000-0c03-1200836bd2d2&page=4062003&dc=0&bookmark=37%3bufo9AAJ7%2f1AAUgAyADIAMAAwADEANQAzADMAAAAAhxAn"
        # "https://act.epcargo.com/BC_CLI/?company=EP%20Cargo%20Trucking%20CZ&node=003dfb46-7078-0000-0c03-1200836bd2d2&page=4062003&dc=0&bookmark=37%3bufo9AAJ7%2f1AAUgAyADIAMAAwADEANQAzADMAAAAAhxAn"  # Replace with the URL of the website you want to access
        self.url = urls.home_url
        self.driver.get(self.url)
        time.sleep(3)

    def login_to_business_central(self):
        print("satrting to login")
        # Find the input element using its CSS selector
        input_element_email = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                          '.form-control.ltr_override.input.ext-input.text-box.ext-text-box')))
        click_next = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                 '.win-button.button_primary.button.ext-button.primary.ext-primary')))
        # Click on the input element to give it focus
        input_element_email.click()
        # Clear the existing content (if any)
        input_element_email.clear()
        # Enter the text "test" into the input element
        input_element_email.send_keys(self.credentials[0])
        click_next.click()

        sleep(1)
        input_element_password = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                             '.form-control.input.ext-input.text-box.ext-text-box')))
        input_element_password.send_keys(self.credentials[1])
        click_next = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                 '.win-button.button_primary.button.ext-button.primary.ext-primary')))
        click_next.click()

        click_no = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                               '.win-button.button-secondary.button.ext-button.secondary.ext-secondary')))
        """click_next = self.driver.find_element(By.CSS_SELECTOR,
                                              '.win-button.button_primary.button.ext-button.primary.ext-primary')"""
        click_no.click()
        # click_next.click()
        sleep(2)
        self.driver.maximize_window()
        # sleep(30)

        iframe = self.driver.find_element(By.CLASS_NAME, 'designer-client-frame')
        self.driver.switch_to.frame(iframe)
        return "logged in", self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                        "/html/body")))

    def filter_by_order_num(self, order_num: str):
        #sleep(3)
        initial_url = self.driver.current_url
        search_button = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                        "/html/body/div[1]/div[2]/form/div/div[2]/div[2]/div/div/nav/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/i")))
        search_field = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                       "/html/body/div[1]/div[2]/form/div/div[2]/div[2]/div/div/nav/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div/input")))

        ActionChains(self.driver).move_to_element(search_button).click().perform()
        print("found search button")
        search_field.click()
        search_field.send_keys(Keys.COMMAND + "a")
        search_field.send_keys(Keys.DELETE)
        sleep(0.25)
        search_field.send_keys(order_num)
        search_field.send_keys(Keys.ENTER)
        while initial_url == self.driver.current_url:
            #print(initial_url,"\n",self.driver.current_url)
            self.driver.current_url


        return f"filtered transportation {order_num}", sleep(1.5)

    def locate_transportation_order_rows(self):

        time.sleep(3)
        result_transportation_orders = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                       "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/table/tbody")))
        tr_webelements = result_transportation_orders.find_elements(By.TAG_NAME, "tr")
        if len(tr_webelements) > 2:
            return "too many rows"
        else:
            for tr_webelement in tr_webelements:

                print(tr_webelement.text)

    def locate_transportation_order_rows_DECORATED(self):
        result_transportation_orders = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                       "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/table/tbody")))
        result = []
        def click_on_tr_webelement(tr_webelement):
            element_to_click_on = tr_webelement.find_elements(By.TAG_NAME, "td")[2]
            ActionChains(self.driver).move_to_element(element_to_click_on).click().perform()
            sleep(.5)
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            #element_to_click_on = table_of_transportation_rows.find_elements(By.TAG_NAME, "td")[2]
            time.sleep(2.5)
        #result_transportation_orders = self.wait.until(EC.presence_of_element_located((By.XPATH,
        #                                                                               "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/table/tbody")))
        tr_webelements = result_transportation_orders.find_elements(By.TAG_NAME, "tr")
        tr_deque = deque(tr_webelements)


        """if len(tr_webelements) > 2:
            return "too many rows"""

        processed_webelements = set()

        while tr_deque:
            if len(tr_deque) > 2:
                return "too many rows"

            # Skip already processed elements
            """"""
            #processed_webelements.add(tr_webelement_deque)
            if len(tr_deque) != 2 and tr_deque[0] == tr_deque[1]:
                result_transportation_orders = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                               "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/table/tbody")))
                tr_webelements = result_transportation_orders.find_elements(By.TAG_NAME, "tr")
                tr_deque = deque(tr_webelements)
                continue

            for index, tr_webelement in enumerate(tr_deque):
                click_on_tr_webelement(tr_webelement)

                if tr_webelement in processed_webelements:
                    continue

        #else:
                """for index,tr_webelement in enumerate(tr_webelements):
                    click_on_tr_webelement(tr_webelement)"""

                element_to_scroll_to = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                       "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[3]")))
                ActionChains(self.driver).move_to_element(element_to_scroll_to).scroll_to_element(
                    element_to_scroll_to).perform()

                # Scroll the element to the right
                self.driver.execute_script("arguments[0].scrollLeft += 1600;", element_to_scroll_to)
                # print("scrolled to -> right for current tranpsortation")

                det_time_value = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                 "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/table/tbody/tr[1]/td[20]/span")))
                det_odometer_value = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                     "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/table/tbody/tr[1]/td[21]/span")))
                order_type = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                             "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/table/tbody/tr[1]/td[3]/span")))
                processed_webelements.add(tr_webelement)

                ActionChains(self.driver).move_to_element(result_transportation_orders).scroll_to_element(
                    result_transportation_orders).perform()
                if index == 0:
                    unloading = det_time_value.get_attribute('title'), det_odometer_value.get_attribute('title'), order_type.get_attribute('title')
                    result.append(unloading)
                elif index == 1:
                    loading = det_time_value.get_attribute('title'), det_odometer_value.get_attribute('title'), order_type.get_attribute('title')
                    result.append(loading)


            return result,self.wait.until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/table/tbody")))


    def locate_transportation_order_rows_DECORATED_2(self):
        result_transportation_orders = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                       "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/table/tbody")))
        result = []
        unique_entries = set()

        def click_on_tr_webelement(tr_webelement) -> list:
            element_to_click_on = tr_webelement.find_elements(By.TAG_NAME, "td")[2]
            transportation_no = element_to_click_on
            text = transportation_no.find_element(By.TAG_NAME, "a").text
            ActionChains(self.driver).move_to_element(element_to_click_on).click().perform()
            sleep(0.5)
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

            return [time.sleep(2.5),text]

        tr_webelements = result_transportation_orders.find_elements(By.TAG_NAME, "tr")
        tr_deque = deque(tr_webelements)

        processed_webelements = set()

        while tr_deque:
            if len(tr_deque) > 2:
                print("too many rows")
                continue

            tr_webelement = tr_deque.popleft()

            # Skip already processed elements
            """if tr_webelement in processed_webelements:
                continue"""
            for tr_deque_element in tr_deque:
                processed_webelements.add(tr_deque_element)
            a = click_on_tr_webelement(tr_webelement)
            #print(a[1])



            element_to_scroll_to = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                   "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[3]")))
            ActionChains(self.driver).move_to_element(element_to_scroll_to).scroll_to_element(
                element_to_scroll_to).perform()
            self.driver.execute_script("arguments[0].scrollLeft += 1600;", element_to_scroll_to)

            det_time_value = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                             "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/table/tbody/tr[1]/td[20]/span")))
            det_odometer_value = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                 "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/table/tbody/tr[1]/td[21]/span")))
            order_type = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                         "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/table/tbody/tr[1]/td[3]/span")))

            ActionChains(self.driver).move_to_element(result_transportation_orders).scroll_to_element(
                result_transportation_orders).perform()

            details = (a[1],det_time_value.get_attribute('title'), det_odometer_value.get_attribute('title'),
                       order_type.get_attribute('title'))

            # Add to result if not already in unique_entries
            if details not in unique_entries:
                unique_entries.add(details)
                result.append(details)

            # Add two new tr_webelements to the deque
            new_tr_webelements = result_transportation_orders.find_elements(By.TAG_NAME, "tr")
            for new_tr in new_tr_webelements:
                if new_tr not in processed_webelements:
                    tr_deque.append(new_tr)

        return result, self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                       "/html/body/div[1]/div[2]/form/div/div[2]/main/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/table/tbody")))