from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import Image
from Screenshot import Screenshot_Clipping
# from PIL import Image
# from StringIO import StringIO
import pandas as pd
import tldextract
# from bs4 import BeautifulSoup
# import re
# import pandas as pd
import pathlib
import os
from webdriver_manager.chrome import ChromeDriverManager
import time
import io

def full_screenshot(driver, save_path):
    # initiate value
    save_path = save_path + '.png' if save_path[-4::] != '.png' else save_path
    img_li = []  # to store image fragment
    offset = 0  # where to start

    # js to get height
    height = driver.execute_script('return Math.max('
                                   'document.documentElement.clientHeight, window.innerHeight);')

    # js to get the maximum scroll height
    # Ref--> https://stackoverflow.com/questions/17688595/finding-the-maximum-scroll-position-of-a-page
    max_window_height = driver.execute_script('return Math.max('
                                              'document.body.scrollHeight, '
                                              'document.body.offsetHeight, '
                                              'document.documentElement.clientHeight, '
                                              'document.documentElement.scrollHeight, '
                                              'document.documentElement.offsetHeight);')
    print(max_window_height)

    # looping from top to bottom, append to img list
    # Ref--> https://gist.github.com/fabtho/13e4a2e7cfbfde671b8fa81bbe9359fb
    count = 0
    while offset < max_window_height:

        # Scroll to height
        driver.execute_script(f'window.scrollTo(0, {offset});')
        # time.sleep(1)
        img = Image.open(io.BytesIO((driver.get_screenshot_as_png())))
        img_li.append(img)
        # print(count,offset,'..........')
        if int(max_window_height /height)-1 == count:
            # print(height,offset,int(max_window_height/height))
            height +=  max_window_height - (offset+height)
            # break
        # print(offset,height)
        count+=1
        offset += height
        # print(offset,max_window_height,'..............')

    # Stitch image into one
    # Set up the full screen frame
    img_frame_height = sum([img_frag.size[1] for img_frag in img_li])
    img_frame = Image.new('RGB', (img_li[0].size[0], img_frame_height))
    offset = 0
    for img_frag in img_li:
        img_frame.paste(img_frag, (0, offset))
        offset += img_frag.size[1]
    img_frame.save(save_path)
ob=Screenshot_Clipping.Screenshot()

#launch url
options = webdriver.ChromeOptions()
# create a new Firefox session
options.add_argument('--headless')
options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument('window-size=1920x1480')
# options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")         
options.add_argument('--disable-dev-shm-usage') 
# from selenium import webdriver

# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# options.add_experimental_option("prefs", prefs)
# driver = webdriver.Chrome(chrome_options=chrome_options)
# options = webdriver.ChromeOptions()
    # pass in headless argument to options
# options.add_argument('--headless')
# options.add_argument('window-size=1920x1480')
# options.add_argument('--no-sandbox')         
# options.add_argument('--disable-dev-shm-usage')        
# driver = webdriver.Remote(
#                 command_executor=f'http://192.168.99.100:4444/wd/hub',
#                 desired_capabilities=DesiredCapabilities.CHROME,options=options)
driver = webdriver.Chrome("/home/giuser/Jeffee/ocr_data_extraction/chromedriver", chrome_options=options)
time.sleep(1.0)

with open('url_list.txt','r') as f:
    url_list = f.read().split('\n')
for count_main,url in enumerate(url_list):
    print(count_main)
    try:
        text_list = []
        text_image_path = []
        driver.get(url)
        # full_screenshot(driver,"webpage_screenshot.png")
        webpage_screenshot = str(tldextract.extract(url).domain)+'_'+str(count_main)
        img_url=ob.full_Screenshot(driver, save_path=r'.', image_name=webpage_screenshot+'.png')

        # driver.save_screenshot("webpage_screenshot.png")
        # list_all = []
        # string_pageText = driver.find_elements_by_tag_name("p")
        # string_pageText.extend(driver.find_elements_by_tag_name("span"))
        # string_pageText.extend(driver.find_elements_by_tag_name("li"))
        # string_pageText.extend(driver.find_elements_by_tag_name("div"))
        # string_pageText.extend(driver.find_elements_by_tag_name("div"))
        string_pageText = driver.find_elements_by_xpath("//*[text()][count(*)=0]")


        # string_pageText = driver.find_elements_by_css_selector('#text-3 > h3')
        # print(string_pageText,'..............')
        # el.screenshot("webpage_screenshot.png")
        im = Image.open(img_url)
        for count,elem in enumerate(string_pageText):
            # print(count,'...........')
            if elem.is_displayed:
                element_text = elem.text
                if element_text:
                    # elem.screenshot('test.png')
                    location = elem.location
                    size = elem.size
                    # print(location,size,elem.text,count)
                    x = location['x']
                    y = location['y']
                    w = size['width']
                    h = size['height']
                    width = x + w
                    height = y + h
                    im_crop = im.crop((int(x), int(y), int(width), int(height)))
                    path = './text_image/'+webpage_screenshot
                    pathlib.Path(path).mkdir(parents=True,exist_ok=True)
                    im_crop.save(path+'/image_'+str(count)+'.png')
                    text_list.append(element_text)
                    text_image_path.append(path+'/image_'+str(count)+'.png')
        df = pd.DataFrame(list(zip(text_image_path,text_list)),columns=['text_image_path','text'])
        df.to_csv('text_image_dataset_'+webpage_screenshot+'_11_03_2020.csv',index=False)
    except:
        pass

driver.quit()