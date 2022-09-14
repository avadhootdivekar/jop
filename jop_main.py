import os 

OPS_SP_CHARS = ['.' , '+' , '-' , '*' , '/' , '\"' , '\\' , '<' , '>' , '=' , '{' , '}' , '(' , ')' , ' ' , '\n']
KEYWORDS = ["value" , "key" , "true" , "false" , "zero" , "null"]
STACK = []
VARIABLES = []

LOG_ERROR               = 1
LOG_WARNING             = 2
LOG_INFO                = 3
LOG_DEBUG               = 4
LOG_VERBOSE             = 5
LOG_FILTER_LEVEL        = 5



def logLevelToString(logLevel):
    '''
    Return log level as string from provided loglevel number.
    '''
    logLevelString = "undefined"
    if logLevel     == LOG_ERROR : 
        logLevelString = "ERROR"
    elif logLevel   == LOG_WARNING : 
        logLevelString = "WARNING"
    elif logLevel   == LOG_INFO : 
        logLevelString = "INFO"
    elif logLevel   == LOG_DEBUG : 
        logLevelString = "DEBUG"
    return logLevelString
    
def log( logLevel , msg):
    if logLevel <= LOG_FILTER_LEVEL:
        print(logLevelToString(logLevel) + " : " + msg)

def f1() :
    print ("Hello world.")
    f = read_file("sample.txt")
    print("file : \n" + f)
    while len(f) > 0 :
        token , f = getToken(f)
        STACK.append(token)
    log(LOG_DEBUG ,  "tokens : " + str(STACK) )

def read_file(filename) :
    file_handle = open(filename , "r")
    file_contents = file_handle.read()
    file_handle.close()
    return file_contents

def scan_new_line(contents) :

    return True

def parseToken(token , contents) :
    if (token == '.') :
        op1 = STACK.pop()
        op2 = getOperand(contents) 
        
    return None

def isString(word) :
    if ( type(word) == str ) : 
        log(LOG_DEBUG , "string : " + word)
        return True

def isNumber(word) :
    if ( (type(word) == int) or (type(word) == float) ) : 
        return True

def isVariable(word) : 
    if ( word in VARIABLES ) : 
        return True

def isKeyword(word):
    if ( word in KEYWORDS) : 
        return True


def parseFile(filename):
    contents        = read_file(filename)
    

def getToken(contents):
    token = ""
    if contents[0] in OPS_SP_CHARS:
        token = contents[0]
        contents = contents[1:]
    else:
        i=0
        while contents[i] not in OPS_SP_CHARS:
            i += 1
            if (i >= len(contents)) :
                break 
        token = contents[0:i]
        contents = contents[i:]
    log(LOG_DEBUG , "token : " + str(token) + " , contents : " + contents)
    return token , contents



def getRValue():
    log(LOG_VERBOSE , "Getting RValue")

def isRValue(token):
    log(LOG_VERBOSE , "Getting RValue")
    if (isNumber(token) or isVariable(token) or isString(token)) : 
        log(LOG_VERBOSE , "Token : "+token+" is RValue")
        return True
    else:
        return False


def getMember(parent , key):
    if key in parent : 
        return parent[key]
    else :
        log(LOG_WARNING , "Incorrect member access. No member : " + str(key))
        return None



if __name__ == "__main__"  :
    f1()