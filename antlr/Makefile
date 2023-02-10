build:
	antlr4 -Dlanguage=Java test_1.g4 -visitor ;			\
	antlr4 -Dlanguage=Python3 test_1.g4 -visitor ;

run : 
	python3 test_1_visitor.py sample.txt ;