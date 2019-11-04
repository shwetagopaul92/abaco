# hello-world.py

from agavepy.actors import get_context

# function to print the message
def say_hello(message):
    print(message)

def main():
    context = get_context()
    message = context['raw_message']
    say_hello(message)

if __name__ == '__main__':
    main()
