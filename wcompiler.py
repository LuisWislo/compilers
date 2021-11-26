import wparser
import argparse
import wsemantic
import werrors
import wexecute
import samples

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-f', '--file')
    argparser.add_argument('-s', '--sample')
    args = argparser.parse_args()

    try:
        code = None
        if(args.file != None):
            file = args.file
            source = open(file, 'r')
            code = source.read()
            source.close()
            
        elif(args.sample != None):
            which = int(args.sample)
            code = samples.samples[which]
        
        tree = wparser.parsecode(code)
        wsemantic.analyze(tree)
        print(wsemantic.tac)
        exe = wexecute.Executer(wsemantic.tac)
        print('>> STDOUT BEGIN >>')
        exe.execute()
        print('>> STDOUT END >>')

    except(FileNotFoundError):
        print('[Error]: File does not exist.')
    except(IndexError):
        print('[Error]: No sample found for specified index.')
    except werrors.WException as err:
        print(err.message)

main()