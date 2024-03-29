import logging
import pdb 
import numbers
import random
import re
import copy
import string

# pdb.set_trace()

logFormat="[%(asctime)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=logFormat ,  level=logging.DEBUG , filename="/var/log/dict_op.log" )
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
	


	def createAccessNestedLists(self , indexArr):
		'''
		Create or access the nested list element as specified by indexArr
		e.g. indexArr = [2,4,5] will 
			- create list [ None, None , [None , None , None , None , [None , None , None , None , None , *None* ]]]
			- If all the list members at indices 2 , 4 and 5 are already present, it will return the value of that element. 
			it is equivalent to access list[2][4][5]
		'''
		log.debug("indexArr : {}".format(indexArr) )
		depth = len(indexArr)
		if (isinstance(indexArr , list)):
			for i in range(depth):
				l = indexArr[i]
				if (isinstance(l , int)) and (l >= 0):
					ok , v = self.getValue()
					if ok and (not isinstance(v , list)):
						self.updateValue([])
						ok , v = self.getValue()
						log.debug("Created new dictionary at depth : {} , self : {} , v : {} ".format(i , self , v) )						
						if not ok :
							log.warning("Failed to get value of new entry.")
					else : 
						log.debug("ok : {} , v : {} ".format(ok , v) )
					actLen = len(v)
					log.debug("actLen : {} , l : {} ".format(actLen , l) )
					if ((actLen <= l)):
						for j in range(l-actLen+1):
							v.append(None)
					self.setRef(v , index=l)
					log.debug("Updated ref to nested index {}".format(l) )
		else : 
			log.warning("Invalid params, indexArr : {}".format(indexArr) )
		return

