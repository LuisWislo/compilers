import wparser
import argparse
import wsemantic
import werrors

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-f', '--file')
    args = argparser.parse_args()

    if(args.file):
        try:

            file = args.file
            source = open(file, 'r')
            code = source.read()
            source.close()
            tree = wparser.parsecode(code)
            print(tree)
            wsemantic.analyze(tree)
            print(wsemantic.tac)
        except(FileNotFoundError):
            print('File does not exist.')
        except werrors.WException as err:
            print(err.message)

main()