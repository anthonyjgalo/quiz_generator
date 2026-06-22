from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


class LLMService:
    def __init__(self, base_url: str, api_key: str, model_name: str) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api_key, base_url=base_url)

    def call_api_model(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.5,
        max_tokens: int = 1500,
        require_json_response: bool = True,
    ):
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=temperature,
            messages=messages,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
            if require_json_response
            else {"type": "text"},
        )

        return response.choices[0].message.content
