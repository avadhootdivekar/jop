import logging
import pdb 
import numbers
import random
import re
import copy
import string

# pdb.set_trace()

logFormat="[%(asctime)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=logFormat ,  level=logging.DEBUG , filename="/var/log/dict_op.log")
log = logging.getLogger(__name__.split('.')[0])

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

union=Infix(lambda x , y : union(x,y))

class refManager():

	obj 			= None
	index 			= None
	key 			= None
	absoluteRef 	= False
	internalDict	= None
	defaultKey		= "DEFAULT_KEY"

	def __init__(self):
		return
	
	def __str__(self):
		return " obj : [{}] , key : [{}] , index : [{}]  ".format(self.obj , self.key , self.index)

	def setRef(self , obj , key = None , index = None):
		success = False
		if (None != obj)  : 
			if ( isinstance(obj , str) or isinstance(obj , numbers.Number) ):
				log.warning("Unable to reference simple object : {} of type [{}]".format(obj , type(obj)) )
			self.obj = obj
			if ( isinstance(self.obj , dict) and (None != key) ):
				self.key 			= key
				self.absoluteRef 	= False
				self.internalDict 	= None
				self.index 			= None
				success = True
			elif ( isinstance(self.obj , list) and ( isinstance(index , int) and (len(self.obj) > index) ) ) :
				self.index 			= index
				self.absoluteRef 	= False
				self.internalDict 	= None
				self.key 			= None
				success 			= True
			elif ((isinstance(self.obj , dict) and (None == key)) or ( isinstance(self.obj , list) and (None == index) )) :
				self.internalDict 	= {}
				self.internalDict[self.defaultKey] = obj
				self.absoluteRef 	= True
				self.key 			= None
				self.index 			= None
				log.debug("Set absolute ref for type : [{}]".format(type(obj)) )
				success = True
			else : 
				success = False
		else :  
			success = False
		if (not success):
			log.warning("Invalid parameters. obj : [{}] , key : [{}] , index : [{}]".format(obj , key , index) )
		return success
	
	def updateValue(self , value=None):
		success = False
		if (self.absoluteRef ):
			self.internalDict[self.defaultKey] = value
			success = True
		elif (isinstance(self.obj , dict) and (self.key != None) ):
			if (self.key in self.obj) :
				self.obj[self.key] = value
				success = True
			else : 
				log.warning("key : [{}] not found in obj : [{}]".format(self.key , self.obj) )
		elif ( isinstance(self.obj , list) and (isinstance(self.index , int)) ) :
			if (len(self.obj) > self.index):
				self.obj[self.index] = value
				success = True
			else : 
				log.warning("Index [{}] out of bounds for list : [{}]. ".format(self.index , self.obj) )
		else : 
			log.warning("Reference not valid. obj : [{}] , key : [{}] , index : [{}]".format(self.obj , self.key , self.index) )
		return success
	
	def getValue(self):
		success = False
		value = None
		if (self.absoluteRef):
			if ( self.defaultKey in self.internalDict.keys()):
				value = self.internalDict[self.defaultKey]
				success = True
			else : 
				log.warning("Unable to get value from Internal dict : {} ".format(self.internalDict) )
		if (isinstance(self.obj , dict) and (self.key != None) ):
			if (self.key in self.obj) :
				value = self.obj[self.key]
				success = True
			else : 
				log.warning("key : [{}] not found in obj : [{}]".format(self.key , self.obj) )
		elif ( isinstance(self.obj , list) and (isinstance(self.index , int)) ) :
			if (len(self.obj) > self.index):
				value = self.obj[self.index] 
				success = True
			else : 
				log.warning("Index [{}] out of bounds for list : [{}]. ".format(self.index , self.obj) )
		else : 
			log.warning("Reference not valid. obj : [{}] , key : [{}] , index : [{}]".format(self.obj , self.key , self.index) )
		return success , value

