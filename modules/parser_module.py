import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class BitrixParser:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

    def parse_all_sections(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        output_file = os.path.join(root_dir, "bitrix_docs.txt")

        if os.path.exists(output_file):
            os.remove(output_file)

        base_url = "https://apidocs.bitrix24.ru/"
        
        try:
            self.driver.get(base_url)
            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(5)

            start_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Что позволяет REST API')]")))
            self.driver.execute_script("arguments[0].click();", start_link)
            
            page_count = 0
            while True:
                time.sleep(5)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                try:
                    title = self.driver.find_element(By.TAG_NAME, "h1").text
                except:
                    title = "Untitled"

                try:
                    content = self.driver.find_element(By.CSS_SELECTOR, "article, main, .bx-docs-content").text
                except:
                    content = self.driver.find_element(By.TAG_NAME, "body").text

                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"\n[PAGE {page_count+1}: {title}]\n")
                    f.write(f"URL: {self.driver.current_url}\n")
                    f.write(content)
                    f.write("\n" + "="*80 + "\n")

                page_count += 1
                print(f"Parsed: {page_count} | {title}")

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                try:

                    next_button = self.driver.find_element(By.CSS_SELECTOR, "a.dc-nav-toc-panel__link")

                    parent_control = next_button.find_element(By.XPATH, "./..")
                    if "control_right" in parent_control.get_attribute("class"):
                        self.driver.execute_script("arguments[0].click();", next_button)
                    else:
                        next_button = self.driver.find_element(By.XPATH, "//div[contains(@class, 'control_right')]//a")
                        self.driver.execute_script("arguments[0].click();", next_button)
                except:
                    print("Кнопка 'Следующая' не найдена. Завершение.")
                    break

            return output_file
        finally:
            self.driver.quit()

if __name__ == "__main__":
    parser = BitrixParser()
    parser.parse_all_sections()