import openai
import yaml

with open("D:\\chatBotWithOptions\\config.yaml") as f:
    config_yaml = yaml.safe_load(f)  # Use safe_load for safety

openai.api_key = config_yaml['token']

models = openai.Model.list()

for model in models['data']:
    print(model['id'])

messages = [
    {"role": "user", "content": "how to get keys from openai platform"},
]

ans = openai.ChatCompletion.create(
    model="gpt-4",
    max_tokens=2048,
    messages=messages,
)

print(ans)
print(ans["choices"][0]["message"]["content"])
