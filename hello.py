# hello-world.py

from agavepy.actors import get_context

# function to print the message
def echo_message(m):
    print(m)

def main():
    context = get_context()
    message = context['raw_message']
    echo_message(message)

if __name__ == '__main__':
    main()
