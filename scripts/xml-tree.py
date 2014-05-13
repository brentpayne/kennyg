from kennyg.element import RecursiveKeyValueCollector
from kennyg.parser import parse
from kennyg.sax_handler import KennyGSAXHandler

__author__ = 'brent'


def main():
    import sys
    filepath = sys.argv[1]
    with open(filepath, 'r') as fp:
        data = RecursiveKeyValueCollector()
        kgsh = KennyGSAXHandler(action_tree=data)
        parse(fp, kgsh)
        def recursively_print(obj, num=0):
            if hasattr(obj, 'keys'):
                sorted_keys = sorted(obj.keys())
                for key in sorted_keys:
                    print "\t"*num, key
                    recursively_print(obj[key], num+1)
        recursively_print(data)


if __name__ == '__main__':
    main()