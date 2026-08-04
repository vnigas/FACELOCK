from openai import OpenAI

client = OpenAI(
    base_url='https://api.tokenrouter.com/v1',
    api_key='sk-DtiOR6KZf288RorFoVF0nNs70k4WhJ3gsWZQyHEVBbrOXHbP',
)

messages = [
    {"role": "system", "content": "You are an intelligent assistant, please reply concisely."},
    {"role": "user", "content": "у тебя есть доступ к папку проекта?"},
]

stream = client.chat.completions.create(
    model="moonshotai/kimi-k3-free",
    messages=messages,
    stream=True,
    stream_options={"include_usage": True},
    extra_body={}
)

content_parts = []
for chunk in stream:
    if chunk.choices:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            content_parts.append(delta.content)

full_content = "".join(content_parts)

print(full_content)

