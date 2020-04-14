from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import Image
#from Screenshot import Screenshot_Clipping
import tldextract
# from PIL import Image
# from StringIO import StringIO
import pandas as pd
# from bs4 import BeautifulSoup
# import re
# import pandas as pd
import os
from webdriver_manager.chrome import ChromeDriverManager
import time
import io
def get_driver(address):
    # initialize options
    options = webdriver.ChromeOptions()
# pass in headless argument to options                                                                                                                          
    options.add_argument('--headless')
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument('window-size=1920x1480')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")         
    options.add_argument('--disable-dev-shm-usage') 
    # Pass the argument 1 to allow and 2 to block
    options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)


    # initialize driver
    # driver = webdriver.Remote(
    #             command_executor=f'http://{adhdress}:4444/wd/hub',
    #             desired_capabilities=DesiredCapabilities.CHROME,options=options)
    try:
        #installer = ChromeDriverManager().install()
        driver = webdriver.Chrome("/home/giuser/Jeffee/ocr_data_extraction/chromedriver", chrome_options=options)
    except Exception as ex:
        print("Error === ",ex)

    return driver

def connect_to_base(browser, base_url):
    
    connection_attempts = 0
    while connection_attempts < 4:
        list_url = []
        # description = ''
        try:
            flags = 0
            browser.get(base_url)
        #     response = scrapy.Selector(
        # text=browser.page_source)
            
            
            browser.find_element_by_tag_name('html').send_keys(Keys.END)
            # print('base_url:',base_url)
            # print('current_url:',browser.current_url)
            elems = browser.find_elements_by_xpath("//a[@href]")
            for elem in elems:
                string_href = elem.get_attribute("href")
                if 'http' not in string_href:
                    string_href = browser.current_url + '/'+ string_href
                if tldextract.extract(browser.current_url).domain == tldextract.extract(string_href).domain:
                # if browser.current_url in elem.get_attribute("href"):
                    # print('ffffffffffffffffffffffff')
                    list_url.append(string_href)
                    flags = 1
            list_url.append(browser.current_url)
            
            # about_lists = ['About','About Us','about','About-US','aboutus','about us','Aboutus','AboutUs','about-us','ABOUT','ABOUT US','ABOUTUS']
            # for about in about_lists:
            #     try:
            #         browser.find_elements_by_xpath("//a[text()='"+about+"']")[-1].click()
            #         print('::::::::::::::')
            #         flags = 1                    
            #         print('-------------')
            #         break
            #     except:
            #         pass
            
            if flags == 0:
                return False,[]
                    # return False
            # response = scrapy.Selector(
            # text=browser.page_source)
            # # data = response.xpath('//div/div/p/span/text()').extract()
            # base_url = base_url + 'images/'
            # browser.get(base_url)
            # html = browser.find_element_by_tag_name('html')
            # html.send_keys(Keys.END)
            # while True:
            #     try :
            #         my_style = WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.XPATH,"//*[@id='viewMoreImageBtn']")))
            #         browser.find_element_by_css_selector('#viewMoreImageBtn').click()
            #         print("viewmore is taken.")
            #     except Exception as e:
            #         html = browser.find_element_by_tag_name('html')
            #         html.send_keys(Keys.END)
            #         sleep(0.5)
            #         print(e)
            #         break
            # browser.get(base_url)

            # WebDriverWait(browser, 5).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, 'col-md-6.col-sm-6.col-xs-12.text-center.nm-modelImage'))
            # )
            # browser.find_element_by_css_selector('body > main > div.zw-con.tp-wigt.dpt-30.nm-deviceHeight > div > div > div.col-md-6.col-sm-6.col-xs-12.text-center.nm-modelImage > div > a').send_keys(Keys.ENTER)
            # wait for table element with id = 'hnmain' to load
            # before returning True
            
            
            return True,list_url
        except Exception as ex:
            connection_attempts += 1
            print(f'Error connecting to {base_url}.')
            print(f'Attempt #{connection_attempts}.')
    return False,[]

def run_process(browser,url):
    check,url_list = connect_to_base(browser, url)
    # print(check,'......................')
    # print(url_list,'::::::::::::::::::::::::::')
    url_list = list(set(url_list))
    if check:
        with open('url_list.txt','+a') as f:
            f.write('\n'.join(url_list))
    else:
        return ''

if __name__ == '__main__':
    browser = get_driver(address='192.168.99.100')
        # href,id = sys.argv[1:]
    with open('domain_url.txt','r') as f:
        href_list = f.read().split('\n')
    for href in href_list:
        run_process(browser,href)
