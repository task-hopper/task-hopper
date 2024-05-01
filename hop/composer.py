import sys

class Composer:
    def __init__(self):
        self.composition = []

    def add(self, dtype, items):
        directive = {
            'eval': '__hop_eval__',
            'bash': '__hop_bash__',
            'python': '__hop_python__',
            'info': '__hop_info__',
            'warn': '__hop_warn__',
            'error': '__hop_error__'
        }[dtype]
        # TODO: revisit the list vs single
        items = items if isinstance(items, list) else [items]
        self.composition.extend([directive, *items])
        if dtype == 'error': self.compose()

    def compose(self):
        for item in self.composition:
            print(item)
        sys.exit()

#  composer = Composer()
