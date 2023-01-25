import logging
import pdb 
import numbers
import random

# pdb.set_trace()

logging.basicConfig(level=logging.DEBUG)
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

class ji (dict ):
	def __init__(self , a={}):
		super(ji , self ).update(a) 

	def depth(self):
		return depth(self)

	def countLeaves(self):
		return countLeaves(self)

	def getDict(self):
		a = self.copy()
		return a

	def scan(self , a):
		if isinstance(a , dict):
			for k , v in a.items():
				self.__setitem__(k , v)
			log.debug("Scan Dictionary : {}  ,self : {} \n".format(a , self))
			return True
		else :
			return False

	def __add__(self , b ):
		c = ji(self.copy())
		for k,v in c.items():
			log.debug(" keys : {}".format(k))
			if  isinstance(v , numbers.Number) or (isinstance(v , str)):
				if k in b.keys():
					c[k] += b[k]
			elif isinstance(v , dict) and ( ( k in b.keys() ) and isinstance(b[k] , dict)):
				c[k] = ji(c[k]) + ji(b[k])
				logging.debug("Adding dictionary.\n")
		return c 

	def getRandomKey(self):
		k , v = random.choice(list(self.items()))
		return k

	def getRandomPair(self , depth=-1):
		logging.debug("Random pair current node is : [{}]. ".format(self) ) 
		if (-1 == depth) : 
			depth = random.randrange(self.depth())
		if 1 == depth :
			logging.debug("depth = 1 and current node is : [{}]. ".format(self) ) 
			k = self.getRandomKey()
			return k , self[k]
		d = 0
		while d < (depth-1):
			k = self.getRandomKey()
			logging.debug("Checking for : {} ".format(k) )
			if isinstance(self[k] , dict ) or isinstance(self[k] , ji):
				d = ji(self[k]).depth()
		return ji(self[k]).getRandomPair(depth -1)
		

	def __sub__(self , b ):
		c = ji(self.copy())
		for k,v in c.items():
			log.debug(" keys : {}".format(k))
			if  isinstance(v , numbers.Number) or (isinstance(v , str)):
				if k in b.keys():
					c[k] -= b[k]
			elif isinstance(v , dict) and ( ( k in b.keys() ) and isinstance(b[k] , dict)):
				c[k] = ji(c[k]) - ji(b[k])
				logging.debug("Adding dictionary.\n")
		return c 

	def __mul__(self , b ):
		c = ji(self.copy())
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
		c = ji(self.copy())
		if isinstance(b , dict) or isinstance(b , ji) :
			c.update(b)
		else:
			logging.warning(" Unable to union with type [{}] operand b [{}] ".format(type(b) , b ) );
		return c

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
