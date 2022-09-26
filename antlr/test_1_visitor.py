from mimetypes import common_types
import antlr4
import sys
from antlr4.tree.Trees import Trees


LOG_ERROR               = 1
LOG_WARNING             = 2
LOG_INFO                = 3
LOG_DEBUG               = 4
LOG_VERBOSE             = 5
LOG_FILTER_LEVEL        = 5
SEPERATOR               = '''
------------------------------------------------------------------------------------
'''


from test_1Lexer import test_1Lexer
from test_1Parser import test_1Parser
from test_1Listener import test_1Listener
from test_1Visitor import test_1Visitor

gVarMap={}
gFunMap={}
ASSIGNMENT          = "assign"
DEFAULT             = "default"


def logFallBack(level=0, str=""):
    print(str)

log = logFallBack

def run_1 (argv , log=logFallBack) :
    print("Hello world!!")
    inp = antlr4.FileStream(argv[1])
    lexer = test_1Lexer(inp)
    tokens = antlr4.CommonTokenStream(lexer)
    parser =  test_1Parser(tokens)
    tree = parser.code()
    root_2 = parser.match_b()
    context = tree

    for token in tokens.tokens :
        print("Tokens : " + str(token))
    #listener = test_1Listener()
    listener = customListener()
    global walker
    walker = antlr4.ParseTreeWalker()
    walker.DEFAULT.walk(listener , tree)
    print("\n\ncontext : " + str(context))
    c = tree.getChild(0)
    count = tree.getChildCount()
    #s = Trees.ToStringtree(tree , None , parser)
    # print("children : " + str(c.getChild(2).getText()) + " , count : " + str(count) )
    # for i in range(count) : 
    #     print("Child " + str(i) + " : " + str(tree.getChild(i).getText() )  )
    log(LOG_DEBUG , "Tree : " + (tree.getText()) )
    log(LOG_DEBUG , "Trees : " + str(Trees))
    print("\n\n")
    visitor = customVisitor()
    visitor.visit(root_2)
    visitor.visit(tree)
    print(SEPERATOR + "gVarMap : " + str(gVarMap))
    return


class customListener(test_1Listener): 
    def commonListener(self , ctx) :
        return

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
    

    def enterLine(self, ctx: test_1Parser.LineContext):
        abc = ctx.getText()
        print("customListener line : " + abc)
        return super().enterLine(ctx)
    

    def enterA(self, ctx: test_1Parser.AContext):
        abc = ctx.getText()
        print("customListener a : " + abc)
        return super().enterA(ctx)


    # def enterAlmostAll(self, ctx: test_1Parser.AlmostAllContext):
    #     abc = ctx.getText()
    #     print("customListener almost all: " + abc)
    #     return super().enterAlmostAll(ctx)

    def enterMember(self, ctx: test_1Parser.MemberContext):
        abc = ctx.getText()
        print("customListener member : " + abc)
        return super().enterMember(ctx)


    def enterAssign(self, ctx: test_1Parser.AssignContext):
        abc = ctx.getText()
        print("customListener assign : " + abc)
        return super().enterAssign(ctx)

    def enterMatch_b(self, ctx: test_1Parser.Match_bContext):
        abc = ctx.getText()
        print("customListener match_b : " + abc)
        return super().enterMatch_b(ctx)

    def enterBlock(self, ctx: test_1Parser.BlockContext):
        abc = ctx.getText()
        print("customListener block : " + abc)
        return super().enterBlock(ctx)

    def enterNum(self, ctx: test_1Parser.NumContext):
        abc = ctx.getText()
        print("customListener num : " + abc)
        return super().enterNum(ctx)

    def enterRvalue(self, ctx: test_1Parser.RvalueContext):
        abc = ctx.getText()
        print("customListener rvalue : " + abc)
        return super().enterRvalue(ctx)



