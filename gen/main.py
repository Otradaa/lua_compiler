import sys
from antlr4 import *
from LuaLexer import LuaLexer
from LuaParser import LuaParser
from LuaBaseListener import LuaBaseListener


def main():#(argv):
    input_stream = FileStream('../tests/bubble.lua')#argv[1])
    lexer = LuaLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LuaParser(stream)
    tree = parser.chunk()

    output = open("output.pir", "w")
    my_output = ''
    printer = LuaBaseListener(my_output, output)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    output.close()
    print(printer.output)


if __name__ == '__main__':
    #main(sys.argv)
    main()