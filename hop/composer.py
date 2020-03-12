import sys

class Composer:
    def __init__(self):
        self.composition = []

    def add(self, dtype, items):
        directive = {
            'message': '__hop_message__',
            'task': '__hop_task__',
            'warning': '__hop_warning__',
            'error': '__hop_error__'
        }[dtype]
        result = items if isinstance(items, list) else [items]
        self.composition.extend([directive, *result])
        if dtype == 'error': self.compose()

    def compose(self):
        for item in self.composition:
            print(item)
        sys.exit()

composer = Composer()
