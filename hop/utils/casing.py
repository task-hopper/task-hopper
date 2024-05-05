from re import sub


def camelcase(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "").replace("*","")

    return ''.join([s[0].lower(), s[1:]])


def snake_case(s):
  return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    s.replace('-', ' '))).split()).lower()
