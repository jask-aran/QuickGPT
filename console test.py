import cmd
import argparse

class MyConsole(cmd.Cmd):
    prompt = '> '

    def do_hello(self, arg):
        print('Hello, world!')

    def do_quit(self, arg):
        return True

if __name__ == '__main__':
    console = MyConsole()
    console.cmdloop('Welcome to the console!')



parser = argparse.ArgumentParser(description="Chat GPT CLI access")
parser.add_argument('Prompt', type=str, nargs='+', help='Prompt Text')
args = parser.parse_args()
prompt = " ".join(args.Prompt)
print(f'Your prompt is: {prompt}')