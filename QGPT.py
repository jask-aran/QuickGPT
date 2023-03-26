import requests
import yaml
import argparse
import json
import sys


def config_load():
    with open("config.yml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        if (
            config["api-key"]
            == "Replace this string with your API key taken from your OpenAI account"
        ):
            return False
    return config


def get_completion(config, messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['api-key']}",
    }
    body = {
        "model": config["model"],
        "temperature": config["temperature"],
        "messages": messages,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=body,
    ).json()

    return response["choices"][0]["message"]


def conversation(config, messages):
    print('Conversational Mode. Enter "/q" to exit.')
    output = get_completion(config, messages)
    messages.append(output)
    print(output["content"])
    prompt = input("> ")
    while True:
        if prompt == "/q":
            sys.exit(0)
        elif prompt == "/s":
            print("Saving most recent message from the LLM to message.txt")
            recent = messages[-1]["content"]
            with open("message.txt", "w") as file:
                file.write(recent)
            prompt = input("> ")
        elif prompt == "/d":
            print("Dumping message history from the LLM to history.json")
            messages.append(
                {"role": "user", "content": "Commanded to dump history and exit"}
            )
            with open("history.json", "w") as file:
                json.dump(messages, file)
            sys.exit(0)
        else:
            messages.append({"role": "user", "content": prompt})
            output = get_completion(config, messages)
            messages.append(output)
            print(output["content"])
            prompt = input("> ")


def main():
    config = config_load()
    if not config:
        print("API key has not been provided, please update it in the config.yml file")
        sys.exit(0)

    # Create Parser
    parser = argparse.ArgumentParser(description="Chat GPT CLI tool")
    parser.add_argument(
        "-c",
        "--conversation",
        action="store_true",
        help="Enter conversational mode with the entered prompt",
    )

    # Positional argument for prompt
    parser.add_argument("Prompt", type=str, nargs="+", help="Prompt Text", default="")
    args = parser.parse_args()

    prompt = " ".join(args.Prompt)

    if args.conversation:
        initialised_message = [
            {"role": "system", "content": config["verbose_context"]},
            {"role": "user", "content": prompt},
        ]
        conversation(config, initialised_message)
    else:
        initialised_message = [
            {"role": "system", "content": config["quick_context"]},
            {"role": "user", "content": prompt},
        ]
        output = get_completion(config, initialised_message)
        print(output["content"])


main()
