import time
import json
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import sys

class TeepublicAutomation:

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "https://teepublic.com/"

    def configure_canvas_element(self, canvas_name, h_align_class, v_align_class, scalar_class, target_value):
        canvas_element = self.driver.find_element(By.XPATH, f'//div[@data-canvas-name="{canvas_name}"]')
        canvas_element.click()

        range_input = self.driver.find_element(By.CLASS_NAME, scalar_class)

        min_range = int(range_input.get_attribute('min'))
        max_range = int(range_input.get_attribute('max'))
        current_value = int(range_input.get_attribute('value'))

        if target_value < min_range:
            target_value = min_range
        elif target_value > max_range:
            target_value = max_range

        difference = target_value - current_value

        if difference < 0:
            range_input.send_keys(Keys.LEFT * abs(difference))
        else:
            range_input.send_keys(Keys.RIGHT * difference)

        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, h_align_class))).click()
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, v_align_class))).click()

    def configure_cut_style(self, canvas_name, cut_style_id, cut_style_value):
        canvas_element = self.driver.find_element(By.XPATH, f'//div[@data-canvas-name="{canvas_name}"]')
        canvas_element.click()

        cut_style_input = self.driver.find_element(By.XPATH, f'//input[@id="{cut_style_id}" and @value="{cut_style_value}"]')
        cut_style_input.click()

    def login(self, email, password):
        self.driver.get(self.base_url)

        try:
            self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'vc-banner__close-icon'))).click()
        
        except NoSuchElementException:
            pass

        self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Log In'))).click()
        
        self.wait.until(
            EC.visibility_of_element_located((By.NAME, 'session[email]'))).send_keys(email)
        
        self.driver.find_element(By.NAME, 'session[password]').send_keys(password)
        self.driver.find_element(By.ID, 'login').click()

    def upload_artwork(self, file_path):
        self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Upload Art'))).click()
        
        try:
            single_upload = self.driver.find_element(By.XPATH, '//div[@data-funnel="single"]')
            single_upload.click()

        except NoSuchElementException:
            pass

        self.wait.until(
            EC.presence_of_element_located((By.NAME, 'file'))).send_keys(file_path)

        WebDriverWait(self.driver, 300).until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, 'm-uploader__dropzone-status'),
                'CHECKING ARTWORK'
            )
        )

        upload_status = self.driver.find_element(By.CLASS_NAME, 'm-uploader__dropzone-status')
        if upload_status.text == "YOUR IMAGE IS TOO SMALL":
            print('Error: YOUR IMAGE IS TOO SMALL')

        time.sleep(5)

    def configure_design_settings(self, entry):
        design_title = entry['title']
        design_description = entry['description']
        primary_tag = entry['primary_tag']
        additional_tags = entry['secondary_tags']
        tshirt_color = entry['tshirt_color']
        tshirt_side = entry['tshirt_side']
        tshirt_scale = entry['tshirt_scale']
        hoodie_color = entry['hoodie_color']
        sticker_cut = entry['sticker_cut']
        magnet_cut = entry['magnet_cut']
        product_scales = entry['product_scales']

        # Set design details
        self.driver.find_element(By.NAME, 'design[design_title]').send_keys(design_title)
        self.driver.find_element(By.NAME, 'design[design_description]').send_keys(design_description)
        self.driver.find_element(By.NAME, 'design[primary_tag]').send_keys(primary_tag)
        self.driver.find_element(By.CLASS_NAME, 'taggle_input').send_keys(additional_tags)

        self.wait.until(
            EC.element_to_be_clickable((By.ID, 'design_content_flag_false'))).click()
        
        #T-Shirt Color
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'jsUploaderApparelScaler')))
        
        range_tshirt = self.driver.find_element(By.CLASS_NAME, 'jsUploaderApparelScaler')

        min_range_tshirt = int(range_tshirt.get_attribute('min'))
        max_range_tshirt = int(range_tshirt.get_attribute('max'))
        current_value_tshirt = int(range_tshirt.get_attribute('value'))
        target_value_tshirt = int(tshirt_scale)

        if target_value_tshirt < min_range_tshirt:
            target_value_tshirt = min_range_tshirt
        elif target_value_tshirt > max_range_tshirt:
            target_value_tshirt = max_range_tshirt

        difference = target_value_tshirt - current_value_tshirt

        if difference < 0:
            range_tshirt.send_keys(Keys.LEFT * abs(difference))
        else:
            range_tshirt.send_keys(Keys.RIGHT * difference)
        
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'jsUploaderApparelHAlign'))).click()

        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'jsUploaderApparelTopAlign'))).click()

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="primary_color_tshirt"]/div/a'))).click()
        
        if tshirt_color == "White":
            self.driver.find_element(By.XPATH, '//div[@id="primary_color_tshirt"]/ul/li[2]/a').click()
        elif tshirt_color == "Black":
            self.driver.find_element(By.XPATH, '//div[@id="primary_color_tshirt"]/ul/li[4]/a').click()

        #Print Side Button
        self.driver.find_element(
            By.XPATH, f'//input[@id="apparel_side_{tshirt_side.lower()}" and @value="{tshirt_side.lower()}"]'
            ).click()

        #Hoodie Color
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="primary_color_hoodie"]/div/a'))).click()
        
        if hoodie_color == "Black":
            self.driver.find_element(By.XPATH, '//div[@id="primary_color_hoodie"]/ul/li[2]/a').click()
        if hoodie_color == "Red":
            self.driver.find_element(By.XPATH, '//div[@id="primary_color_hoodie"]/ul/li[3]/a').click()

        #Baseball Tee Color
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="primary_color_baseballtee"]/div/a'))).click()
        
        self.driver.find_element(By.XPATH, '//div[@id="primary_color_baseballtee"]/ul/li[3]/a').click()

        # Configure Sticker settings
        if sticker_cut == "Auto":
            self.configure_cut_style("Sticker", 'design_mockup_config_sticker_attributes_config_style_auto', 'auto')
        if sticker_cut == "Auto with Background":
            self.configure_cut_style("Sticker", 'design_mockup_config_sticker_attributes_config_style_auto_br', 'auto_br')
        if sticker_cut == "Print":
            self.configure_cut_style("Sticker", 'design_mockup_config_sticker_attributes_config_style_print', 'print')

        # Configure Magnet settings
        if magnet_cut == "Auto":
            self.configure_cut_style("Magnet", 'design_mockup_config_magnet_attributes_config_style_auto', 'auto')
        if magnet_cut == "Auto with Background":
            self.configure_cut_style("Magnet", 'design_mockup_config_magnet_attributes_config_style_auto_bg', 'auto_bg')
        if magnet_cut == "Rectangle":
            self.configure_cut_style("Magnet", 'design_mockup_config_magnet_attributes_config_style_print', 'print')
        if magnet_cut == "Circle":
            self.configure_cut_style("Magnet", 'design_mockup_config_magnet_attributes_config_style_circle', 'circle')

        # Configure other product settings
        for product, scale in product_scales.items():
            h_align_class = f'jsUploader{product}HAlign'
            v_align_class = f'jsUploader{product}VAlign'
            scaler_class = f'jsUploader{product}Scaler'

            if product == "CoffeeMug" or product == "TravelMug":
                product = "Mug"
                self.configure_canvas_element(product, h_align_class, v_align_class, scaler_class, int(scale))  
            else:            
                self.configure_canvas_element(product, h_align_class, v_align_class, scaler_class, int(scale))
    
    def publish_design(self):
        self.driver.find_element(By.XPATH, '//input[@id="terms" and @value="read"]').click()
        self.driver.find_element(By.CLASS_NAME, 'publish-and-promote-button').click()

    def automate_upload_and_publish(self, email, password, json_file):

        self.login(email, password)

        with open(json_file, 'r') as f:
            design_data = json.load(f)
        
        total_files = len(design_data)  # Get the total number of files
        completed_files = 0  # Initialize completed files counter

        for entry in design_data:
            file_path = entry['path']
            self.upload_artwork(file_path)
            self.configure_design_settings(entry)
            self.publish_design()
            time.sleep(3)

            completed_files += 1  # Increment the completed files counter

            # Calculate progress
            progress = (completed_files / total_files) * 100
            filename = entry['title']
            print(f"{filename},{progress:.2f}%")
            sys.stdout.flush()  # Ensure the output is immediately flushed

        self.driver.quit()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    email = config.get("teepublic", "email")
    password = config.get("teepublic", "password")

    automation = TeepublicAutomation()
    automation.automate_upload_and_publish(email, password, "data.json")