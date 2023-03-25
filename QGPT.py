import argparse

parser = argparse.ArgumentParser(description="Chat GPT CLI access")


parser.add_argument('Prompt', type=str, nargs='+', help='Prompt Text')

# Parse the arguments
args = parser.parse_args()

# Access the arguments
output = " ".join(args.Prompt)
print(f'Your prompt is: {output}')