class matchCriteria():

	key 		= None
	keyRegex	= None
	value 		= None
	valueRegex	= None
	refs 		= None
	level       = 0
	matchType	= None
	complement	= False

	MATCH_ALL							= "all"
	MATCH_DEL_NON_MATCHING_LEVELS		= "del_nonmatch_level"

	def __init__(self) : 
		pass

	def __str__(self):
		d = {"key" : self.key , "keyRegex" : self.keyRegex , "value" : self.value ,
       			"valueRegex" : self.valueRegex , "refs" : self.refs , "level" : self.level,
				"complement" : self.complement }
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
		'''
		Copy the dictionary a (Deep copy) to self.
		'''
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

	def getRandomKey(self):
		'''
		Returns a random key at the top level.
		'''
		k , v = random.choice(list(self.items()))
		return k

	def getRandomPair(self , depth=-1):
		'''
		Get a random pair at the specified depth. Returns the key , value tuple
		'''
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
			elif isinstance(v , list) and  ( ( k in b.keys() ) and isinstance(b[k] , list)):
				maxLen = len(v)
				for i in range(len(b[k])) : 
					if i > maxLen:
						break
					c[k][i] = c[k][i] + b[k][i]
		log.debug("Final retvalue : [[{}]]".format(c) )
		return c 

	def __sub__(self , b ):
		c = ji(copy.deepcopy(self))
		for k,v in c.items():
			log.debug(" keys : {}".format(k))
			if  isinstance(v , numbers.Number) :
				if k in b.keys():
					c[k] -= b[k]
			elif isinstance(v , dict) and ( ( k in b.keys() ) and isinstance(b[k] , dict)):
				c[k] = ji(c[k]) - ji(b[k])
				log.debug("Subtracting dictionary.\n")
			elif isinstance(v , list) and  ( ( k in b.keys() ) and isinstance(b[k] , list)):
				maxLen = len(v)
				for i in range(len(b[k])) : 
					if i > maxLen:
						break
					c[k][i] = c[k][i] - b[k][i]
			else : 
				log.warning("Subtraction not supported for type [{}] .".format(type(v)))
		log.debug("Final retvalue : [[{}]]".format(c) )
		return c 

	def __or__(self , b):
		c = ji(copy.deepcopy(self))
		for k,v in c.items():
			log.debug(" keys : {}".format(k))
			if  isinstance(v , numbers.Number) :
				if k in b.keys():
					c[k] |= b[k]
			elif isinstance(v , dict)  and ( ( k in b.keys() ) and isinstance(b[k] , dict)):
				c[k] = ji(c[k]) | ji(b[k])
				log.debug("Operation OR (|) on dictionaries [[ {} ]]  , [[ {} ]] .\n".format(ji(c[k]) , ji(b[k])) )
			elif isinstance(v , list) and  ( ( k in b.keys() ) and isinstance(b[k] , list)):
				maxLen = len(v)
				for i in range(len(b[k])) : 
					if i > maxLen:
						break
					c[k][i] = c[k][i] | b[k][i]
		log.debug("Final retvalue : [[{}]]".format(c) )
		return c

	def __and__(self, b):
		c = ji(copy.deepcopy(self))
		for k,v in c.items():
			log.debug(" keys : {}".format(k))
			if  isinstance(v , numbers.Number) :
				if k in b.keys():
					c[k] &= b[k]
			elif isinstance(v , dict)  and ( ( k in b.keys() ) and isinstance(b[k] , dict)):
				c[k] = ji(c[k]) & ji(b[k])
				log.debug("Operation And on dictionaries. [[ {} ]]  and [[ {} ]] \n".format(ji(c[k]) , ji(b[k]) ) )
			elif isinstance(v , list) and  ( ( k in b.keys() ) and isinstance(b[k] , list)):
				maxLen = len(v)
				for i in range(len(b[k])) : 
					if i > maxLen:
						break
					c[k][i] = c[k][i] & b[k][i]
		log.debug("Final retvalue : [[{}]]".format(c) )
		return c

	def __truediv__(self, b ):
		c = ji(copy.deepcopy(self))
		for k,v in c.items():
			log.debug(" keys : {}".format(k))
			if  isinstance(v , numbers.Number) :
				if k in b.keys():
					c[k] /= b[k]
			elif isinstance(v , dict)  and ( ( k in b.keys() ) and isinstance(b[k] , dict)):
				c[k] = ji(c[k]) / ji(b[k])
				log.debug("Operation Divide (/) on dictionaries [[{}]] , [[{}]].\n".format(ji(c[k]) , ji(b[k])))
			elif isinstance(v , list) and  ( ( k in b.keys() ) and isinstance(b[k] , list)):
				maxLen = len(v)
				for i in range(len(b[k])) : 
					if i > maxLen:
						break
					c[k][i] = c[k][i] / b[k][i]
		log.debug("Final retvalue : [[{}]]".format(c) )
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
				log.debug("Operation Multiply (*) on dictionaries : [[{}]] , [[{}]].\n".format( ji(c[k])  , ji(b[k]) ) )
			elif isinstance(v , list) and  ( ( k in b.keys() ) and isinstance(b[k] , list)):
				maxLen = len(v)
				for i in range(len(b[k])) : 
					if i > maxLen:
						break
					c[k][i] = c[k][i] * b[k][i]
		log.debug("Final retvalue : [[{}]]".format(c) )
		return c
	
	def union(self , b , recursive : bool = True):
		'''
		Union of self and b
		'''
		c = ji(copy.deepcopy(self))
		if isinstance(b , dict) or isinstance(b , ji) :
			log.debug("Union")
			c = union(self , b , recursive=recursive)
		else:
			log.warning(" Unable to union with type [{}] operand b [{}] ".format(type(b) , b ) );
		return c

	def intersection(self , b , recursive : bool = True):
		c = intersection(self , b , recursive=recursive)
		return c

	def diff(self , b , recursive:bool = True):
		'''
		A.diff(B) returns the result of set operation (A - B). The keys present in B will be deleted from the A. 
		If resursive == True, even common keys in B will be subtracted from keys in A at successive matching levels.
		e.g. A."k1"."k2" is present and B."k1" is present but B."k1"."k2" is not present, 
		then A."k1" will be kept but A."k1"."k2" will be deleted.  
		'''		
		return diff(self , b , recursive=recursive)

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
	'''
	Generate a random dictionary conforming to the specified constraints.
	'''
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
		elif maxDepth == 1:
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
	'''
	Get a random variable of any type (num , str , dict, list). list and dict are complex types. 
	Specify the constraints on the generated variable. 
	'''
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




