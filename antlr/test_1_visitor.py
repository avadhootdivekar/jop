from curses import tigetflag
from http.client import RESET_CONTENT
from mimetypes import common_types
from statistics import variance
from syslog import LOG_ERR
import antlr4
import sys
from antlr4.tree.Trees import Trees


LOG_ERROR               = 1
LOG_WARNING             = 2
LOG_INFO                = 3
LOG_DEBUG               = 4
LOG_VERBOSE             = 5
LOG_FILTER_LEVEL        = 5
RET_FAILURE             = -1
RET_SUCCESS             = 0
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
PTYPE_DEFAULT       = "default"
PTYPE_MEMBER        = "member"
PTYPE_GET_TREE      = "get_tree"

def logFallBack(level=0, str1="" , tid="000OO"):
    print( "<< check "+str(tid) + " >> " + str1)

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
    p = visitor.visit(tree)
    print(SEPERATOR + "gVarMap : " + str(gVarMap) + "\nvisitor return : p:" + str(p) )
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
        return RET_SUCCESS, super().visitMatch_b(ctx) 

    def visitMath_b_op(self, ctx: test_1Parser.Math_b_opContext):
        val = ""
        retCode = RET_FAILURE
        if ctx.P() != None:
            val = "+"
            retCode = RET_SUCCESS
        elif ctx.N() != None:
            val = "-"
            retCode = RET_SUCCESS
        elif ctx.M() != None:
            val = "*"
            retCode = RET_SUCCESS
        elif ctx.D() != None:
            val = "/"
            retCode = RET_SUCCESS
        if val =="" :
            log(LOG_WARNING , "Unexpected binary operator. " , tid="100af")
        return retCode, val
    
    def visitLines(self, ctx: test_1Parser.LinesContext , parent_type=DEFAULT):
        self.commonVisitor(ctx , "Lines")
        print("visitor count : " + str(ctx.getChildCount()) )
        # self.visit()
        return super().visitLines(ctx)

    def visitList_(self, ctx: test_1Parser.List_Context):
        self.commonVisitor(ctx , "LIST_")
        v = []
        count = ctx.getChildCount()
        retCode = RET_FAILURE
        # log(LOG_DEBUG , "list tokens : " + str(ctx.getTokens()))
        for i in range(count-1):
            if i==0:
                # Skip Opening and closing brackets.
                continue;
            node = ctx.getChild(i)
            log(LOG_DEBUG , "list node : " + node.getText())
            if (node.accept(self) != None):
                v.append(node.accept(self)[1])
        log(LOG_DEBUG , "Final derived list : " + str(v))
        return RET_SUCCESS , v

    def visitCurly(self, ctx: test_1Parser.CurlyContext):
        self.commonVisitor(ctx , "  CURLY : ")
        v = {}
        retCode = RET_FAILURE
        if ctx.curly() != None :
            for i in range(len(ctx.curly())):
                log(LOG_ERROR , "Getting curly " + str(i))
                retCode , val = ctx.curly(i).accept(self)
                v = v | val
        if ctx.pair() != None : 
            for i in range(len(ctx.pair())) : 
                log(LOG_ERROR , "Getting pair " + str(i) )
                retCode , temp_k , temp_v = ctx.pair(i).accept(self)
                v = v | {temp_k : temp_v}
        log(LOG_ERROR , "value for curly : " + str(v)  + " , where actual text : " + ctx.getText())
        return RET_SUCCESS, v

    def visitPair(self, ctx: test_1Parser.PairContext):
        self.commonVisitor(ctx, " PAIR : ")
        k = None
        v = None
        retCode = RET_FAILURE
        if ctx.uid(0) == None:
            log(LOG_ERROR , "UID not found in pair.")
        retCode , k = ctx.uid(0).accept(self)

        if (ctx.uid(1) != None):
            log(LOG_DEBUG , "uid value for pair")
            retCode , v = ctx.uid(1).accept(self)
        elif (ctx.list_() != None ) :
            log(LOG_DEBUG , "curly value for pair")
            retCode , v = ctx.list_().accept(self)
        elif (ctx.curly() != None ) :
            log(LOG_DEBUG , "list value for pair")
            retCode , v = ctx.curly().accept(self)
        log(LOG_ERROR , "pair key : " + str(k) + " , v : " + str(v) )
        return RET_SUCCESS, k , v

    def visitUid(self, ctx: test_1Parser.UidContext):
        self.commonVisitor(ctx , "UID")
        v = None
        retCode = RET_FAILURE
        if (ctx.num() != None):
            retCode , v = ctx.num().accept(self)
        elif (ctx.id_() != None) :
            retCode , v = ctx.id_().accept(self)
        elif (ctx.bt() != None):
            retCode , v = ctx.bt().accept(self)
        elif (ctx.bf() != None):
            retCode , v = ctx.bf().accept(self)
        elif (ctx.strings() != None):
            retCode , v = ctx.strings().accept(self)
        else:
            retCode = RET_FAILURE
        log(LOG_DEBUG , "UID value : " + str(v) )
        return retCode, v

    def visitAssign(self, ctx: test_1Parser.AssignContext , parent_type=DEFAULT):
        self.commonVisitor(ctx , "Assign")
        value = None
        count = ctx.getChildCount()
        varName = str(ctx.ID())
        if varName in gVarMap:
            print("Assignment variable already declared.")
        try:
            retCode , value = ctx.rvalue().accept(self)
            print("Derived rvalue : " + str(value) + " , for string : " + str(ctx.rvalue().getText()))
            retCode, gVarMap[varName] = ctx.rvalue().accept(self)
        except:
        	print("Failed..")
        # for i in range(0,count):
        #     if ctx.getChild(i).accept(self , parent_type=ASSIGNMENT):
        #         print("Accepted..")
        return super().visitAssign(ctx)

    def visitCode(self, ctx: test_1Parser.CodeContext , parent_type=DEFAULT):
        self.commonVisitor(ctx , "Code")
        return super().visitCode(ctx)

    def visitMember(self, ctx: test_1Parser.MemberContext , parent_type=DEFAULT , parent={}):
        '''
        parent type == member , in case we are visiting member of node.
        parent = dictionary of parent.
        '''
        v = None
        first = ctx.ID()
        self.commonVisitor(ctx , "member")
        log(LOG_DEBUG , "" , tid="100ar")
        if  first != None:
            if parent_type == PTYPE_MEMBER:
                if str(first) in parent:
                    v = parent[str(first)]
                else : 
                    log(LOG_ERROR , "Member '" + str(first) + "' not in parent.")
            elif parent_type == DEFAULT:
                if isVariable( str(first) ):
                    v = gVarMap[str(first)]
                else : 
                    log(LOG_ERROR , "Variable '" + str(first) + "' not declared.")
            else:
                log(LOG_ERROR , "Unknown parent type. Malformed membership.")
        parent = v
        if ctx.member_candidate() != None :
            log(LOG_DEBUG, "parent : "+ str(parent) , tid="100at" )
            success , v = self.evalMember(ctx.member_candidate(0) , memberList=ctx.member_candidate() , parent=parent , depth=0)
            log(LOG_DEBUG , " success : "+str(success)+", v : " + str(v)  + "parent : " + str(parent) , tid="100aq")
            # for i in range(len(ctx.member_candidate())):
            #     cand = ctx.member_candidate(i)
            #     log(LOG_DEBUG , "member candidate ::" +str(i) +" ::" + str(ctx.member_candidate(i).getText()) )
            #     v = self.visitMember_candidate(ctx.member_candidate(i) , parent_type=PTYPE_MEMBER , parent = parent)
        elif ctx.member() != None :
            v = self.visitMember(ctx.member() , parent_type=PTYPE_MEMBER , parent = parent)
        else : 
            log(LOG_ERROR , "No member OR member candidate!!")
        log(LOG_DEBUG , "Member v : "+str(v) , tid="100ap"  )
        return RET_SUCCESS, v


    def visitMember_candidate(self, ctx: test_1Parser.Member_candidateContext , parent_type=DEFAULT , parent={}):
        var = None
        success = False
        retCode = RET_FAILURE;
        self.commonVisitor(ctx , "member candidate")
        if ctx.uid() != None:
            log(LOG_ERROR , "In member candidate , var : " + str(var)  + " , parent : " + str(parent) + " type : " +str(type(parent)) +", uid : " + str(ctx.uid().getText()) )
            retCode, val= ctx.uid().accept(self)

            if type(val) == dict : 
                log(LOG_WARNING , "Dictionary specified as member.. " , tid="100am")
            k = val
            log(LOG_DEBUG , "k : " +k  + " , type : " + str(type(k))  , tid="809kn")
            if k in parent :
                var = parent[k]
                success = True
                log(LOG_DEBUG , "var : " + str(var) , tid="369ho")
            else : 
                log(LOG_ERROR , "ERR! var : " +  str(var) + " , parent : " +str(parent)   , tid="400ij")
                success = False
            if (parent_type == PTYPE_GET_TREE) :
                var = {k:var}
                log(LOG_DEBUG , "Parent get tree , var : " + str(var) , tid="100ay")

        elif ctx.match_b() != None :
            retCode , var = (ctx.match_b().accept(self))
            success = True
        elif (ctx.M() != None) :
            log(LOG_DEBUG , "m cand in all members") 
            var = parent
            success = True
            # for k,v in parent.items():
                # var.append()
        log(LOG_DEBUG , "Returning var : " + str(var) + " , success : " + str(success)  ,tid="587uj")
        if success :
            retCode = RET_SUCCESS
        return retCode, var


    def visitExpr(self, ctx: test_1Parser.ExprContext):
        self.commonVisitor(ctx , "expr")
        log(LOG_DEBUG , "In visitExpr." , tid="100ag")
        ans = ""
        retCode = RET_FAILURE
        if ctx.math_b_op() != None :
            # Implies, there is num/bracket + expr
            retCode , op = ctx.math_b_op().accept(self)
            retCode , v2 = ctx.expr().accept(self)
            if ctx.expr_1 != None:
                retCode, v1 = ctx.expr_1().accept(self)
            else:
                log(LOG_WARNING , "Unexpected condition. " , tid="100aa")
            retCode , ans = self.elementWiseOp(v1 , v2 , op)
        else:
            log(LOG_WARNING , "expression without operator. i.e. simple uid.")
            if ctx.expr_1 != None :
                retCode, ans = ctx.expr_1().accept(self)
        
        return retCode , ans

    def elementWiseOp(self, a , b , op) :
        c = {}
        retCode = RET_FAILURE
        log(LOG_DEBUG , "op : "  +str(op) + " a : " + str(a) +" ,  b : " + str(b) + " , c : "+ str(c)\
            + " , type a : "  +str(type(a)) + " , type b : " + str(type(b)) ,tid="100aj"  )
        if (type(a) != dict) or (type(b) != dict) :
            log(LOG_DEBUG , "non dict received in elementWiseOp. " , tid="100ab")
            return RET_FAILURE , ""
        for k in a.keys():
            log(LOG_DEBUG , "Checking key : " + str(k) , tid="100ai")
            if (k in b):
                ta = type(a[k])
                tb = type(b[k])
                if ( (ta!=dict) and (tb!=dict) ) :
                    log(LOG_DEBUG , "In leaf nodes" , tid="100ak")
                    # If both are leaf nodes, perform op.
                    if ( ta == tb) :
                        if op == "+":
                            c[k] = a[k] + b[k]
                        elif op == "-":
                            if(ta == str) or (tb == str): 
                                c[k] = a[k]
                            else:
                                c[k] = a[k] - b[k]
                        elif op == "*":
                            if(ta == str) or (tb == str): 
                                c[k] = a[k]
                            else:
                                c[k] = a[k] * b[k]
                        elif op == "/":
                            if(ta == str) or (tb == str): 
                                c[k] = a[k]
                            else:
                                c[k] = a[k] / b[k]
                    else:
                        log(LOG_WARNING , "Typemismatch for leaf nodes. " , tid="100ac")
                elif( (ta!=dict) or (tb!=dict) ):
                    log(LOG_WARNING , "Nodes are leaf and non-leaf, Assigning one random node without operation." , tid="100ad")
                    c[k] = b[k]
                else:
                    retCode , c[k] = self.elementWiseOp(a[k] , b[k] , op)
        log(LOG_DEBUG , "op : "  +str(op) + " a : " + str(a) +" ,  b : " + str(b) + " , c : "+ str(c),tid="100ae"  )
        return retCode, c;


    def visitId_(self, ctx: test_1Parser.Id_Context , parent_type=DEFAULT):
        # self.commonVisitor(ctx, "id")
        text = str(ctx.ID())
        retCode , var = getVar(text)
        if retCode == RET_FAILURE : 
            log(LOG_WARNING , "variable not in map : " + text)
        return retCode , var
        
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
        return RET_SUCCESS , (num)

    def visitStrings(self, ctx: test_1Parser.StringsContext):
        self.commonVisitor(ctx , "String")
        log(LOG_DEBUG , "strings return is : " + str(ctx.STR())[1:-1])
        # Remove quotes from both the ends..
        return RET_SUCCESS,  str(ctx.STR())[1:-1]

    def visitBt(self, ctx: test_1Parser.BtContext , parent_type=DEFAULT):
        return RET_SUCCESS, True;

    def visitBf(self, ctx: test_1Parser.BfContext , parent_type=DEFAULT):
        return RET_SUCCESS, False


    def evalMember(self , ctx  , memberList , parent = {} , ptype = PTYPE_DEFAULT , depth = 0):
        v = {}
        success = True
        success1 = False
        retCode = RET_FAILURE
        ret1 = RET_SUCCESS
        log(LOG_DEBUG , " In evalMember , PARENT : " + str(parent) + " , memberList : " +str(memberList[0].getText()) )
        if len(memberList) > 1:
            log(LOG_DEBUG , "Going down a member..") 
            if memberList[0].M() :
                log(LOG_DEBUG , "Encountered a * .")
                for key_each in parent.keys() :
                    success = True
                    retCode , val =  self.evalMember(ctx , memberList[1:] , parent[key_each] , depth = (depth +1)) 
                    log(LOG_DEBUG , "success : " + str(success) + " , val : " +str(val) , tid="254dc"  )
                    if (retCode == RET_SUCCESS) :
                        if ptype == PTYPE_DEFAULT:
                            v = val
                        elif ptype == PTYPE_GET_TREE :
                            v[key_each] = val
                        else:
                            log(LOG_WARNING , "Uidentified ptype" , tid="100aw")
                    log(LOG_DEBUG , "v : " + str(v) , tid="465kn")
            elif memberList[0].uid() :
                retCode , var = memberList[0].uid().accept(self)
                log(LOG_DEBUG , "var : "+ str(var) , tid="100an")
                retCode , val = self.evalMember(ctx , memberList[1:] , parent[var] , depth=(depth + 1) )
                log(LOG_DEBUG , "retcode : "+str(retCode) + " , val:" + str(val) , tid="100au")
                if retCode == RET_SUCCESS :
                    if ptype == PTYPE_DEFAULT : 
                        v = val
                    elif ptype == PTYPE_GET_TREE :
                        v[var] = val
                    else : 
                        log(LOG_DEBUG , "Unidentified ptype" , tid="100ax")
                else:
                    log(LOG_DEBUG , "" , tid="100av")
                    retCode = RET_FAILURE 
                    v = {}
                log(LOG_DEBUG , "v : " + str(v) , tid="100ao")
            elif ( memberList[0].match_b() ) : 
                log(LOG_WARNING , "match_b not implemented in evalmembers..")
            else : 
                log(LOG_WARNING , "Unconsidered member encountered. " , tid="100al")
        else : 
            log(LOG_DEBUG , "Reached terminal member of member candidates ." + " , memberList : " +str(memberList[0].getText()))
            retCode , v = self.visitMember_candidate( memberList[0] , parent_type=PTYPE_MEMBER , parent = parent )
        log(LOG_DEBUG , "evalMember , PARENT : " + str(parent)+ " , v : " + str(v) + " , retCode : " + str(retCode) , tid="976hv")
        log(LOG_DEBUG , "" , tid="100as")

        return retCode, v


    def commonVisitor(self, ctx  , ruleName):
        abc = ctx.getText()
        count = ctx.getChildCount()
        log( LOG_DEBUG , "visitor  :" + ruleName +" : " + abc + " ,  child count : " + str(count)  , tid = "099aa" )        
        try:
            if (count > 0) : 
                for i in range(0,count) : 
                    c = ctx.getChild(i)
                    c.accept(self)
                    # print("done with " + str(c.getText()) )

            else : 
                log(LOG_DEBUG , "This is termilnal node.." , tid="099ab")
        except:
            log(LOG_ERROR , "Exception in common visitor..")


def isFunction(param):
    if param in gFunMap:
        return True
    else :
        return False

def getVar(param):
    if isVariable(param):
        return RET_SUCCESS , gVarMap[param]
    else:
        return RET_FAILURE , None


def isVariable(param):
    if param in gVarMap:
        return True
    else :
        return False




if __name__ == "__main__"  :
    run_1(sys.argv)
else :
    run_1(["test_1_visitor.py","sample.txt"] )




