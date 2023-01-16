from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import random
import time

def createDriver() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.headless = True

    chrome_options.add_experimental_option("prefs", prefs)
    myDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return myDriver

def getGoogleHomepage(driver: webdriver.Chrome) -> str:
    driver.get("https://www.google.com")
    return driver.page_source

def getHulan(driver: webdriver.Chrome, topic: str, len: str) -> dict:
    driver.get("https://howtobullshit.me")

    topic_pos = driver.find_element_by_id("topic")
    minlen_pos = driver.find_element_by_id("minlen")

    topic_pos.send_keys(topic)
    minlen_pos.send_keys(len)

    driver.find_element_by_id("btn-get-bullshit").click()
    time.sleep(3)
    content = driver.find_element_by_id("content")

    myDict = {
        "topic": topic,
        "len": len,
        "text": content.text
    }

    return myDict

def drawLots(driver: webdriver.Chrome, topic: str, len: str)-> dict:
    index = "%03d" % (random.randint(1,100))
    driver.get(f"http://www.chance.org.tw/籤詩集/淺草金龍山觀音寺一百籤/籤詩網‧淺草金龍山觀音寺一百籤__第{index}籤.htm")

    luck  = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/p[10]')
    content = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/p[11]')
    conclusion = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/p[12]')

    myDict = {
        "luck": luck.text,
        "content": content.text,
        "conclusion": conclusion.text
    }

    return myDict

def doBackgroundTask(inp):
    print("Doing background task")
    print(inp.msg)
    print("Done")