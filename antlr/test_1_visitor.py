from http.client import RESET_CONTENT
from inspect import currentframe, getframeinfo
from itertools import islice
import antlr4
import sys
import re
from antlr4.tree.Trees import Trees
import logging
import copy
import numbers

sys.path.append("/home/container/mounted/jop_repo/")
import dict_op


# Creating a logger object
logFormat="[%(asctime)s:%(levelname)s: %(filename)s:%(lineno)s-%(funcName)s() ] %(message)s"
logging.basicConfig(filename="visitor.log" ,  level=logging.DEBUG , force=True , format=logFormat)
logger = logging.getLogger(__name__.split('.')[0])
logger.debug("This is first debug message")
logger.error("This is first error message")
LOG_ERROR               = 1
LOG_WARNING             = 2
LOG_INFO                = 3
LOG_DEBUG               = 4
LOG_VERBOSE             = 5
LOG_FILTER_LEVEL        = 5
RET_FAILURE             = -1
RET_SUCCESS             = 0
RET_TREE                = 1
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
PTYPE_SET_VAL       = "set_value"


'''
Return value sample dictionary : 
ret = {
    "value" : "This is actual value or may be another dictionary or array as value. "
    "str"   : "String of this node"
    ""
}
'''

def getFLoc():
    frameinfo = getframeinfo(currentframe().f_back.f_back)
    filename = frameinfo.filename.split('/')[-1]
    linenumber = frameinfo.lineno
    loc_str = ' # %s:%d : ' % (filename, linenumber)
    return loc_str

def logFallBack(level=0, str1="" , tid="000OO"):
    print(  getFLoc()+ ":<< check "+str(tid) + " >> " + str1 )

log = logFallBack

def run_1 (log=logFallBack , ip_string=None , ip_file=None) :
    print("Hello world!!")
    if (ip_file != None) : 
        inp = antlr4.FileStream(ip_file)
    elif (ip_string != None) :
        inp = antlr4.InputStream(ip_string)
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
    p = visitor.visit(tree)
    logger.debug(SEPERATOR + "gVarMap :  \n" )
    for k,v in gVarMap.items():
        logger.debug(" k : [{}] , v : [{}]".format(k,v))
    logger.debug("visitor return : p:{} ".format(p))
    logger.debug("{}Return value : {}".format(SEPERATOR , visitor.gRet))
    return visitor.gRet


class cArgs():
    setValue                        =   False
    rootDefined                     =   False
    lValue                          =   False
    level                           =   0
    sharedJi                        =   None
    value                           =   None
    refs                            =   None
    def __init__(self):
        inArray     = None
        inDict      = None
            
    def __str__(self):
        return ( "cArg : [ {{ setValue : {} , rootDefined : {} , lValue : {} , level : {} , sharedJi : {} , refs : {} }} ] ".format(
                    self.setValue , self.rootDefined  , self.lValue , self.level , self.sharedJi , self.refs ) )

class cRet():
    RETCODE_SUCCESS                 = "RETURN_SUCCESS"
    RETCODE_GENERIC_FAILURE         = "RETURN_GENERIC_FAILURE"
    RETCODE_INVALID_PARAMS          = "RETURN_INVALID_PARAMETERS"
    RETCODE_INVALID_RET             = "RETURN_INVALID_RETURN_CODE"
    RETCODE_INVALID_CONSTRUCT       = "RETURN_INVALID_LANGUAGE_CONSTRUCT"
    key                             = None
    value                           = None
    retCode                         = None
    text                            = None
    rootDefined                     = False
    sharedJi                        = dict_op.ji()
    varValue                        = None
    refs                            = None
    def __init__(self):
        retCode     = self.RETCODE_GENERIC_FAILURE
    
    def __str__(self):
        return ("cRet : {{ retCode : {} key : {} , value : {} , text : {} }}".format(self.retCode , self.key , self.value , self.text) )


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

class response():
    def __init__(self):
        self.ret = RET_FAILURE
    



