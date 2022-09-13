import os 

TOKENS = ['.' , '+' , '-' , '*' , '/' , '\"' , '\\' , '<' , '>' , '=']
KEYWORDS = ["value" , "key" , "true" , "false" , "zero" , "null"]
STACK = []
VARIABLES = []

LOG_ERROR               = 1
LOG_WARNING             = 2
LOG_INFO                = 3
LOG_DEBUG               = 4
LOG_FILTER_LEVEL        = 4




def log( logLevel , msg):
    if logLevel <= LOG_FILTER_LEVEL:
        print(logLevelToString(logLevel) + " : " + msg)

def f1() :
    print ("Hello world.")
    f = read_file("sample.txt")
    print("file : \n" + f)

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
    

if __name__ == "__main__"  :
    f1()