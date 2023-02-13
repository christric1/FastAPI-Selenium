from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import os
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

def drawLots()-> dict:
    # 載入資料庫
    mongo_client_ccsue = MongoClient(os.getenv("MONGO_URL"))
    db = mongo_client_ccsue.get_database('Sensoji')
    record = db['Omikuji']

    random = record.aggregate(
        [{"$sample": { "size": 1 }}]
    )

    for item in random:
        myDict = {
            "luck": item["luck"],
            "content": item["content"],
            "src": item["src"]
        }

    return myDict

def getHentai(driver: webdriver.Chrome, topic: str) -> list:
    driver.get("https://www.htmanga2.top/albums.html")

    input = driver.find_element(By.NAME, "q")
    input.send_keys("紅村")
    input.submit()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    )
    
    myList = []
    for index, i in enumerate(element):
        if index == 9:
            break
        obj = i.find_element(By.TAG_NAME, "a")
        myDict["title"] = obj.get_attribute("title")
        myDict["src"] = obj.get_attribute("href")

        myList.append(myDict)

    return myList

def doBackgroundTask(inp):
    print("Doing background task")
    print(inp.msg)
    print("Done")