class customVisitor(test_1Visitor):
    gRet = { 
            "success"   : False , 
            "value"     : None ,
            "version"   : "1.0"
        }
    argStack = []
    def visitMatch_b(self, ctx: test_1Parser.Match_bContext  ):
        self.commonVisitor(ctx , "match_b")
        args = self.getArgs()
        ret = cRet()
        value = None
        if (ctx.match_b(0) != None):
            nArg = self.newArgs()
            ret = ctx.match_b(0).accept(self)
        elif (ctx.rvalue(0) != None):
            nArg = self.newArgs()
            ret = ctx.rvalue(0).accept(self)
        logger.debug( "ret : {} ,".format(ret)   )
        return ret

    def visitDict_b_op(self, ctx: test_1Parser.Dict_b_opContext  ):
        log(LOG_DEBUG , "DICT OPS not implemented.." , tid="100bw")
        args = self.getArgs()
        ret = cRet()
        ret.value = ""
        ret.retCode = ret.RETCODE_GENERIC_FAILURE
        if ctx.P() != None:
            ret.value = "+"
            ret.retCode = ret.RETCODE_SUCCESS
        elif ctx.N() != None:
            ret.value = "-"
            ret.retCode = ret.RETCODE_SUCCESS
        return ret

    def  visitB_op(self, ctx: test_1Parser.B_opContext  ):
        args = self.getArgs()
        ret = cRet()
        ret.retCode = ret.RETCODE_GENERIC_FAILURE
        ret.value = None
        if (ctx.math_b_op() != None) :
            nArg = self.newArgs()
            ret  = ctx.math_b_op().accept(self)
        elif (ctx.dict_b_op() != None) :
            nArg = self.newArgs()
            ret = ctx.dict_b_op().accept(self)
        logger.debug("ret : {}   ".format(ret )  )
        return ret #super().visitB_op(ctx)

    def visitMath_b_op(self, ctx: test_1Parser.Math_b_opContext  ):
        args    = self.getArgs()
        ret     = cRet()
        ret.retCode = ret.RETCODE_GENERIC_FAILURE
        if ctx.P() != None:
            ret.value = ".+"
            ret.retCode = ret.RETCODE_SUCCESS
        elif ctx.N() != None:
            ret.value = ".-"
            ret.retCode = ret.RETCODE_SUCCESS
        elif ctx.M() != None:
            ret.value = ".*"
            ret.retCode = ret.RETCODE_SUCCESS
        elif ctx.D() != None:
            ret.value = "./"
            ret.retCode = ret.RETCODE_SUCCESS
        if ret.value =="" :
            logger.warning( "Unexpected binary operator. ")
        return ret
    
    def visitLines(self, ctx: test_1Parser.LinesContext  ):
        args = self.getArgs()
        self.commonVisitor(ctx , "Lines")
        print("visitor count : " + str(ctx.getChildCount()) )
        # self.visit()
        return super().visitLines(ctx)

    def visitList_(self, ctx: test_1Parser.List_Context   ):
        self.commonVisitor(ctx , "LIST_")
        ret = cRet()
        ret.value = []
        ret.retCode = ret.RETCODE_GENERIC_FAILURE
        count = ctx.getChildCount()
        # log(LOG_DEBUG , "list tokens : " + str(ctx.getTokens()))
        for i in range(count-1):
            if i==0:
                # Skip Opening and closing brackets.
                continue;
            node = ctx.getChild(i)
            logger.debug( "list node : {}" .format( node.getText()) )
            nArgs = self.newArgs()
            child = node.accept(self) 
            if ( child != None):
                ret.value.append(child.value)
        logger.debug("Final derived list : {} ".format(ret) )
        return ret

    def visitCurly(self, ctx: test_1Parser.CurlyContext  ):
        self.commonVisitor(ctx , "  CURLY : ")
        args = cArgs()
        self.argStack.append(args)
        ret = cRet()
        ret.value = {}
        ret.retCode = ret.RETCODE_GENERIC_FAILURE
        if ctx.curly() != None :
            for i in range(len(ctx.curly())):
                logger.error( "Getting curly {}".format(i))
                nArgs = self.newArgs()
                ret2 = ctx.curly(i).accept(self)
                ret.value = ret.value | ret2.val
        if ctx.pair() != None : 
            for i in range(len(ctx.pair())) : 
                logger.error("Getting pair {}".format(i) )
                nArgs = self.newArgs()
                ret2 = ctx.pair(i).accept(self)
                ret.value = ret.value | {ret2.key : ret2.value}
        logger.error( "value for curly : {} , where actual text : {} " .format( ret.value , ctx.getText()) )
        return ret

    def visitPair(self, ctx: test_1Parser.PairContext  ):
        self.commonVisitor(ctx, " PAIR : ")
        args = self.getArgs()
        ret = cRet()
        ret.key = None
        ret.value = None
        ret.retCode = ret.RETCODE_GENERIC_FAILURE
        if ctx.uid(0) == None:
            logger.error("UID not found in pair.")
        nArgs = self.newArgs()
        retK = ctx.uid(0).accept(self)

        if (ctx.uid(1) != None):
            logger.debug( "uid value for pair")
            nArgs = self.newArgs()
            retV = ctx.uid(1).accept(self)
        elif (ctx.list_() != None ) :
            log(LOG_DEBUG , "curly value for pair")
            nArgs = self.newArgs()
            retV = ctx.list_().accept(self)
        elif (ctx.curly() != None ) :
            log(LOG_DEBUG , "list value for pair")
            nArgs = self.newArgs()
            retV = ctx.curly().accept(self)
        logger.error( "pair key : {} , v : {} ".format(retK.value , retV.value) )
        ret.key = retK.value
        ret.value = retV.value
        ret.retCode = ret.RETCODE_SUCCESS
        return ret

    def visitUid(self, ctx: test_1Parser.UidContext   ):
        self.commonVisitor(ctx , "UID")
        args        = self.getArgs()
        ret         = cRet()
        ret.value   = None
        ret.retCode = ret.RETCODE_GENERIC_FAILURE
        if (ctx.num() != None):
            nArgs = self.newArgs()
            ret = ctx.num().accept(self)
        elif (ctx.id_() != None) :
            nArgs = self.newArgs()
            ret = ctx.id_().accept(self)
        elif (ctx.bt() != None):
            nArgs = self.newArgs()
            ret = ctx.bt().accept(self)
        elif (ctx.bf() != None):
            nArgs = self.newArgs()
            ret = ctx.bf().accept(self)
        elif (ctx.strings() != None):
            nArgs = self.newArgs()
            ret = ctx.strings().accept(self)
        else:
            ret.retCode = ret.RETCODE_GENERIC_FAILURE
        logger.debug( "UID value : {}".format(ret) )
        return ret

    def getReturn(arg):
        ret = cRet()
        ret.retCode = ret.RETCODE_INVALID_RET
        fName = sys._getframe(1).f_code.co_name
        if arg==None:
            logger.warning("[{}] : Got None return. ".format(fName) )
        elif (isinstance(arg , cRet) ):
            ret = arg
        else:
            logger.warning("[{}] : Incorrect return type : {}".format( fName , type(arg)))
        return ret
    
    def visitAssign(self, ctx: test_1Parser.AssignContext  ):
        self.commonVisitor(ctx , "Assign")
        value = None
        newVar = True
        count = ctx.getChildCount()
        logger.debug("In assign for : {}".format(ctx.getText()) )
        nArgs = self.newArgs()
        ret = cRet()  
        side = "lvalue"
        keyChain = []
        if ctx.rvalue() != None : 
            nArgs.lValue = False
            ret2 = ctx.rvalue().accept(self)
            value = copy.deepcopy(ret2.value)
        if ctx.id_() != None : 
            nArgs = self.newArgs()
            nArgs.lValue = True
            nArgs.value = value
            ret2 = ctx.id_().accept(self)
            try:
                varName = ret2.text
                nArgs = self.newArgs()
                ret = ctx.rvalue().accept(self)
                #log(LOG_DEBUG , "rvalue : {}".format(ctx.rvalue()) , tid="100bo")
                logger.debug( "Derived rvalue : {}  , for string : {}".format(value, ctx.rvalue().getText())  )
                # Direct variable assignment.
                logger.debug("varName : {} , value : {}".format(varName , value)   )
                gVarMap[varName] = (value)
            except Exception as e:
                ret = cRet()
                ret.retCode =ret.RETCODE_GENERIC_FAILURE
                logger.error("Failed.. Exception : {} ".format(e) )
        elif ctx.member() != None :
            nArgs = self.newArgs()
            nArgs.lValue = True
            nArgs.value = value
            ret2 = ctx.member().accept(self)
            if ( (isinstance(ret2 , cRet)) and (isinstance(ret2.value , list))  ):
                logger.debug("test")
                refList = ret2.value
                if (len(refList) > 0):
                    for ref in refList : 
                        logger.debug("Updating ref : {}".format(ref) )
                        ref.updateValue(value)
        logger.debug("VarName  : {}". format(ret.value)  )
        if (ret.retCode == RET_SUCCESS) and (ret.value in gVarMap):
            logger.debug("Assignment variable already declared. VarName : {} ,  gVarMap : ".format(ret.value , gVarMap)  )
            newVar = False

        return ret

    def visitRoot(self, ctx:test_1Parser.RootContext):
        args            = self.getArgs()
        ret             = cRet()
        ret.rootDefined = True
        ret.retCode     = ret.RETCODE_SUCCESS
        return ret

    def visitCode(self, ctx: test_1Parser.CodeContext):
        self.commonVisitor(ctx , "Code")
        a =  super().visitCode(ctx)
        if "ret" in gVarMap :
            self.gRet["value"] = gVarMap["ret"]         # Assign return value
        return a
    def visitMember(self, ctx: test_1Parser.MemberContext ):
        '''
        parent type == member , in case we are visiting member of node.
        parent = dictionary of parent.
        '''
        args = self.getArgs()
        logger.debug("Visting children for {}".format(ctx.getText()) )
        nArgs = self.newArgs()
        ret = cRet()
        root = dict_op.ji( {"root" : []} )  
        level = 0
        localRef = dict_op.refManager()
        localRef.setRef(root , key="root")
        logger.debug("args : {}".format(args) )
        if (ctx.root() != None) and ( (2 > len(ctx.root())) )  : 
            logger.debug("root : {} ".format(ctx.root()))
        else : 
            logger.debug("Incorrect ROOT defined. ROOT count = [{}]".format(len(ctx.root())))
            return RET_FAILURE , v
        
        if (ctx.id_() != None ):
            rootRet = ctx.id_().accept(self)
        else:
            log(LOG_DEBUG , "Unexpected error, None ID in member." , tid="100bq")
        self.commonVisitor(ctx , "member")
        logger.debug("Member candidatess : {} ".format(ctx.getText()) )

        count = ctx.getChildCount()
        logger.debug("Member has [{}] children.".format(count) )
        for i in range (count):
            child   = ctx.getChild(i)
            logger.debug(" i : [{}] , child : [{}] ".format(i , child.getText()) )
            nArgs   = self.newArgs()
            nArgs.rootDefined = ret.rootDefined
            nArgs.refs = localRef
            logger.debug("new Refs : {}".format(nArgs.refs) )
            if 0 == i:
                nArgs.lValue = args.lValue
                nArgs.sharedJi  = root
                localRef.setRef(root , key="root")
                logger.debug("Checking for : [{}]. ".format(child.getText()) )
                ret2    = child.accept(self)
                if ( ( args.lValue) or isinstance(ret2.value , dict)):
                    if args.lValue : 
                        if (not isVariable(ret2.text)):
                            gVarMap[ret2.text] = {}
                            r = dict_op.refManager()
                            r.setRef(gVarMap , ret2.text)
                            localRef.updateValue( [r])
                            logger.debug("varName : {} , Ref : {}".format(ret2.text ,  r) )
                        else :
                            localRef.updateValue( [ret2.refs])
                    else : 
                        ok , v = ret2.refs.getValue()
                        if ok : 
                            mockDict = { "dummy" : copy.deepcopy(v) }
                            r = dict_op.refManager()
                            r.setRef(mockDict , "dummy")
                            localRef.updateValue( [r])
                            logger.debug("Added deepcopy for RHS.")

                else : 
                    logger.warning("Tried to access membership for non dictionary variable. {} ".format(ret2.value) )
                    ret.retCode = ret.RETCODE_INVALID_PARAMS
                    return ret
                logger.debug("new Refs : {}".format(nArgs.refs) )
            else : 
                nArgs.lValue        = args.lValue
                if (not (isinstance(root , dict_op.ji) )):
                    logger.warning("Incorrect dictionary evaluated at : [{}]".format(child.getText()) )
                nArgs.sharedJi      = root
                nArgs.level         = level
                logger.debug("Checking for : [{}]. python type : [{}] ".format(child.getText() , type(child) ) )
                ret2    = child.accept(self)

                if (  isinstance(child , test_1Parser.Member_candidateContext) ) : 
                    logger.debug("Identified member candidate type.")
                    level = level+1
                elif (isinstance(child , test_1Parser.RootContext) ) :
                    logger.debug("Identified Root location.")            
                    nArgs.sharedJi  = root
                    ret.rootDefined = True
                    level = 0

            logger.debug("root : {}".format(root))
            if ret2 == None : 
                logger.warning("RET2 is NONE. ")
            else :
                ok , v = localRef.getValue()
                if not ok : 
                    logger.warning("Localref getvalue failed")
                s = ""
                for i in v:
                    s += "\n{}".format(i)
                logger.debug("Refs : [{}] , {}".format(localRef , s) )

        ok , v = localRef.getValue()
        if not ok : 
            logger.warning("Localref getvalue failed")
        if len(v) == 0 : 
            logger.warning("No match found !!!")
        elif ( (not args.lValue) and (len(v) == 1) ): 
            ok , v2 = v[0].getValue()
            if ok :
                ret.value = copy.deepcopy( v2 )
            else : 
                logger.warning("Unable to get value.")
        elif (args.lValue):
            ret.value = v
        ret.retCode = ret.RETCODE_SUCCESS        
        logger.debug("ret : [{}]".format(ret) )
        return ret


    def visitMember_candidate(self, ctx: test_1Parser.Member_candidateContext ):
        success = False
        ret = cRet()
        ret.retCode = ret.RETCODE_GENERIC_FAILURE
        self.commonVisitor(ctx , "member candidate")
        args = self.getArgs()
        m = dict_op.matchCriteria()
        k = None
        ret2 = None
        if (args == None):
            logger.debug("Custom args not found. ")
        else :
            logger.debug("custom args : [{}]".format(args) )

        ok , refList = args.refs.getValue()
        if not ok : 
            logger.warning("Ref access failed. ")
            ret.retCode = ret.RETCODE_INVALID_PARAMS
        logger.debug("REF LIST : {}".format(refList) )
        if ( not ( isinstance(refList, list) ) ): 
            logger.warning("reflist is of type : [{}]".format(type(refList)) )

        if ctx.uid() != None:
            nArgs = self.newArgs()
            ret2  = ctx.uid().accept(self)
            logger.debug("level [{}],  RET : [{}]".format(args.level , ret2) )
            if type(ret2.value) == dict : 
                logger.warning("Dictionary specified as member.. ")
            k = ret2.value
            m.key = k 
        elif ctx.match_b() != None :
            nArgs = self.newArgs()
            ret = (ctx.match_b().accept(self))
            success = True
        elif (ctx.M() != None) :
            if (not args.rootDefined) : 
                logger.warning("Select all without root.")
            else : 
                m.matchType = m.MATCH_ALL
            log(LOG_DEBUG , "m cand in all members") 
            success = True
        
        if ( not args.lValue): 
            if ( not args.rootDefined): 
                ok , d = refList[0].getValue()
                logger.debug("Ref 0 : {}".format(d) )
                if ok and ((isinstance(d , dict)) and (k in d.keys())):
                    refList[0] = dict_op.refManager()
                    refList[0].setRef(d , k)
                    logger.debug("test")
            else : 
                if (m.matchType != m.MATCH_ALL) :
                    # If matchAll , no need to do anything, 
                    ok , d = refList[0].getValue()
                    if ok : 
                        if (isinstance(d , dict)):
                            j = dict_op.ji(d)
                            refList[0].updateValue(j)
                            logger.debug("Converted to Ji instance")
                        elif (isinstance(d , dict_op.ji)):
                            j = d
                            logger.debug("Already Ji instance")
                    m.level = args.level
                    m.key = ret2.value
                    m.matchType = m.MATCH_DEL_NON_MATCHING_LEVELS
                    j.filter(m)
                    logger.debug("test")
        else :
            logger.debug("refList : {}".format(refList) )
            if ((len(refList) == 0)): 
                logger.debug(" refList {}".format(refList ) )
                d = {k : None}
                r = dict_op.refManager()
                r.setRef(d , k)
                refList.append(r)                
                logger.debug("New reflist : {} , new ref : {} ".format(refList , r) )
            for refIndex in range(len(refList)) :  
                logger.debug("test")
                m = dict_op.matchCriteria()
                m.key = k
                newRef = dict_op.getRefs(refList[refIndex] , m)
                if (len(newRef)==0):
                    ok , d_orig = refList[refIndex].getValue()
                    if ok : 
                        if ( isinstance(d_orig , dict) ):
                            d_orig[k] = None
                        else : 
                            refList[refIndex].updateValue({k:None})
                    logger.debug("new ref : {} , value : {}".format(refList[refIndex] , refList[refIndex].getValue()[1]) )
                    r = dict_op.refManager()
                    r.setRef(refList[refIndex].getValue()[1] , k)
                    refList.append(r)
                refList.pop(refIndex)
                if (len(newRef) > 0 ):
                    logger.debug("test")
                    for eachRef in newRef : 
                        refList.append(eachRef)
        if success :
            ret.retCode = ret.RETCODE_SUCCESS
        return ret


    def visitExpr(self, ctx: test_1Parser.ExprContext  ):
        self.commonVisitor(ctx , "expr")
        args = self.getArgs()
        ret = cRet()
        logger.debug( "In visitExpr." )
        ans = ""
        ret.retCode = ret.RETCODE_GENERIC_FAILURE
        if ctx.b_op() != None :
            # Implies, there is num/bracket + expr
            nArgs = self.newArgs()
            retOp = ctx.b_op().accept(self)
            nArgs = self.newArgs()
            retV2 = ctx.expr().accept(self)
            if ctx.expr_1 != None:
                nArgs = self.newArgs()
                retV1 = ctx.expr_1().accept(self)
                logger.debug("retV1 : {} ".format(retV1) )
            else:
                logger.warning("Unexpected condition. ")
            logger.debug( "v1 : {} , v2 : {} , op : {}".format(retV1 , retV2 , retOp)  )
            if ( (retV1.value == None) or (retV2.value == None) ):
                ret.retCode = ret.RETCODE_GENERIC_FAILURE;
                return ret
            elif ( (isinstance(retV1.value , str ) and isinstance(retV2.value , str)) ):
                logger.debug("Concatenating strings.")
                if retOp.value == "+" :
                    ret.value = retV1.value + retV2.value
                return ret
            # if ( (isinstance(v1 , dict_op.ji) or isinstance(v1 , dict) ) and 
            #     (isinstance(v2 , dict_op.ji) or isinstance(v2 , dict) ) ):

            if ( (ctx.b_op() != None ) and (ctx.b_op().math_b_op()!= None) and 
                (isinstance(retV1.value , dict) and isinstance(retV2.value , dict)) ):
                if retOp.value == ".+" :
                    a = dict_op.ji(retV1.value) 
                    b = dict_op.ji(retV2.value) 
                    ret.value = a + b
                elif retOp.value == ".-" :
                    a = dict_op.ji(retV1.value) 
                    b = dict_op.ji(retV2.value) 
                    ret.value = a - b
                elif retOp.value == ".*" :
                    a = dict_op.ji(retV1.value) 
                    b = dict_op.ji(retV2.value) 
                    ret.value = a * b
                elif retOp.value == "./" :
                    a = dict_op.ji(retV1.value) 
                    b = dict_op.ji(retV2.value) 
                    ret.value = a - b
                elif retOp.value == "+" :
                    a = dict_op.ji(retV1.value) 
                    b = dict_op.ji(retV2.value) 
                    ret.value = a.union(b)
                elif retOp.value == "-" :
                    logger.warning("Dict diff not yet implemented. ")
                    # a = dict_op.ji(retV1.value) 
                    # b = dict_op.ji(retV2.value) 
                    # ret.value = a - b
                logger.debug(" calculated return : [ {} ]".format(ret))
            elif ( (isinstance(retV1.value , numbers.Number)) and (isinstance(retV2.value , numbers.Number)) ):
                if (retOp.value == "+"  or retOp.value == ".+"):
                    ret.value = retV1.value + retV2.value
                elif (retOp.value == "-"  or retOp.value == ".-"):
                    ret.value = retV1.value - retV2.value
                elif (retOp.value == "*"  or retOp.value == ".*"):
                    ret.value = retV1.value * retV2.value
                elif (retOp.value == "/"  or retOp.value == "./"):
                    ret.value = retV1.value / retV2.value
            elif (isStr(retV1.value) and isStr(retV2.value)) :
                if (retOp.value == "+" or retOp.value == ".+"):
                    ret.value = retV1.value + retV2.value
            else:
                pass
        else:
            log(LOG_WARNING , "expression without operator. i.e. simple uid.")
            if ctx.expr_1() != None :
                nArgs = self.newArgs()
                ret = ctx.expr_1().accept(self)
            else: 
                logger.warning("expr_1 not defined : " )
        logger.debug( "Exit visitexpr. retCode : {} , ans : {} , ctx : {}".format(ret , ans , ctx.getText() ) )
        return ret

    def evalDictOp(self , a , b , op ):
        ret = cRet()
        ret.value = None
        if (isinstance(a , dict)):
            ja = dict_op.ji(a)
        else : 
            logger.warning("a is not dict")
            return ret
        if (isinstance(b , dict)):
            jb = dict_op.ji(b)
        else : 
            logger.warning("b is not dict")
            return ret
        
        if (op == "+"):
            ret.value = a|b
            ret.retCode = ret.RETCODE_SUCCESS
        elif (op == "-"):
            ret.value = ja - jb
            ret.retCode = ret.RETCODE_SUCCESS
        return ret

    def elementWiseOp(self, a , b , op) :
        c = {}
        ret = cRet()
        ret.retCode = RET_FAILURE
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
                    ret2 = self.elementWiseOp(a[k] , b[k] , op)
                    ret.value[k] = ret2.value
            else:
                log(LOG_DEBUG , "Skipping key : {} ".format(k) ,tid="100bv" )
        logger.debug("op : {}  a : {} ,  b : {} , c : {} ".format(op , a , b , c)   )
        ret.value = c
        return ret;

    def newArgs(self):
        args = cArgs()
        self.argStack.append(args)
        return args

    def getArgs(self):
        fName = sys._getframe(1).f_code.co_name
        if len(self.argStack) > 0:
            args = self.argStack.pop()
        else : 
            logger.warning("Stack underflow for [{}]".format(fName) )
            return cArgs()
        if self.verifyCustomArgs(args , fName) : 
            return args
        else :
            logger.warning("Incorrect args found for [{}]".format(args) )
            return cArgs()

    def verifyCustomArgs(self, args , string):
        if (not isinstance(args , cArgs)) :
            logger.debug("[{}] : Custom args not found.".format(string) )
            return False
        else : 
            logger.debug("[{}] : Custom arg was found.".format(string) )
            return True

    def visitId_(self, ctx: test_1Parser.Id_Context  ):
        self.commonVisitor(ctx, "id")
        args= self.getArgs()
        ret = cRet()
        text = str(ctx.ID())
        if not self.verifyCustomArgs(args , "visitId_") : 
            return ret 
        ret = getVar(text)
        ret.text = text
        if ret.retCode == RET_FAILURE : 
            logger.warning("variable not in map : {}".format(ret.text)   )
        if args.setValue : 
            ret.retCode = ret.RETCODE_INVALID_RET
            ret.value = ret.text
        return ret
        
    def visitRvalue(self, ctx: test_1Parser.RvalueContext  ):
        print("Non need to explicitly implement the rvalue, as rvalue would just call one of the OR'd methods.")
        return super().visitRvalue(ctx)

    def visitNum(self, ctx: test_1Parser.NumContext  ):
        # self.commonVisitor(self, "num")
        args = self.getArgs()
        ret = cRet()
        num = 0
        if ctx.INT() != None : 
            num = int(str(ctx.INT()))
        else : 
            num = float(str(ctx.FLT()))
        logger.debug( "NUM : {}".format(num))
        ret.value = num
        ret.retCode = ret.RETCODE_SUCCESS
        return ret

    def visitStrings(self, ctx: test_1Parser.StringsContext  ):
        args = self.getArgs()
        ret = cRet()
        ret.retCode = ret.RETCODE_SUCCESS
        ret.value = str(ctx.STR())[1:-1]
        self.commonVisitor(ctx , "String")
        logger.debug( "strings return is : {} ".format(ret.value))
        # Remove quotes from both the ends..
        return ret

    def visitBt(self, ctx: test_1Parser.BtContext  ):
        ret = cRet()
        ret.retCode = ret.RETCODE_SUCCESS
        ret.value = True
        return ret

    def visitBf(self, ctx: test_1Parser.BfContext  ):
        ret = cRet()
        ret.retCode = ret.RETCODE_SUCCESS
        ret.value = False
        return ret

    def isDict(var):
        return (type(var) == dict)

    def isList(var):
        return (type(var) == list)

    def getValue(self , target , var , path=[]):
        ret = cRet()
        ret.value = None
        if self.isDict(var) : 
            if self.pathMatch(target=target , path=path , isRegex=False):
                # Path matches, return current value. 
                value = var
            for k in var.keys():
                self.getValue(target , path.append(k) , var )

        return ret

    def setValue(self , target, path , value):
        ret = cRet()
        return ret

    def internalCalls(self , ctx  ):
        ret = cRet()
        ret.retCode = ret.RETCODE_GENERIC_FAILURE
        v = None
        f = ""
        log(LOG_DEBUG , getFLoc() + "Pathmaymatch. " )
        if f == "re":
            v = ""
        elif f == "replace":
            v = ""
        else : 
            retCode = RET_FAILURE
        return ret

    def replace(self, a , b , input , isRegex) :
        ret = cRet()
        ret.retCode = RET_FAILURE
        v = ""
        try : 
            if (not isRegex):
                if a == input :
                    v = b
                    retCode = RET_SUCCESS
                else : 
                    v = a
                    retCode = RET_SUCCESS
            else:
                match = re.search(a , input)
                if match!= None :
                    v = b
                else:
                    v = input
                retCode = RET_SUCCESS
        except Exception as e : 
            retCode = RET_FAILURE
        return ret
    def evalUnion(self, ctx , a , b , parent_type=PTYPE_DEFAULT) : 
        ret= cRet()
        return ret

    def evalDiff(self, ctx , a , b , parent_type = PTYPE_DEFAULT):
        ret= cRet()
        return ret

    def isMultipleAllowed(valType = "rvalue" , rootDefined = False):
        multipleAllowed = False
        if ( valType == "rvalue" and (not rootDefined)):
            multipleAllowed = False
        elif ( (valType == "rvalue") and (rootDefined) ) : 
            multipleAllowed = True
        elif( (valType == "lvalue") ):
            multipleAllowed = True
        return multipleAllowed

    def commonVisitor(self, ctx  , ruleName):
        try: 
            abc = ctx.getText()
            count = ctx.getChildCount()
            logger.debug( "visitor  :{} : {} ,  child count : ".format( ruleName , abc , count) )        
        except Exception as e:
            log(LOG_ERROR , "Exception in commin visitor : {}".format(e)  )

def isNum(param):
    if (isinstance(param , numbers.Number)):
        return True
    else : 
        return False
    
def isStr(param):
    if (isinstance(param , str)):
        return True
    else : 
        return False

def isFunction(param):
    if param in gFunMap:
        return True
    else :
        return False

def getVar(param):
    ret = cRet()
    if isVariable(param):
        ret.value =  gVarMap[param]
        ret.refs = dict_op.refManager()
        ret.refs.setRef(gVarMap , param)
        ret.retCode = ret.RETCODE_SUCCESS
        return ret
    else:
        ret.retCode = ret.RETCODE_GENERIC_FAILURE
        return ret


def isVariable(param):
    if param in gVarMap:
        return True
    else :
        return False




if __name__ == "__main__"  :
    run_1(ip_file=sys.argv[1])
else :

    # run_1(["test_1_visitor.py","sample.txt"] )
    pass




