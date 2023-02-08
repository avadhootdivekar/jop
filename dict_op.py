import logging
import pdb 
import numbers
import random
import re
import copy

# pdb.set_trace()

logFormat="[%(asctime)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=logFormat ,  level=logging.DEBUG , filename="dict_op.log")
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

	obj = None
	index = None
	key = None

	def __init__(self):
		return
	
	def __str__(self):
		return " obj : [{}] , key : [{}] , index : [{}]  ".format(self.obj , self.key , self.index)

	def setRef(self , obj , key = None , index = None):
		success = False
		if (None != obj) and ( (None != index ) or (None != key) ) : 
			self.obj = obj
			if ( isinstance(self.obj , dict) and (None != key) ):
				self.key = key
				success = True
			elif ( isinstance(self.obj , list) and ( isinstance(index , int) and (len(self.obj) > index) ) ) :
				self.index = index
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
		if (isinstance(self.obj , dict) and (self.key != None) ):
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


class response():
	RET_FAILURE = "RET_FAILURE"
	RET_SUCCESS = "RET_SUCCESS"
	def __init__(self):
		self.ret = self.RET_FAILURE

class ji (dict ):
	def __init__(self , a={}):
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
	
	def filter(self , level=0 , key=None , value=None, keyRegex=None , valueRegex=None ):
		log.debug("Filtering for level [{}] , key [{}] , value [{}] , keyRegex [{}] , valueRegex [{}]".format(level , key , value , keyRegex , valueRegex) )
		if ( (key != None) and (keyRegex != None) ):
			log.info("Key as well as keyRegex specified, please spcify only one.")
		# Do same for value
		return filter(root=self , level=level , key=key , keyRegex=keyRegex , value=value , valueRegex=valueRegex)

def depth(a):
	if isinstance(a, ji) or isinstance(a , dict):
		return 1 + (max(map(depth, a.values())) if a else 0)
	return 0

def countLeaves(a , count=0):
	if isinstance(a, ji) or isinstance(a , dict):
		return count +( sum(map(countLeaves , a.values()))) if a else 0
	else :
		return count + 1



def getRandom(maxDepth=0):
	for i in range(maxDepth):
		getRandom()


def filter( root = {} , level=0 , key=None , value=None, keyRegex=None , valueRegex=None ):
	ret = []
	log.debug("Filtering for level [{}] , key [{}] , value [{}] , keyRegex [{}] , valueRegex [{}]".format(level , key , value , keyRegex , valueRegex) )
	retDefault = None
	if ( (key != None) and (keyRegex != None) ):
		log.warning("Both key and keyRegex specified. ")
		return retDefault
	if ( (value != None) and (valueRegex != None) ):
		log.warning("Both key and keyRegex specified. ")
		return retDefault
	if (type(root) == dict ) or (type(root) == ji ) : 
		for k , v  in list(root.items()):
			keyMatch = False
			valueMatch = False
			if ( 0 == level) : 
				if (keyRegex != None):
					log.debug("Searching for regex [{}] in key [{}]".format(keyRegex , k) )
					pattern = re.compile(keyRegex)
					match = pattern.match(k)
					if (match != None):
						keyMatch = True
				if (valueRegex != None):
					log.debug("Searching for regex [{}] in key [{}]".format(valueRegex , v) )
					pattern = re.compile(valueRegex)
					if (isinstance(v , str)):
						match = pattern.match(v)
						if (match != None):
							valueMatch = True
				if (key != None) and (key == k ):
					keyMatch = True
				if (value != None) and (value == v ):
					valueMatch = True				
				if keyMatch or valueMatch:
					ret = refManager()
					ret.setRef(obj=root , key=k)
					log.debug("Match found for key [{}]".format(k))
				else :
					log.debug("No match, deleting key [{}] from root [{}]".format(k , root))
					root.__delitem__(k) 
			elif ( level > 0) : 
				if ( isinstance(v , dict) or isinstance(v , ji) ):
					ref = filter(root=v , level=(level-1) , key=key , keyRegex=keyRegex , value=value , valueRegex=valueRegex)
					if (isinstance(ref , list)) : 
						ret = ret + ref
					elif (isinstance(ref , refManager ) ):
						ret.append(refManager)
					elif (ref == None) : 
						pass
					else : 
						log.warning("Ref [{}] received and discarded. ".format(ref) )
						
			else : 
				log.warning("Incorrect level [{}]".format(level))
	else : 
		log.warning("Incorrect root [{}]".format(root))
	log.debug("Ret is : [{}]".format(ret))
	return ret

	

