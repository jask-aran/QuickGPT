import requests
import yaml
import argparse
import json
import sys
import os


def config_load():
    with open("config.yml", "r+") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    # Should only be false for first start of program, may add functionality to set to false and clear stored key if a 'bad key' response is returned from the API call
    if config["api-key"] == False:
        option = input("Enter API Key (Found in OpenAI account settings): ")
        print(
            "API key has been stored in newly created api-key.yml file, this file is included in .gitignore to not accidentally be uploaded along with your API Key"
        )

        with open("api-key.yml", "w") as file:
            key = {"api-key": option}
            yaml.dump(key, file)

        config["api-key"] = True

        with open("config.yml", "w") as file:
            yaml.dump(config, file)
        sys.exit(0)

    # The config dictionary is updated at runtime to include the api-key that has been pulled from the api-key.yml file, before being passed on to the rest of the program
    with open("api-key.yml", "r") as file:
        key = yaml.load(file, Loader=yaml.FullLoader)
    config.update(key)
    return config


def config_adjust(prompt):
    with open("config.yml", "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    if prompt.lower() == "model":
        print(
            "Available models: \ngpt-3.5-turbo (1)\ngpt-4 (2) ONLY IF YOUR OpenAI ACCOUNT AND THEREFORE API KEY HAS BEEN GRANTED ACCESS"
        )
        option = input("Enter a number option: ")
        if option == str(1):
            config["model"] = "gpt-3.5-turbo"
            print(
                "Model has been set to gpt-3.5-turbo for all future conversation calls"
            )
        elif option == str(2):
            config["model"] = "gpt-4"
            print("Model has been set to gpt-4 for all future conversation calls")
        else:
            print("Invalid")
            sys.exit(0)

    elif prompt.lower() == "temperature":
        option = float(input("Enter a temperature for the model, between 0 and 2: "))
        if 0 <= option <= 2:
            print(
                "Temperature is now "
                + str(option)
                + " for all future conversation calls"
            )
            config["temperature"] = option

    elif prompt.lower() == "verbose_context":
        print(
            "Enter a contextual system message, used to define the behaviour of the model. This option adjusts context in conversational mode"
        )
        print("The (recomended) default is: You are a helpful assistant")
        option = input("> ")
        config["verbose_context"] = option

    elif prompt.lower() == "quick_context":
        print(
            "Enter a contextual system message, used to define the behaviour of the model. This option adjusts context in inline/ normal mode"
        )
        print(
            "It is recommended to include a direction to limit output to ~30-50 words in this prompt, to avoid cluttering the terminal and ensuring conciseness"
        )
        print(
            "The (recommended) default is: You give concise, short answers to questions in ideally no more than 30 words, unless instructed to expand on your answer."
        )
        option = input("> ")
        config["quick_context"] = option

    with open("config.yml", "w") as file:
        yaml.dump(config, file)


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

    # Create Parser
    parser = argparse.ArgumentParser(description="Chat GPT CLI tool")
    parser.add_argument(
        "-c",
        "--conversation",
        action="store_true",
        help="Enter conversational mode with the entered prompt",
    )
    parser.add_argument(
        "-s",
        "--settings",
        action="store_true",
        help="Adjust settings for config.yml",
    )
    # Prompt, either passed to API call from model, or to settings adjustment if -s flag
    parser.add_argument("Prompt", type=str, nargs="+", help="Prompt Text", default="")
    args = parser.parse_args()
    prompt = " ".join(args.Prompt)

    # Adjust settings using prompt provided
    if args.settings:
        config_adjust(prompt)

    # Enter conversational mode, using the verbose_context from config
    elif args.conversation:
        initialised_message = [
            {"role": "system", "content": config["verbose_context"]},
            {"role": "user", "content": prompt},
        ]
        conversation(config, initialised_message)

    # Return an inline response from the model, using the quick_context from config
    else:
        initialised_message = [
            {"role": "system", "content": config["quick_context"]},
            {"role": "user", "content": prompt},
        ]
        output = get_completion(config, initialised_message)
        print(output["content"])


main()
