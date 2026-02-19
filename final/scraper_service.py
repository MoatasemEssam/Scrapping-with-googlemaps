from fastapi import FastAPI, Query
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dataclasses import dataclass, asdict

app = FastAPI(title="Scraper Service")

@dataclass
class RawLead:
    name: str
    address: str
    raw_data: str
    link: str

class Scraper:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def scrape(self, query: str, limit: int):
        results = []
        try:
            formatted_query = query.replace(" ", "+")
            self.driver.get(f"https://www.google.com/maps/search/{formatted_query}")
            
            # Consent/Feed logic
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))
            
            items = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')
            for item in items[:limit]:
                name = item.get_attribute("aria-label") or "Unknown"
                link = item.find_element(By.TAG_NAME, "a").get_attribute("href") if item.find_elements(By.TAG_NAME, "a") else "N/A"
                raw_text = item.text.replace("\n", " | ")
                results.append(RawLead(name=name, address="Egypt", raw_data=raw_text, link=link))
        finally:
            self.driver.quit()
        return results

@app.get("/scrape")
async def run_scrape(query: str, limit: int = 5):
    s = Scraper()
    data = s.scrape(query, limit)
    return [asdict(d) for d in data]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)