class customVisitor(test_1Visitor):
    def visitMatch_b(self, ctx: test_1Parser.Match_bContext , parent_type=DEFAULT):
        self.commonVisitor(ctx , "match_b")
        return super().visitMatch_b(ctx) 
    
    def visitLines(self, ctx: test_1Parser.LinesContext , parent_type=DEFAULT):
        self.commonVisitor(ctx , "Lines")
        print("visitor count : " + str(ctx.getChildCount()) )
        # self.visit()
        return super().visitLines(ctx)

    def visitList_(self, ctx: test_1Parser.List_Context):
        self.commonVisitor(ctx , "LIST_")
        return super().visitList_(ctx)

    def visitCurly(self, ctx: test_1Parser.CurlyContext):
        self.commonVisitor(ctx , "  CURLY : ")
        v = {}
        if ctx.curly() != None :
            for i in range(len(ctx.curly())):
                log(LOG_ERROR , "Getting curly " + str(i))
                v = v | ctx.curly(i).accept(self)
        if ctx.pair() != None : 
            for i in range(len(ctx.pair())) : 
                log(LOG_ERROR , "Getting pair " + str(i) )
                temp_k , temp_v = ctx.pair(i).accept(self)
                v = v | {temp_k : temp_v}
        log(LOG_ERROR , "value for curly : " + str(v) )
        return super().visitCurly(ctx)

    def visitPair(self, ctx: test_1Parser.PairContext):
        self.commonVisitor(ctx, " PAIR : ")
        k = None
        v = None
        if ctx.uid(0) == None:
            log(LOG_ERROR , "UID not found in pair.")
        k = ctx.uid(0).accept(self)

        if (ctx.uid(1) != None):
            log(LOG_DEBUG , "uid value for pair")
            v = ctx.uid(1).accept(self)
        elif (ctx.list_(0) != None ) :
            log(LOG_DEBUG , "curly value for pair")
            v = ctx.list_(0).accept(self)
        elif (ctx.curly(0) != None ) :
            log(LOG_DEBUG , "list value for pair")
            v = ctx.curly(0).accept(self)
        log(LOG_ERROR , "pair key : " + str(k) + " , v : " + str(v) )
        return k , v

    def visitUid(self, ctx: test_1Parser.UidContext):
        self.commonVisitor(ctx , "UID")
        v = None
        if (ctx.num() != None):
            v = ctx.num().accept(self)
        elif (ctx.id_() != None) :
            v = ctx.id_().accept(self)
        elif (ctx.bt() != None):
            v = ctx.bt().accept(self)
        elif (ctx.bf() != None):
            v = ctx.bf().accept(self)
        elif (ctx.strings() != None):
            v = ctx.strings().accept(self)
        log(LOG_DEBUG , "UID value : " + str(v) )
        return v

    def visitAssign(self, ctx: test_1Parser.AssignContext , parent_type=DEFAULT):
        self.commonVisitor(ctx , "Assign")
        value = None
        count = ctx.getChildCount()
        varName = str(ctx.ID())
        if varName in gVarMap:
            print("Assignment variable already declared.")
        try:
            value = ctx.rvalue().accept(self)
            print("Derived rvalue : " + str(value) )
            gVarMap[varName] = ctx.rvalue().accept(self)
        except:
        	print("Failed..")
        # for i in range(0,count):
        #     if ctx.getChild(i).accept(self , parent_type=ASSIGNMENT):
        #         print("Accepted..")
        return super().visitAssign(ctx)

    def visitCode(self, ctx: test_1Parser.CodeContext , parent_type=DEFAULT):
        self.commonVisitor(ctx , "Code")
        return super().visitCode(ctx)

    def visitId_(self, ctx: test_1Parser.Id_Context , parent_type=DEFAULT):
        self.commonVisitor(ctx, "id")
        text = str(ctx.ID())
        if text in gVarMap:
            print("varMap : " + str(gVarMap[text]))
            return gVarMap[text]
        else : 
            log(LOG_DEBUG , "variable not in map : " + text)
        return text
        
    def visitRvalue(self, ctx: test_1Parser.RvalueContext , parent_type=DEFAULT):
        print("Non need to explicitly implement the rvalue, as rvalue would just call one of the OR'd methods.")
        return super().visitRvalue(ctx)

    def visitNum(self, ctx: test_1Parser.NumContext , parent_type=DEFAULT):
        # self.commonVisitor(self, "num")
        num = 0
        if ctx.INT() != None : 
            num = int(str(ctx.INT()))
        else : 
            num = float(str(ctx.FLT()))
        log(LOG_DEBUG , "NUM : " + str(num))
        return (num)

    def visitStrings(self, ctx: test_1Parser.StringsContext):
        self.commonVisitor(ctx , "String")
        return str(ctx.STR())

    def visitBt(self, ctx: test_1Parser.BtContext , parent_type=DEFAULT):
        return True;

    def visitBf(self, ctx: test_1Parser.BfContext , parent_type=DEFAULT):
        return False

    
    def commonVisitor(self, ctx  , ruleName):
        abc = ctx.getText()
        count = ctx.getChildCount()
        print("visitor  :" + ruleName +" : " + abc + " ,  child count : " + str(count)  )        
        try:
            if (count > 0) : 
                for i in range(0,count) : 
                    c = ctx.getChild(i)
                    c.accept(self)
                    # print("done with " + str(c.getText()) )

            else : 
                print("This is termilnal node..")
        except:
            log(LOG_ERROR , "Exception in common visitor..")


def isFunction(param):
    if param in gFunMap:
        return True
    else :
        return False


def isVariable(param):
    if param in gVarMap:
        return True
    else :
        return False


if __name__ == "__main__"  :
    run_1(sys.argv)
else :
    run_1(["test_1_visitor.py","sample.txt"] )


