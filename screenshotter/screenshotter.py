import os
import time
import selenium
from Screenshot import Screenshot
from getpass import getpass
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

def launch_aws(driver):
    # Open the website
    driver.get("https://console.aws.amazon.com/console/home?nc2=h_ct&amp;src=header-signin")   

def login_aws(driver, usr, pwd):
    username_text = driver.find_element(By.ID,'resolving_input')
    username_text.send_keys(usr)

    next_button = driver.find_element(By.ID,'next_button')
    next_button.click()

    username_text = driver.find_element(By.ID,'password')
    username_text.send_keys(pwd)

    next_button = driver.find_element(By.ID,'signin_button')
    next_button.click()
    
def find_ec2(driver):
    search_text = driver.find_element(By.ID,'awsc-concierge-input')
    search_text.send_keys("ec2")

    ec2_button = driver.find_element(By.CLASS_NAME, "globalNav-search-13141")
    ec2_button.click()

def find_instances(driver):
    instance_button = driver.find_element(By.LINK_TEXT, "Instances")
    instance_button.click()

    driver.switch_to.frame('compute-react-frame')

    search_text = driver.find_element(By.XPATH,"//*[contains(@id, 'input8-')]")

    instances = import_instance_names()

    search_text.send_keys(instances[0])
    search_text.send_keys(Keys.ENTER)

    current_instance = driver.find_element(By.XPATH, "//*[@id='compute-react']/div/div/div/div/div/main/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/table/thead/tr/th[1]")
    current_instance.click()

    instance_summary = driver.find_element(By.XPATH, "//*[contains(text(), 'Instance summary')]")
    instance_summary.click()

    time.sleep(1)

    ob = Screenshot.Screenshot()
    img_url = ob.full_Screenshot(driver, save_path=r'./outputs/EC2', image_name=instances[0]+'.png')

    clear_button = driver.find_element(By.CLASS_NAME, "awsui_remove-all_1wzqe_1mbni_219")
    clear_button.click()

    for instance in instances[1:]:
        search_text.send_keys(instance)
        search_text.send_keys(Keys.ENTER)

        current_instance = driver.find_element(By.XPATH, "//*[@id='compute-react']/div/div/div/div/div/main/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/table/thead/tr/th[1]")
        current_instance.click()

        time.sleep(1)

        ob = Screenshot.Screenshot()
        img_url = ob.full_Screenshot(driver, save_path=r'./outputs/EC2', image_name=instance+'.png')

        clear_button = driver.find_element(By.CLASS_NAME, "awsui_remove-all_1wzqe_1mbni_219")
        clear_button.click()

    driver.switch_to.default_content()
    # driver.implicitly_wait(10)

    # while(True):
    #     pass

def import_instance_names():
    in_file = open('instances.txt', 'r')
    instances = in_file.read()
    instances = instances.split("\n")
    return instances

if __name__ == "__main__":
    # ENTER LOGIN
    usr = ""
    pwd = getpass("Enter password:\n")


    # Using Chrome to access web
    opts = ChromeOptions()
    opts.add_argument("--window-size=1400,900")
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(20)
    launch_aws(driver)
    login_aws(driver, usr, pwd)

    # Comment out unneccessary instances
    find_ec2(driver)
    find_instances(driver)

    driver.close()
    driver.quit()
