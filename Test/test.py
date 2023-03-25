import os
import yaml
import openai
import argparse
# import readline

DIRNAME = str(os.path.dirname(__file__))
# print("The current directory is: " + DIRNAME)

def config_load():
    with open('config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        if config['api-key'] == "Replace this string with your API key taken from your OpenAI account":
            return False
    return config

openai.api_key = config_load()['api-key']



parser = argparse.ArgumentParser(description="Chat GPT CLI access")
parser.add_argument('Prompt', type=str, nargs='+', help='Prompt Text')
args = parser.parse_args()
prompt = " ".join(args.Prompt)
# print(f'Your prompt is: {prompt}')

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
      messages=[
        {"role": "user", "content": prompt}],
)["choices"][0]["message"]
print("Response: "  + str(response['content']))
print(response)


