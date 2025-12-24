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
            print(f"Открываю сайт: {base_url}")
            self.driver.get(base_url)
            
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(10)

            target_sections = [
                "Что позволяет REST API",
                "Первые шаги",
                "Как получить доступ",
                "Как выполнить запрос",
                "Частые кейсы и сценарии",
                "Локальные решения",
                "Библиотеки для разработки",
                "Настройка и использование",
                "Маркетплейс",
                "Лимиты REST API",
                "Коды ошибок",
                "Поддержка",
                "Обратная связь"
            ]

            for section in target_sections:
                try:
                    print(f"Поиск раздела: {section}")
                    
                    xpath = f"//*[contains(text(), '{section}')]"
                    element = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    time.sleep(2)
                    self.driver.execute_script("arguments[0].click();", element)
                    
                    time.sleep(5)

                    try:
                        content_area = self.driver.find_element(By.TAG_NAME, "main").text
                    except:
                        content_area = self.driver.find_element(By.TAG_NAME, "body").text

                    with open(output_file, "a", encoding="utf-8") as f:
                        f.write(f"SECTION: {section}\n")
                        f.write(content_area)
                        f.write("\n" + "="*50 + "\n")
                    
                    print(f"Успешно сохранено: {section}")

                except Exception as e:
                    print(f"Пропуск раздела '{section}': {str(e)[:100]}")

            print(f"Файл создан по пути: {output_file}")
            return output_file

        finally:
            self.driver.quit()

if __name__ == "__main__":
    parser = BitrixParser()
    parser.parse_all_sections()