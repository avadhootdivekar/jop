package jop

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	c "jop/common"
	parser "jop/gen"
	"reflect"

	"github.com/antlr4-go/antlr/v4"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

type jopListener struct {
	*parser.BasejopListener
}

type MyVisitor struct {
	*parser.BasejopVisitor
}

var log *zap.SugaredLogger
var nm c.NSPACE_COLLECTION

func Init() (err error) {
	err = errors.New(c.ERR_GENERIC)
	log, err = configLogger(c.LOGFILE)
	nm = make(map[string]c.NAMESPACE)
	nm[c.NS_GLOBAL] = *c.NewNamespace()
	return err
}

func configLogger(filename string) (log *zap.SugaredLogger, err error) {
	file, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Printf("Error [%v] reading file [%v] ", err, filename)
		return nil, err
	}
	logConfig := file
	/* Zap config Start			*/
	var zapConfig zap.Config
	err = json.Unmarshal(logConfig, &zapConfig)
	if err != nil {
		fmt.Printf("Invalid json [%v]", err)
		return nil, err
	}
	zapConfig.EncoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	logger := zap.Must(zapConfig.Build())
	log = logger.Sugar()
	log.Info("Created the logger in caller.")
	return log, nil
}

func helloJop() {
	fmt.Printf("Hello JOP. \n")
}

func Process(s string) {
	lexer := ProcInputStream(s)
	parser := ProcTokenStream(lexer)
	log.Debugf("Parser : %v ", parser)
}

func ProcInputStream(s string) (lexer antlr.Lexer) {
	istream := antlr.NewInputStream(s)
	lexer = parser.NewjopLexer(istream)
	log.Debugf("Lexer : %v ", lexer)
	return lexer
}

func ProcTokenStream(lexer antlr.Lexer) (err error) {
	tokens := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)
	p := parser.NewjopParser(tokens)
	tree := p.All()
	t, _ := tree.(*parser.AllContext)
	v := MyVisitor{}
	log.Debugf("Created visitor.")
	antlr.ParseTreeWalkerDefault.Walk(&jopListener{}, tree)
	v.Visit(t)
	return nil
}

func VisitTree() c.JI {
	ret := c.JI{}
	return ret
}

func (v *MyVisitor) VisitAll(ctx *parser.AllContext) interface{} {
	log.Debugf("This is overloaded function.")
	return nil
}

func (v *MyVisitor) Visit(ctx *parser.AllContext) interface{} {
	log.Debugf("This is overloaded All function.")
	ls := ctx.AllCode()
	for i := 0; i < len(ls); i++ {
		code_ctx, _ := ctx.Code(i).(*parser.CodeContext)
		v.VisitCode(code_ctx)
	}
	return nil
}

func (v *MyVisitor) VisitCode(ctx *parser.CodeContext) interface{} {
	log.Debugf("This is overloaded Code function.")
	log.Debugf("Text : %v ", ctx.GetText())
	AllLines := ctx.AllLines()
	for i := 0; i < len(AllLines); i++ {
		str, ok := ctx.Lines(0).(*parser.LinesContext)
		if ok {
			v.VisitLines(str)
		} else {
			log.Warnf("Type interface not matching, type : %v ", reflect.TypeOf(ctx.Lines(0)))
		}
	}
	return nil
}

func (v *MyVisitor) VisitString(ctx *parser.StringContext) c.Intf {
	log.Debugf("Entry , ctx : %v ", ctx)
	s := ctx.STR(0).GetText()
	log.Debugf("String : %v ", s)
	return nil
}

func (v *MyVisitor) VisitLines(ctx *parser.LinesContext) c.Intf {
	log.Debugf("Entry")
	assign := ctx.AllAssign()
	for i := 0; i < len(assign); i++ {
		log.Debugf("i : %v ", i)
		a, ok := ctx.Assign(i).(*parser.AssignContext)
		if !ok {
			log.Errorf("assign context incorrect.")
		}
		v.VisitAssign(a)
	}
	return nil
}

func (v *MyVisitor) VisitAssign(ctx *parser.AssignContext) c.Intf {
	id := ctx.ID().GetText()
	rvalue := ctx.Rvalue().GetText()
	val := new(c.JI)
	val.Ptr = rvalue
	val.Type = c.JT_STR
	log.Debugf("JI : %v ", val.Text())
	nm[c.NS_GLOBAL][id] = val
	log.Debugf("Map : %v ", nm.Text())
	log.Debugf("ID : %v , rvalue : %v , nm : %v  ", id, rvalue, nm)
	return nil
}

func logErr(err error) {
	log.Errorf("Error : %v ", err)
}

// func (v *MyVisitor) Visit__(ctx *parser.LinesContext)(c.Intf){
// 	return nil
// }