class matchCriteria():

	key 		= None
	keyRegex	= None
	value 		= None
	valueRegex	= None
	refs 		= None
	level       = 0
	matchType	= None

	MATCH_ALL							= "all"
	MATCH_DEL_NON_MATCHING_LEVELS		= "del_nonmatch_level"

	def __init__(self) : 
		pass

	def __str__(self):
		d = {"key" : self.key , "keyRegex" : self.keyRegex , "value" : self.value ,
       			"valueRegex" : self.valueRegex , "refs" : self.refs , "level" : self.level}
		return "{}".format(d)

class response():
	RET_FAILURE = "RET_FAILURE"
	RET_SUCCESS = "RET_SUCCESS"
	def __init__(self):
		self.ret = self.RET_FAILURE

class ji (dict ):
	def __init__(self , a={}):
		super().clear()
		super().update(copy.deepcopy(a)) 

	def depth(self):
		return depth(self)

	def countLeaves(self):
		return countLeaves(self)

	def getDict(self):
		a = copy.deepcopy(self)
		return a

	def scan(self , a):
		vCopy=None
		if isinstance(a , dict):
			for k , v in a.items():
				if (isinstance(v , dict) or isinstance(v , ji) ):
					vCopy = copy.deepcopy(v)
				else : 
					vCopy = v
				self.__setitem__(k , vCopy)
			log.debug("Scan Dictionary : {}  ,self : {} \n".format(a , self))
			return True
		else :
			return False

	def __add__(self , b ):
		c = ji(copy.deepcopy(self))
		for k,v in c.items():
			log.debug(" keys : {}".format(k))
			if  isinstance(v , numbers.Number) or (isinstance(v , str)):
				if k in b.keys():
					c[k] += b[k]
			elif isinstance(v , dict) and ( ( k in b.keys() ) and isinstance(b[k] , dict)):
				c[k] = ji(c[k]) + ji(b[k])
				log.debug("Adding dictionary.\n")
		return c 

	def getRandomKey(self):
		k , v = random.choice(list(self.items()))
		return k

	def getRandomPair(self , depth=-1):
		log.debug("Random pair current node is : [{}]. ".format(self) ) 
		if (-1 == depth) : 
			depth = random.randrange(self.depth())
		if 1 == depth :
			log.debug("depth = 1 and current node is : [{}]. ".format(self) ) 
			k = self.getRandomKey()
			return k , self[k]
		d = 0
		while d < (depth-1):
			k = self.getRandomKey()
			log.debug("Checking for : {} ".format(k) )
			if isinstance(self[k] , dict ) or isinstance(self[k] , ji):
				d = ji(self[k]).depth()
		return ji(self[k]).getRandomPair(depth -1)
		

	def __sub__(self , b ):
		c = ji(copy.deepcopy(self))
		for k,v in c.items():
			log.debug(" keys : {}".format(k))
			if  isinstance(v , numbers.Number) :
				if k in b.keys():
					c[k] -= b[k]
			elif isinstance(v , dict) and ( ( k in b.keys() ) and isinstance(b[k] , dict)):
				c[k] = ji(c[k]) - ji(b[k])
				logging.debug("Subtracting dictionary.\n")
			else : 
				log.warning("Subtraction not supported for type [{}] .".format(type(v)))
		return c 

	def __mul__(self , b ):
		c = ji(copy.deepcopy(self))
		for k,v in c.items():
			log.debug(" keys : {}".format(k))
			if  isinstance(v , numbers.Number) :
				if k in b.keys():
					c[k] *= b[k]
			elif isinstance(v , dict)  and ( ( k in b.keys() ) and isinstance(b[k] , dict)):
				c[k] = ji(c[k]) * ji(b[k])
				logging.debug("Adding dictionary.\n")
		return c
	
	def union(self , b):
		c = ji(copy.deepcopy(self))
		if isinstance(b , dict) or isinstance(b , ji) :
			c.update(b)
		else:
			logging.warning(" Unable to union with type [{}] operand b [{}] ".format(type(b) , b ) );
		return c
	
	def filter(self , m = None ):
		log.debug("Filtering for matchCriteria : {}".format(m) )
		if ( m == None):
			log.warning("No match criteria specified.")
		elif (m.key != None and m.keyRegex != None):
			log.info("Key as well as keyRegex specified, please spcify only one.")
		# Do same for value
		return filter(root=self , m = m)
	
	def getRandom(self ,  maxDepth=0 , maxWidth=10 , fixDepth=False , fixWidth=False , maxStrLen=100 , maxNum=100) :
		super().clear()
		ret = getRandom(maxDepth=maxDepth , maxWidth=maxWidth , fixDepth=fixDepth , fixWidth=fixWidth , maxStrLen=maxStrLen , maxNum=maxNum)
		super().update(ret)
		return ret

