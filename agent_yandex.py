# ИИ-агент, yandexGPT, yandex_cloud, prompt, тест

import os
import asyncio
import json
from dotenv import load_dotenv
from yandex_gpt_api import gpt_async

load_dotenv()

# Системный промпт
system_prompt = """Ты - полезный AI-ассистент. Ты помогаешь пользователям отвечать на вопросы, 
решать задачи и предоставлять информацию. Будь вежливым, точным, кратким и полезным."""

class ChatSession:
    def __init__(self):
        self.messages = [{"role": "system", "text": system_prompt}]
        
    def add_message(self, role: str, text: str):
        self.messages.append({"role": role, "text": text})
        
    def clear_history(self):
        self.messages = [{"role": "system", "text": system_prompt}]

chat_session = ChatSession()

async def ask_agent(prompt: str) -> str:
    chat_session.add_message("user", prompt)
    
    try:
        # Создаем auth_headers как словарь
        auth_headers = {
            "Authorization": f"Api-Key {os.getenv('YANDEX_API_KEY')}",
            "x-folder-id": os.getenv("YANDEX_FOLDER_ID")
        }
        
        # Получаем ответ
        response_json = await gpt_async(
            auth_headers,           # auth_headers как словарь
            chat_session.messages,  # messages
            0.5,                    # temperature
            200                     # max_tokens
        )
        
        # Парсим JSON и извлекаем текст ответа
        response_data = json.loads(response_json)
        assistant_text = response_data['result']['alternatives'][0]['message']['text']
        
        chat_session.add_message("assistant", assistant_text)
        return assistant_text
        
    except Exception as e:
        return f"Ошибка: {str(e)}"

async def interactive_chat():
    print("🤖 Добро пожаловать в чат с YandexGPT!")
    print("Команды: /clear - очистить историю, /exit - выйти")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nPrompt: ").strip()
            
            if user_input.lower() in ['/exit', '/quit', 'quit', 'exit']:
                print("До свидания!")
                break
            elif user_input.lower() == '/clear':
                chat_session.clear_history()
                print("🗑️ История очищена")
                continue
            elif user_input.startswith('/'):
                print("❌ Неизвестная команда")
                continue
            elif not user_input:
                continue
                
            response = await ask_agent(user_input)
            print(f"🤖 Ассистент: {response}")
            
        except KeyboardInterrupt:
            print("\n\nПрограмма завершена")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")

if __name__ == "__main__":

    asyncio.run(interactive_chat())
