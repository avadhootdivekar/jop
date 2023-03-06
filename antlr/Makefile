build:
	antlr4 -Werror -Dlanguage=Java test_1.g4 -visitor ;			\
	antlr4 -Werror -Dlanguage=Python3 test_1.g4 -visitor ;

run : 
	python3 test_1_visitor.py sample.txt ;