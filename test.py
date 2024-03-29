import re
import dict_op
import sys
sys.path.append("/home/jop_workspace/antlr/")
import test_1_visitor

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
	q = r 
	print(" Q : {} , R : {} ".format(q , r ) )
	q.updateValue("latest value")
	print(" Q : {} , R : {} ".format(q , r ) )
	return 

def test4() : 

	v1={"a1" : "v1" , "a2" : "v2" , "a3" : {"a4" : "v4" , "a5" : {"a6" : "v6" , "a2" : "v3.2"} , "a2" : "v2.2" }}
	v2={"b1" : "vb1" , "b2" : "vb2" , "b3" : {"b4" : "vb4" , "b5" : {"b6" : "vb6"}}}
	m = dict_op.matchCriteria()
	m.level = -1
	m.key = "a2"
	out = dict_op.getRefs(v1 , m)
	print("Output length : {} , {}".format(len(out) , out) )
	for i in range(len(out)):
		print("Output {} : {}".format( i , out[i].getValue()[1]) )

	v4 = dict_op.ji()
	print("V4 : {}".format(v4) )
	v4.getRandom(maxDepth=3 , maxWidth=4,  maxStrLen=10 , maxNum=100000)
	print("V4 : \n{}\n Depth : {}".format(v4 , v4.depth()) )
	v4.getRandom(maxDepth=0, maxWidth=4 , maxStrLen=10 , maxNum=100000)
	print("V4 : \n{}\nDepth : {}".format(v4, v4.depth()) )
	return

def test5():
	test_1_visitor.run_1(ip_string="ret=50;")
	return 

def test6():
	v1 = {"A" : None}
	r = dict_op.refManager()
	r.setRef(v1 , key = "A")
	print("v1 : {}  , r : {}".format(v1 , r) )
	r.createAccessNestedLists([3 , 5 , 2])
	print("v1 : {}  , r : {}".format(v1 , r) )
	r.updateValue({"alpha" : "beta"})
	print("v1 : {}  , r : {}".format(v1 , r) )

	return


def test7():
	v1={"a1" : "v1" , "a2" : "v2" , "a3" : {"a4" : "v4" , "a5" : {"a6" : "v6" , "a2" : "v3.2"} , "a2" : "v2.2" }}
	v2={"b1" : "vb1" , "b2" : "vb2" , "b3" : {"b4" : "vb4" , "b5" : {"b6" : "vb6"}} , "a3" : {"ab1" : "vab1"}}
	v3={"b1" : "vb1" , "b2" : "vb2" , "b3" : {"b4" : "vb4" , "b5" : {"b6" : "vb6"}} , "a3" : {"a4" : "vab3"}}
	j1 = dict_op.ji(v1)
	j2 = dict_op.ji(v2)
	j3 = dict_op.ji(v3)
	print ("RES 1 : \nj1 : {} \nj2 : {} ".format(j1 , j2 ) )
	j4 = j1.union(j2)
	print ("RES 2 : \nj1 : {} \nj2 : {} \n j4 : {}\n".format(j1 , j2 , j4) )
	j4 = j1.intersection(j2)
	print ("RES 3 : \nj1 : {} \nj2 : {} \n j4 : {}\n".format(j1 , j2 , j4) )
	j4 = j1.intersection(j3)
	print ("RES 3 : \nj1 : {} \nj2 : {} \n j4 : {}\n".format(j1 , j2 , j4) )

# op_check()
# test2()
# test3()
# test4()
# test5()
test7()

