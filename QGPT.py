import requests
import yaml
import argparse
import json

def config_load():
    with open('config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        if config['api-key'] == "Replace this string with your API key taken from your OpenAI account":
            return False
    return config

def get_completion(config, messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['api-key']}",
    }
    body = {"model": config['model'], 
            "temperature": config['temperature'],
            "messages": messages
            }
    
    response = {'id': 'chatcmpl-6xxbLHmF9H4prvSmsYUuUc0wgfkCS', 'object': 'chat.completion', 'created': 1679748479, 'model': 'gpt-3.5-turbo-0301', 'usage': {'prompt_tokens': 12, 'completion_tokens': 21, 'total_tokens': 33}, 'choices': [{'message': {'role': 'assistant', 'content': "As an AI language model, I don't have a name, but you can call me OpenAI."}, 'finish_reason': 'stop', 'index': 0}]}
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", 
        headers=headers, 
        json=body
        ).json()

    return response["choices"][0]["message"]


def conversation(config, messages):
    running = 1
    while running == 1:
        output = get_completion(config, messages)
        messages.append(output)
        # print(messages)
        print(output['content'])
        prompt = input("> ")
        if prompt == "/q":
            break
        messages.append({'role': 'user', 'content': prompt})
        
        
def main():
    #Create Parser
    parser = argparse.ArgumentParser(description="Chat GPT CLI tool")
    
    # Mutually exclusive options; memory mode enable/ disable or enter conversational mode
    interaction_mode_group = parser.add_mutually_exclusive_group()
    interaction_mode_group.add_argument('-c', '--conversation', action="store_true", help="Enter conversational mode with the entered prompt")
    interaction_mode_group.add_argument('-m', '--memory', action="store_true", help="Enable/ Disable memory mode to store conversation between inline calls. Call flag again to disable this mode.")
    
    # Positional argument for 
    parser.add_argument('Prompt', type=str, nargs='+', help='Prompt Text', default="")
    args = parser.parse_args()
    
    prompt = " ".join(args.Prompt)
    config = config_load()
    
    initialised_message = [
        {"role": "system", "content": config['quick_context']},
        {"role": "user", "content": prompt}
        ]
    
    if args.conversation:
        initialised_message[0]['content'] = config['verbose_context']
        print('Conversational Mode. Enter "/q" to exit')
        conversation(config, initialised_message)
    elif args.memory:
        print("Memory Cleared")
        with open('history.json', 'w') as history:
            json.dump([], history)
        
    else:
        output = get_completion(config, initialised_message)        
        print(output['content'])
    

    

        
main()