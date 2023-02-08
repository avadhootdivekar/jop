import re
import dict_op

def run_1() : 
	text = "alpha delta gallon Sigma and some $pec!@l chars."
	e = "al.*?o"
	match = re.search(e , text)
	print("matc h: {}".format(match))
	if match != None : 
		print("value : match : {}".format(match[0]))

		
#run_1()

def op_check():
	v1={"a1" : "v1" , "a2" : "v2" , "a3" : {"a4" : "v4" , "a5" : {"a6" : "v6"}}}
	v2={"b1" : "vb1" , "b2" : "vb2" , "b3" : {"b4" : "vb4" , "b5" : {"b6" : "vb6"}}}
	v3={"a1" : "vc1" , "a2" : "vc2" , "a3" : {"a4" : "vc4" , "a5" : {"a6" : "vc6"}}}
	n1={"a1" : 10 , "a2" : 12 , "a3" : {"a4" : 16 , "a5" : { "a6" : 19}}}
	n2={"a1" : 100 , "a2" : 120 , "a3" : {"a4" : 160 , "a5" : { "a6" : 190}}}
	n3={"b1" : 27 , "b2" : 25 , "b3" : {"b4" : 22 , "b5" : { "a6" : 21}}}
	a=dict_op.ji()
	j1 = dict_op.ji()
	j2 = dict_op.ji()
	j3 = dict_op.ji()

	jd1 = dict_op.ji()
	jd2 = dict_op.ji()
	jd3 = dict_op.ji()

	jd1.scan(n1)
	jd2.scan(n2)
	jd3.scan(n3)

	j1.scan(v1)
	j2.scan(v2)
	j3.scan(v3)
	print(a)
	a["new"]="new_val"
	print("a type : [{}] , a : [{}]".format( type(a) , a) )
	print("j1 type : [{}] , j1 : [{}]".format( type(j1) , j1) )
	j4 = j1 + j2;
	print("j4 type : [{}] , j4 : [{}]".format( type(j4) , j4) )
	j5 = j1 + j3;
	print("j5 type : [{}] , j5 : [{}]".format( type(j5) , j5) )

	o5 = jd1 * jd2 
	print("o5 type : [{}] , o5 : [{}]".format( type(o5) , o5) )

	o6 = jd1.union(jd3)
	print("o6 type : [{}] , o6 : [{}] , o6 depth = {} , leaf count  : {} ".format( type(o6) , o6 , o6.depth() , o6.countLeaves()) )
	k = o6.getRandomKey()
	print("random key : {} ".format(k))
	k , v = o6.getRandomPair(depth=1)
	print("random key : {} , value : {}  ".format(k , v))


def test2():
	v1={"a1" : "v1" , "a2" : "v2" , "a3" : {"a4" : "v4" , "a5" : {"a6" : "v6"}}}
	v2={"b1" : "vb1" , "b2" : "vb2" , "b3" : {"b4" : "vb4" , "b5" : {"b6" : "vb6"}}}
	v3=v2.copy()
	print ("v2 : {}   ,    v3 : {} ".format(v2, v3) )
	v3.__delitem__("b2")
	print ("v2 : {}   ,    v3 : {} ".format(v2, v3) )
	j1=dict_op.ji(v1)
	j2=dict_op.ji(v3)
	print("j1 : [{}]".format(j1))
	print("j2 : [{}]".format(j2))
	j1.filter(level=0 , key="a1")
	print("After filter j1 : [{}]".format(j1))

	j2.filter(level=1 ,  keyRegex=r"b[0-4]")
	print("After filter j2 : [{}] , v2 : [{}]".format(j2 , v2))

	j2.scan(v2)
	print("Reinitialize j2 : {} ".format(j2))
	j2.filter(level=0 , value="vb2")
	print("After filter j2 : [{}]\n\n".format(j2))

	# Check valueRegex.
	j2.scan(v2)
	print("Reinitialize j2 : {} ".format(j2))
	j2.filter(level=1 , valueRegex="vb\d")
	print("After filter j2 : [{}]".format(j2))


def test3():

	v1={"a1" : "v1" , "a2" : "v2" , "a3" : {"a4" : "v4" , "a5" : {"a6" : "v6"}}}
	v2={"b1" : "vb1" , "b2" : "vb2" , "b3" : {"b4" : "vb4" , "b5" : {"b6" : "vb6"}}}
	r = dict_op.refManager()
	print("Original V1 : {}".format(v1))
	r.setRef(v1 , key="a2")
	print( "r : [{}] \nRequested value : [{}] ".format( r , r.getValue() ) )
	r.updateValue("newValue")
	print( "Updated V1 : {}".format(v1) )

	return 

# op_check()
# test2()

test3()