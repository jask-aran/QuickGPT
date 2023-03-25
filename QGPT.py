import requests
import yaml
import argparse

def config_load():
    with open('config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        if config['api-key'] == "Replace this string with your API key taken from your OpenAI account":
            return False
    return config
config = config_load()



parser = argparse.ArgumentParser(description="Chat GPT CLI access")
parser.add_argument('Prompt', type=str, nargs='+', help='Prompt Text')
args = parser.parse_args()
prompt = " ".join(args.Prompt)






def get_completion(config, prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['api-key']}",
    }
    body = {"model": config['model'], 
        "messages": [{"role": "system", "content": config['quick_context']},
                     {"role": "user", "content": prompt}],
        "temperature": config['temperature']}
    
    # response = requests.post(
    #         "https://api.openai.com/v1/chat/completions", 
    #         headers=headers, 
    #         json=body
    #     ).json()
    
    response = {'id': 'chatcmpl-6xxbLHmF9H4prvSmsYUuUc0wgfkCS', 'object': 'chat.completion', 'created': 1679748479, 'model': 'gpt-3.5-turbo-0301', 'usage': {'prompt_tokens': 12, 'completion_tokens': 21, 'total_tokens': 33}, 'choices': [{'message': {'role': 'assistant', 'content': "As an AI language model, I don't have a name, but you can call me OpenAI."}, 'finish_reason': 'stop', 'index': 0}]}
    
    return response

print(get_completion(config, prompt)["choices"][0]["message"]["content"])