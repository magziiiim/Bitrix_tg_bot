from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BitrixParser:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--remote-debugging-port=9222")
        self.options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    def get_method_details(self, url: str):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        try:
            driver.get(url)
            wait = WebDriverWait(driver, 15)

            content_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            title = driver.title
            text_content = driver.find_element(By.TAG_NAME, "body").text

            return {
                "url": url,
                "title": title,
                "description": text_content[:2000]
            }
        except Exception as e:
            print(f"DEBUG Parser Error: {e}")
            return {"error": str(e)}
        finally:
            driver.quit()