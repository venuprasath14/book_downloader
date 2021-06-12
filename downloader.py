import os
import time
import requests as req
from termcolor import colored
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def download_file(name: str, url: str) -> str:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    browser = Chrome(chrome_options=options)
    print('\nPlease wait, It make take while....')
    browser.get(url)
    print('\nGetting download link....')
    try:
        f = WebDriverWait(browser, 20).until(ec.presence_of_element_located((By.LINK_TEXT, 'Download ( PDF )')))
    except:
        f = browser.find_element_by_link_text('Go to PDF')
    link = str(f.get_attribute('href'))
    print('\nStarting Download.....\n')
    finished = False
    try:
            with open('book.pdf', 'wb') as pdf:
                res = req.get(link, stream=True)
                length = res.headers.get('content-length')
                if length is None:
                    pdf.write(res.content)
                else:
                    downloaded = 0
                    length = int(length)/(1024*1024)
                    for content in res.iter_content(chunk_size=4096):
                        pdf.write(content)
                        downloaded += len(content)/(1024*1024)
                        per = round((downloaded/length)*100)
                        print(f"<|{('█'*round(per/10)).ljust(20, ' ')}|> {per}%  ( {round(downloaded, 2)}MB | {round(length, 2)}MB )", end='\r')
                    finished = True
                    print(colored(f'\n\nDownload Successful...\n\nFile saved at {os.getcwd()}', 'green'))
                    print('\nDon\'t close until program ends....')
    except Exception as err:
            print(colored(err, 'Error happend during downloading ', 'red'))
            os.remove(f'{name}.pdf')
            finished = False
    
    time.sleep(2)
    browser.close()
    os.rename('book.pdf', f'{name}.pdf')
    return finished
