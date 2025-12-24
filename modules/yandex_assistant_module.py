from yandex_cloud_ml_sdk import YCloudML
from config import YANDEX_API_KEY, YANDEX_FOLDER_ID, ASSISTANT_ID

class YandexAssistant:
    def __init__(self):
        self.sdk = YCloudML(
            folder_id=YANDEX_FOLDER_ID.strip().replace('"', ''),
            auth=YANDEX_API_KEY.strip().replace('"', ''),
        )
        self.assistant = self.sdk.assistants.get(ASSISTANT_ID.strip().replace('"', ''))
        self.thread = self.sdk.threads.create()

    def ask_question(self, user_text):
        try:
            self.thread.write(user_text)
            run = self.assistant.run(self.thread)
            result = run.wait()
            
            if result.message and result.message.parts:
                return str(result.message.parts[0])
            
            return "К сожалению, в документации Bitrix24 нет прямого ответа на этот вопрос."
            
        except Exception as e:
            return f"Ошибка Yandex Cloud: {str(e)}"