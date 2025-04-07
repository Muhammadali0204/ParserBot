import time
import requests

from datetime import datetime
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.types import RequestData
from core.config import DATA, settings, bot

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


def login():
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(f"{settings.BASE_URL}/login")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(settings.USERNAME)
        driver.find_element(By.NAME, "password").send_keys(settings.PASSWORD)

        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        time.sleep(5)

        cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        driver.quit()
        
        return session
    except Exception as e:
        print(f"Login amalga oshmadi : {e}")
        return None


def get_data(session: requests.Session):
    response = session.get(settings.BASE_URL)
    if response.status_code != 200:
        session = login()
        if session:
            response = session.get(settings.BASE_URL)
            DATA["session"] = session
            if response.status_code != 200:
                return []
        else:
            return []
        
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="datatable")
    rows = table.find("tbody").find_all("tr")

    parsed_data = []
    for row in rows:
        cols = row.find_all("td")
        stops = [li.get_text(strip=True) for li in cols[5].find_all("li")]
        parsed_data.append({
            "status": False if cols[0].text.strip() == "Expired" else True,
            "time_remaining": int(cols[0].find('span')['data-endtime']),
            "load_id": cols[1].text.strip(),
            "total_distance": float(cols[2].text.strip()),
            "load_start_date": cols[3].text.strip(),
            "load_end_date": cols[4].text.strip(),
            "stops": stops
        })

    return parsed_data

def parse_2_bottext(item: RequestData):
    if item["status"] is True:
        delta_time = item['time_remaining']-time.time()
        text = "Test\n\n"\
        f"⏳Time remaining: {int(delta_time//60)}:{int(delta_time%60)}\n\n"\
        f"🔢Load ID: {item['load_id']}\n📏Total distance: {item['total_distance']} mile\n\n"\
        f"🕐Load start date: {item['load_start_date']}\n🏁Load end date: {item['load_end_date']}\n\n"\
        f"🔴Stops: \n{"\n".join(item['stops'])}\n\n🕐: {datetime.utcnow().strftime("%Y-%m-%d %H:%M")} UTC"
        
        return text
    return None

async def send_message(message):
    await bot.send_message(settings.CHAT_ID, message)
    await bot.session.close()
