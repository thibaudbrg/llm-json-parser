from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

import instructor


class Character(BaseModel):
    name: str
    age: int
    fact: List[str] = Field(..., description="A list of facts about the character")


# enables `response_model` in create call
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required, but unused
    ),
    mode=instructor.Mode.JSON,
)

resp = client.chat.completions.create(
    model="phi3:3.8b-mini-instruct-4k-fp16",
    messages=[
        {
            "role": "user",
            "content": "Tell me about the Harry Potter",
        }
    ],
    response_model=Character,
)

print(resp.model_dump_json(indent=2))
