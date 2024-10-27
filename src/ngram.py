import argparse 

def main():
    parser = argparse.ArgumentParser(description='This is a n-grams model command line')
    parser.add_argument('filename', type=str, help='Filename of training corpus')
    parser.add_argument('--s', action='store_true', help='Provides a 50 word sample of the text supplied')

    args = parser.parse_args()

    with open(args.filename, 'r') as file:
        content = file.read()
        

    if (args.s):
        print(content[:49])


if __name__ == "__main__":
    main()

