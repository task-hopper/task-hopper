import sys
import pkgutil

def compose(directive, command_result):
    if directive == 'message':
        print('__hop_message__')
        print(command_result)
    elif directive == 'instructions':
        print('__hop_instructions__')
        if isinstance(command_result, list):
            for i in command_result:
                print(i)
        else:
            print(command_result)
    elif directive == 'error':
        print('__hop_error__')
        print(command_result)
        sys.exit()
    else:
        print('__hop_error__')
        print('InvalidDirective - failed compose hop.')

# decorator for implementing before / after commands
def command_hooks(func, enabled=True):
    def wrapper(*args, **kwargs):
        compose('message', 'Running before...')
        func(*args, **kwargs)
        compose('message', 'Running after...')

    return wrapper

