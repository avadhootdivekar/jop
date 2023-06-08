package jop

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	c "jop/common"
	parser "jop/gen"

	"github.com/antlr4-go/antlr/v4"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)


type jopListener struct{
	*parser.BasejopListener
}


type MyVisitor struct {
	*parser.BasejopVisitor 
}

var log *zap.SugaredLogger



func Init()(err error){
	err = errors.New(c.ERR_GENERIC)
	log , err = configLogger(c.LOGFILE)
	return err
}

func configLogger(filename string)(log *zap.SugaredLogger , err error){
	file, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil , err
	}
	logConfig := file
	/* Zap config Start			*/
	var zapConfig zap.Config
	err = json.Unmarshal(logConfig, &zapConfig)
	if err != nil {
		fmt.Printf("Failed log config")
		return nil, err
	}
	zapConfig.EncoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	logger := zap.Must(zapConfig.Build())
	log = logger.Sugar()
	log.Info("Created the logger in caller.")
	return log , nil
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
	tree := p.All()
	t , _ := tree.(*parser.AllContext)
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




func (v *MyVisitor) VisitAll(ctx *parser.AllContext) interface{} {
	fmt.Printf("\nThis is overloaded function.\n")
	return nil
}

func (v *MyVisitor) Visit(ctx *parser.AllContext) interface{} {
	fmt.Printf("\nThis is overloaded All function.\n")
	code_ctx,_ :=  ctx.Code(0).(*parser.CodeContext)
	v.VisitCode(code_ctx)
	return nil
}

func (v *MyVisitor) VisitCode(ctx *parser.CodeContext) interface{} {
	fmt.Printf("\nThis is overloaded Code function.\n")
	
	return nil
}





