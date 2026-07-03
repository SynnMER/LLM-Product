import requests


class OllamaService:

    BASE_URL = "http://localhost:11434"

    def generate(self, prompt: str):
        print("PROMPT LENGTH:", len(prompt))

        try:

            response = requests.post(
                f"{self.BASE_URL}/api/generate",
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=300
            )

            response.raise_for_status()

            return response.json()["response"]

        except Exception as e:

            print("OLLAMA ERROR:")
            print(e)

            return f"Ошибка генерации: {str(e)}"