import requests
from config import YANDEX_API_KEY, YANDEX_FOLDER_ID

class YandexAssistant:
    def __init__(self):
        self.api_key = YANDEX_API_KEY
        self.folder_id = YANDEX_FOLDER_ID

    def get_answer(self, query: str) -> str:
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "x-folder-id": self.folder_id,
            "Content-Type": "application/json"
        }
        
        data = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite/latest",
            "completionOptions": {
                "stream": False, 
                "temperature": 0.1,
                "maxTokens": 2000
            },
            "messages": [
                {
                    "role": "system", 
                    "text": (
                        "Ты — эксперт по разработке в Bitrix24. Отвечай технически точно. "
                        "Обязательно используй базу знаний документации. "
                        "Правила: Названия полей только в ВЕРХНЕМ РЕГИСТРЕ. "
                        "Название метода всегда в формате сущность.действие (например, crm.deal.add). "
                        "Примеры кода оборачивай в блоки кода Markdown."
                    )
                },
                {"role": "user", "text": query}
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                print(f"DEBUG Yandex API Error: {response.status_code} - {response.text}")
            
            response.raise_for_status()
            result = response.json()
            return result['result']['alternatives'][0]['message']['text']
        except Exception as e:
            print(f"CRITICAL ERROR in YandexAssistant: {e}")
            return "Извините, возникла ошибка при обращении к нейросети."