def filter( root = {} , m:matchCriteria = None ):
	'''
	Filter a dictionary (root) as per matchCriteria m. Delete all non matching elements.
	Returns a list of references of type refManager
	'''
	ret = []
	log.debug("Filtering for match : {}".format(m) )
	retDefault = None
	if None == m : 
		log.warning("None match as argument. ")
	if ( (m.key != None) and (m.keyRegex != None) ):
		log.warning("Both key and keyRegex specified. ")
		return retDefault
	if ( (m.value != None) and (m.valueRegex != None) ):
		log.warning("Both value and valueRegex specified. ")
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
				if (keyMatch or valueMatch) != (m.complement):
					ret = refManager()
					ret.setRef(obj=root , key=k)
					log.debug("Match found for key [{}]".format(k))
				else:
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

	

def getRefs(root:dict , m:matchCriteria):
	'''
	Provide references to all the members mataching with matchCriteria m.
	Returns array of refManager instances
	'''
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




def union(a , b , recursive : bool = True ):
	log.debug("a : {} , b : {} , recursive : {}".format(a , b , recursive) )
	if ( (isinstance(a , dict) or (isinstance(a , ji)))  and 
     		(isinstance(b , dict) or isinstance(b , ji) ) ):
		a = copy.deepcopy(a)
		keys_a = a.keys()
		for k , v in b.items():
			log.debug("k : {} ".format(k) )
			if not (k in keys_a):	
				a[k] = b[k]
			else : 
				if ( (isinstance(a[k] , dict) or isinstance(a[k] , ji) ) and 
					(isinstance(b[k] , dict) or isinstance(b[k] , ji) ) ) : 
					a[k] = union(a[k] , b[k])
	return a


def intersection(a : dict , b : dict , recursive=True):
	'''
	Return the dictionary containing items present in both the dictionaries. 
	Keys which match are retained. If values differ and values are dictionaries,  
	intersection is applied again to both the values.
	'''
	log.debug("a : {} , b : {} , recursive : {}".format(a , b , recursive) )
	if ( (isinstance(a , dict) or (isinstance(a , ji)))  and 
     		(isinstance(b , dict) or isinstance(b , ji) ) ):
		a = copy.deepcopy(a)
		keys_a = list(a.keys())
		keys_b = list(b.keys())
		for k in keys_a:
			log.debug("k : {} ".format(k) )
			if not (k in keys_b):
				a.__delitem__(k)
			elif (recursive) : 
				if ( (isinstance(a[k] , dict) or isinstance(a[k] , ji) ) and 
					(isinstance(b[k] , dict) or isinstance(b[k] , ji) ) ) : 
					a[k] = intersection(a[k] , b[k])
			# else :   	 Do nothing , a[k] = a[k]

	log.debug("returning a : {}".format(a) )
	return	a

def diff (a:dict , b:dict , recursive:bool = True):
	log.debug("a : {} , b : {} , recursive : {}".format(a , b , recursive) )
	if ( (isinstance(a , dict) or (isinstance(a , ji)))  and 
     		(isinstance(b , dict) or isinstance(b , ji) ) ):
		a = copy.deepcopy(a)
		keys_a = list(a.keys())
		keys_b = list(b.keys())
		for k in keys_a:
			log.debug("k : {} ".format(k) )
			if (k in keys_b):
				log.debug("deleting k : {} ".format(k) )
				a.__delitem__(k)
			# else : Do nothing a[k] = a[k]
			# No recursion consideration here. If any common element, that will be deleted
			# Thus , recursion will not happen.
	# else : Do nothing, operation not possible
	log.debug("returning c : {}".format(a) )
	return a




