class InvalidDirective(Exception):
    pass

def compose(directive, command_result):
    if directive == 'message':
        print('__message__')
        print(cmd_result)
    elif directive == 'instructions':
        print('__instructions__')
        for i in command_result:
            print(i)
    else:
        raise InvalidDirective
