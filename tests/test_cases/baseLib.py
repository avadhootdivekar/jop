import sys
sys.path.append("/home/jop_workspace/")
sys.path.append("/home/jop_workspace/antlr/")
import test_1_visitor
import dict_op
import random
class baseLib():
	def __init__(self):
		print("Hello world")

	def test_new(self , *args ):
		print("Hello world2 !! args : {}".format(args))
		return "Hello world!!!"

	def run_file_and_check_output(self , input_file = None , expected_op_file = None):
		import test_1_visitor
		result = False
		ret = None
		ret = test_1_visitor.run_1(ip_file=input_file)
		s = "Return value from jop service is : \n{}\n".format(ret)
		print(s)
		with open(expected_op_file , "r") as f_exp:
			expected_output = f_exp.read()
			print("expected output : \n{}\n".format(expected_output))
			s_op = "{}".format(ret)
			if (s_op == expected_output):
				result = True
			else : 
				raise Exception()

	def random_op_check(self):
		import test_1_visitor
		iter = 10
		for i in range(iter):
			maxDepth = random.randint(1,25)
			s = '''
ret = jop.random(maxDepth={});
			'''.format(maxDepth)
			ret = test_1_visitor.run_1(ip_string = s)
			act_depth = dict_op.depth(ret["value"]) 
			print("Max depth : {} , actual depth : {}  , Dict : \n{}\n".format(maxDepth , act_depth , ret["value"]) )
			assert((act_depth <= maxDepth) )