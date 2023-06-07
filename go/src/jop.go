package jop

import (
	"fmt"
	c "jop/common"
	parser "jop/gen"

	"github.com/antlr4-go/antlr/v4"
)


func helloJop(){
	fmt.Printf("Hello JOP. \n")
}


func ProcInputStream(s string)(c.JI){
	ret := c.JI{}
	istream := antlr.NewInputStream(s)
	lexer := parser.NewjopLexer(istream)
	fmt.Printf("Lexer : %v " , lexer)
	return ret
}

func ProcTokenStream()(c.JI){
	ret := c.JI{}
	return ret
}

func VisitTree()(c.JI){
	ret := c.JI{}
	return ret
}