def getRandom( maxDepth=0 , maxWidth=10 , fixDepth=False , fixWidth=False , maxStrLen = 100 , maxNum=10000):
	log.debug("maxWidth : {} , maxDepth : {} , maxStrLen : {} , maxNum : {} ".format(
				maxWidth , maxDepth , maxStrLen , maxNum
	) )
	width = int( random.random() * maxWidth )
	log.debug("width = {}".format(width) )
	if width == 0:
		width = 1
	ret= {}
	for i in range(width):
		log.debug("For {}-th member".format(i) )
		v = None
		k = getRandomTypeValue(complex=False, maxStrLen=maxStrLen , maxNum=maxNum)
		if maxDepth > 1:
			if fixDepth :
				v = getRandom(maxDepth= (maxDepth-1) , maxWidth=maxWidth , fixDepth=fixDepth , fixWidth=fixWidth , maxStrLen=maxStrLen , maxNum=maxNum)
			else : 
				if random.randint(1,10) > 5:
					v = getRandom(maxDepth= (maxDepth-1) , maxWidth=maxWidth , fixDepth=fixDepth , fixWidth=fixWidth, maxStrLen=maxStrLen , maxNum=maxNum)
				else :
					v = getRandomTypeValue(complex=False, maxStrLen=maxStrLen , maxNum=maxNum)
			ret.update({k:v})
		elif maxDepth == 0:
			k = getRandomTypeValue(complex=False, maxStrLen=maxStrLen , maxNum=maxNum)
			v = getRandomTypeValue(complex=False, maxStrLen=maxStrLen , maxNum=maxNum)
			ret.update({k:v})
	log.debug("Generated random dict : {}".format(ret) )
	return ret
	

def depth(a):
	if isinstance(a, ji) or isinstance(a , dict):
		return 1 + (max(map(depth, a.values())) if a else 0)
	return 0

def countLeaves(a , count=0):
	if isinstance(a, ji) or isinstance(a , dict):
		return count +( sum(map(countLeaves , a.values()))) if a else 0
	else :
		return count + 1

def getRandomTypeValue(complex=True , maxNum = 100 , maxStrLen = 100 , maxArrayLen=100):
	_typeMin  = 1
	_typeNum  = 1
	_typeStr  = 2
	_typeArr  = 3
	_typeDict = 4
	_typeMax  = 4

	ret = None

	if not complex:
		r = random.randint(_typeNum , _typeStr)
	else : 
		r = random.randint(_typeMin , _typeMax)

	if r == _typeNum :
		ret = random.random() * maxNum
	elif r == _typeStr : 
		ret = "".join(random.choices(string.ascii_letters + string.digits ,
			        k = maxStrLen))
	elif (r == _typeArr):
		ret = []
		len = int( random.random() * maxArrayLen )
		for i in range(len):
			ret.append(getRandomTypeValue(complex=False, maxStrLen=maxStrLen , maxNum=maxNum))
	elif (r == _typeDict):
		k = getRandomTypeValue(complex=False, maxStrLen=maxStrLen , maxNum=maxNum)
		v = getRandomTypeValue(complex=False, maxStrLen=maxStrLen , maxNum=maxNum)
		log.debug("key : {}  , value : {}".format(k,v) )
		ret = {k:v}
	else : 
		log.warning("Incorrect type {}".format(r) )
	log.debug("Returning random Value : {}".format(ret) )
	return ret




