import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"

messages = [
    {
        "role": "system",
        "content": "あなたは親身な心理カウンセラーです。ユーザーの悩みに優しく寄り添って回答してください。",
    }
]

while True:
    user_input = input("あなた: ").strip()

    if user_input == "終了":
        break

    messages.append({"role": "user", "content": user_input})

    try:
        response = requests.post(
            API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            },
            data=json.dumps(
                {
                    "model": "gpt-4o-mini",
                    "messages": messages,
                }
            ),
        )
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        print(f"AIカウンセラー: {reply}")
        messages.append({"role": "assistant", "content": reply})

    except requests.exceptions.RequestException as e:
        print(f"通信エラーが発生しました: {e}")
    except (KeyError, IndexError) as e:
        print(f"APIレスポンスの処理中にエラーが発生しました: {e}")
