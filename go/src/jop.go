package jop

import (
	"fmt"
	c "jop/common"
	parser "jop/gen"

	"github.com/antlr4-go/antlr/v4"
)


type jopListener struct{
	*parser.BasejopListener
}


type MyVisitor struct {
	*parser.BasejopVisitor 
}

func helloJop(){
	fmt.Printf("Hello JOP. \n")
}

func Process(s string)(){
	lexer := ProcInputStream(s)
	parser := ProcTokenStream(lexer)
	fmt.Printf("Parser : %v " , parser)
}

func ProcInputStream(s string)(lexer antlr.Lexer){
	istream := antlr.NewInputStream(s)
	lexer = parser.NewjopLexer(istream)
	fmt.Printf("Lexer : %v " , lexer)
	return lexer
}

func ProcTokenStream(lexer antlr.Lexer)(err error){
	tokens := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)
	p := parser.NewjopParser(tokens)
	tree := p.Code()
	t , _ := tree.(*parser.CodeContext)
	v := MyVisitor{}
	fmt.Printf("Created visitor.\n")
	antlr.ParseTreeWalkerDefault.Walk(&jopListener{} , tree)
	v.Visit(t)
	return nil
}

func VisitTree()(c.JI){
	ret := c.JI{}
	return ret
}




func (v *MyVisitor) VisitCode(ctx *parser.CodeContext) interface{} {
	fmt.Printf("\nThis is overloaded function.\n")
	return v.VisitChildren(ctx)
}

func (v *MyVisitor) Visit(ctx *parser.CodeContext) interface{} {
	fmt.Printf("\nThis is overloaded function.\n")
	return nil
}