def filter( root = {} , m = None ):
	ret = []
	log.debug("Filtering for match : {}".format(m) )
	retDefault = None
	if None == m : 
		log.warning("None match as argument. ")
	if ( (m.key != None) and (m.keyRegex != None) ):
		log.warning("Both key and keyRegex specified. ")
		return retDefault
	if ( (m.value != None) and (m.valueRegex != None) ):
		log.warning("Both key and keyRegex specified. ")
		return retDefault
	if (type(root) == dict ) or (type(root) == ji ) : 
		for k , v  in list(root.items()):
			keyMatch = False
			valueMatch = False
			if ( 0 == m.level) : 
				if (m.keyRegex != None):
					log.debug("Searching for regex [{}] in key [{}]".format(m.keyRegex , k) )
					pattern = re.compile(m.keyRegex)
					match = pattern.match(k)
					if (match != None):
						keyMatch = True
				if (m.valueRegex != None):
					log.debug("Searching for regex [{}] in key [{}]".format(m.valueRegex , v) )
					pattern = re.compile(m.valueRegex)
					if (isinstance(v , str)):
						match = pattern.match(v)
						if (match != None):
							valueMatch = True
				if (m.key != None) and (m.key == k ):
					keyMatch = True
				if (m.value != None) and (m.value == v ):
					valueMatch = True				
				if keyMatch or valueMatch:
					ret = refManager()
					ret.setRef(obj=root , key=k)
					log.debug("Match found for key [{}]".format(k))
				else :
					log.debug("No match, deleting key [{}] from root [{}]".format(k , root))
					root.__delitem__(k) 
			elif ( m.level > 0) : 
				log.debug(" m : {} , k : {} , value : {} ".format(m , k , v) )
				if ( isinstance(v , dict) or isinstance(v , ji) ):
					newM = copy.deepcopy(m)
					newM.level = m.level - 1
					ref = filter(root=v , m = newM)
					if (isinstance(ref , list) and (len(ref) > 0)) : 
						ret = ret + ref
					elif (isinstance(ref , refManager ) ):
						ret.append(refManager)
					elif (ref == None  or (isinstance(ref , list) and len(ref)==0 ) ) :
						if (m.matchType == m.MATCH_DEL_NON_MATCHING_LEVELS) :
							log.warning("Deleting item {} from {}".format(k , root))
							root.__delitem__(k)
					else : 
						log.warning("Ref [{}] received and discarded. ".format(ref) )
				elif ( m.matchType ==  m.MATCH_DEL_NON_MATCHING_LEVELS) : 
							log.warning("Deleting item {} from {}".format(k , root))
							root.__delitem__(k)						
			else : 
				log.warning("Incorrect level [{}]".format(level))
	else : 
		log.warning("Incorrect root [{}]".format(root))
	log.debug("Ret is : [{}]".format(ret))
	return ret

	

def getRefs(root , m):
	arr = []
	log.debug(" Root : {} , m : {} ".format(root , m) )
	if ( not (isinstance(root , dict ) or isinstance(root , ji)) ):
		log.error("Incorrrect root of type [{}] defined : {}".format(type(root) , root) )
		return arr
	if (not isinstance(m , matchCriteria) ) : 
		log.error("Incorrect matchCriteria [type : {} ] , value : {}".format(type(m) , m ) )
		return arr
	if (m.level == 0   or   m.level == -1 ) : 
		for k,v in root.items() :
			match = False
			if ( (m.matchType == m.MATCH_ALL) or k == m.key   or v == m.value):
				match = True
				# TODO : Add regex support
			if match : 
				r = refManager()
				r.setRef(root , k)
				arr.append(r)
	if (m.level > 0 or  m.level == -1): 
		if (m.level > 0):
			newM = copy.deepcopy(m)
			newM.level = newM.level - 1
		else : 
			newM = m
		for k , v  in root.items() : 
			r = getRefs(v , newM )
			if (len(r) > 0 ):
				for i in range(len(r)):
					arr.append(r[i]) 
	return arr