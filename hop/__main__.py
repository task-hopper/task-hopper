import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', help='Text to print')
    return parser.parse_args()

def main():
    args = parse_args()
    print(args.text)

if __name__ == '__main__':
    main()
