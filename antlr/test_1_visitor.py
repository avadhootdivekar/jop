import antlr4
import sys
from antlr4.tree.Trees import Trees
from test_1Lexer import test_1Lexer
from test_1Parser import test_1Parser
from test_1Listener import test_1Listener
from test_1Visitor import test_1Visitor


def run_1 (argv):
    print("Hello world!!")
    inp = antlr4.FileStream(argv[1])
    lexer = test_1Lexer(inp)
    tokens = antlr4.CommonTokenStream(lexer)
    parser =  test_1Parser(tokens)
    tree = parser.almostAll()
    context = tree

    for token in tokens.tokens :
        print("Tokens : " + str(token))
    #listener = test_1Listener()
    listener = customListener()
    global walker
    walker = antlr4.ParseTreeWalker()
    walker.DEFAULT.walk(listener , tree)
    print("\n\ncontext : " + str(context))
    c = tree.getChildren()
    count = tree.getChildCount()
    #s = Trees.ToStringtree(tree , None , parser)
    print("children : " + str(c) + " , count : " + str(count) )
    for i in range(count) : 
        print("Child " + str(i) + " : " + str(tree.getChild(i).getText() )  )
    print("Tree : " + tree.getText())
    print("Trees : " + str(Trees))
    print("\n\n")
    return


class customListener(test_1Listener): 

    def enterRule1(self, ctx: test_1Parser.Rule1Context):
        # global walker
        abc = "" + ctx.getText()
        # walker.DEFAULT.walk(self,ctx)
        print("customListener Rule1 : " + abc)
        return super().enterRule1(ctx)

    
    def enterStrings(self, ctx: test_1Parser.StringsContext):
        # global walker
        abc = ctx.getText()
        # walker.DEFAULT.walk(self,ctx)
        print("customerListener string : " + abc)
        return super().enterStrings(ctx)
    
    def enterLines(self, ctx: test_1Parser.LinesContext):
        # global walker
        abc = ctx.getText()
        # walker.DEFAULT.walk(self,ctx)
        print("customListener lines : " + abc)
        return super().enterLines(ctx)
    

    def enterAlmostAll(self, ctx: test_1Parser.AlmostAllContext):
        # global walker
        abc = ctx.getText()
        # walker.DEFAULT.walk(self,ctx)
        print("customListener almost all: " + abc)
        return super().enterAlmostAll(ctx)


run_1(sys.argv)

