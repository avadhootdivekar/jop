package jop

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	c "jop/common"
	parser "jop/gen"
	"reflect"
	"strconv"

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
var ns c.NSPACE_COLLECTION

func Init() (err error) {
	err = errors.New(c.ERR_GENERIC)
	log, err = configLogger(c.LOGFILE)
	ns = make(map[string]c.NAMESPACE)
	ns[c.NS_GLOBAL] = *c.NewNamespace()
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
	zapConfig.EncoderConfig.EncodeCaller = zapcore.FullCallerEncoder
	logger , err := zapConfig.Build( )
	fmt.Printf("logger : %v , err : %v " , logger , err)
	log = logger.Sugar()
	log.Infof("Created the logger in caller. error : %v " , err)
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
	tree := p.Code()
	t, _ := tree.(*parser.CodeContext)
	v := MyVisitor{}
	log.Debugf("Created visitor.")
	antlr.ParseTreeWalkerDefault.Walk(&jopListener{}, tree)
	v.VisitCode(t)
	return nil
}

func VisitTree() c.JI {
	ret := c.JI{}
	return ret
}

func (v *MyVisitor) VisitCode(ctx *parser.CodeContext) ( ret *c.RET) {
	log.Debugf("This is overloaded Code function.")
	log.Debugf("Text : %v ", ctx.GetText())
	AllLines := ctx.AllLines()
	for i := 0; i < len(AllLines); i++ {
		str, ok := ctx.Lines(i).(*parser.LinesContext)
		if ok {
			v.VisitLines(str)
		} else {
			log.Warnf("Type interface not matching, type : %v ", reflect.TypeOf(ctx.Lines(i)))
		}
	}
	log.Debugf("Final namespace map : [%v] ", ns)
	return nil
}

func (v *MyVisitor) VisitString(ctx *parser.StringsContext) (ret *c.RET) {
	ret = new( c.RET)
	log.Debugf("Entry , ctx : %v ", ctx)
	s := ctx.STR().GetText()
	log.Debugf("String : %v ", s)
	return ret
}

func (v *MyVisitor) VisitLines(ctx *parser.LinesContext) (ret *c.RET) {
	ret = new( c.RET)
	log.Debugf("Entry")
	l := ctx.AllLine()
	for i := 0; i < len(l); i++ {
		l1, ok := ctx.Line(i).(*parser.LineContext)
		if ok {
			v.VisitLine(l1)
		} else {
			log.Warnf("Incoorect type, type : %v ", reflect.TypeOf(ctx.Line(i)))
		}
	}
	return ret
}

func (v *MyVisitor) VisitLine(ctx *parser.LineContext) (ret *c.RET) {
	ret = new( c.RET)
	log.Debugf("Entry")
	cl := ctx.AllCode_line()
	for i := 0; i < len(cl); i++ {
		l1, ok := ctx.Code_line(i).(*parser.Code_lineContext)
		if ok {
			v.VisitCode_line(l1)
		} else {
			log.Warnf("Incoorect type, type : %v ", reflect.TypeOf(ctx.Code_line(i)))
		}
	}
	return ret
}

func (v *MyVisitor) VisitCode_line(ctx *parser.Code_lineContext) (ret *c.RET) {
	ret = new( c.RET)
	log.Debugf("Entry")
	s := ctx.GetText()
	a, ok := ctx.Assign().(*parser.AssignContext)
	if (a != nil) && ok {
		v.VisitAssign(a)
	}
	b, ok := ctx.Rvalue().(*parser.RvalueContext)
	if (b != nil) && ok {
		v.VisitRvalue(b)
	}
	sc := ctx.SEMIC()
	if sc != nil {
		log.Debugf("code line SEMIC : [ %v ]", sc.GetText())
	}
	log.Debugf("code line : [ %v ]", s)
	return ret
}

func (v *MyVisitor) VisitAssign(ctx *parser.AssignContext) (ret *c.RET) {
	ret = new( c.RET)
	log.Debugf("Entry")
	s := ctx.GetText()
	a, ok := ctx.Rvalue().(*parser.RvalueContext)
	value := new(c.JI)

	if (a != nil) && ok {
		r1 := v.VisitRvalue(a)
		log.Debugf("ret : %v , r1 : %v " , ret , r1)
		value = ret.ValueRef
	}

	id, ok := ctx.Id_().(*parser.Id_Context)
	if (id != nil) && ok {
		arg := new(c.ARG)
		r1 := v.VisitId_(id, arg)
		ret = r1
		varName, ok := r1.ValueRef.Ptr.(*string)
		if !ok {
			log.Warnf("Error. Ret : %v , ptrType: %v ", ret.Text() , reflect.TypeOf(r1.ValueRef.Ptr))
			return ret
		}
		ns[c.NS_GLOBAL][*varName] = value
		log.Debugf("Updated namespace : %v " , ns)
	}
	member, ok := ctx.Member().(*parser.MemberContext)
	if (member != nil) && ok {
		v.VisitMember(member)
	}

	log.Debugf("assign : [ %v ]", s)
	return ret
}

func (v *MyVisitor) VisitRvalue(ctx *parser.RvalueContext) (ret *c.RET) {
	log.Debugf("Entry")
	s := ctx.GetText()
	ret = new(c.RET)
	ret.Err = errors.New(c.ERR_GENERIC)

	a, ok := ctx.Member().(*parser.MemberContext)
	if (a != nil) && ok {
		log.Debugf("Member : %v ", a.GetText())
		r1 := v.VisitMember(a)
		return r1
	}
	b, ok := ctx.Uid().(*parser.UidContext)
	if (b != nil) && ok {
		log.Debugf("UID : %v ", b.GetText())
		r1 := v.VisitUid(b)
		return r1
	}
	c1, ok := ctx.Fcall().(*parser.FcallContext)
	if (c1 != nil) && ok {
		log.Debugf("Fcall : %v ", c1.GetText())
		r1 := v.VisitFcall(c1)
		return r1
	}
	d, ok := ctx.Match_b().(*parser.Match_bContext)
	if (d != nil) && ok {
		log.Debugf("Match_b : %v ", d.GetText())
		r1 := v.VisitMatch_b(d)
		return r1
	}
	e, ok := ctx.Curly().(*parser.CurlyContext)
	if (e != nil) && ok {
		log.Debugf("Curly : %v ", e.GetText())
		r1 := v.VisitCurly(e)
		return r1
	}
	f, ok := ctx.List_().(*parser.List_Context)
	if (f != nil) && ok {
		log.Debugf("List_ : %v ", f.GetText())
		r1 := v.VisitList_(f)
		return r1
	}
	g, ok := ctx.Expr().(*parser.ExprContext)
	if (g != nil) && ok {
		log.Debugf("Expr : %v ", g.GetText())
		r1 := v.VisitExpr(g)
		return r1
	}
	h, ok := ctx.Jop_func().(*parser.Jop_funcContext)
	if (h != nil) && ok {
		log.Debugf("JOP Func: %v ", h.GetText())
		r1 := v.VisitJop_func(h)
		return r1
	}
	log.Debugf("rvalue : [ %v ]", s)
	return ret
}

func (v *MyVisitor) VisitMember(ctx *parser.MemberContext) (ret *c.RET) {
	ret = new( c.RET)
	log.Debugf("Entry ")
	s := ctx.GetText()
	log.Debugf("string : [%v] ", s)

	l := ctx.AllMember_candidate()

	for i := 0; i < len(l); i++ {
		cand, ok := ctx.Member_candidate(i).(*parser.Member_candidateContext)
		if (cand != nil) && ok {
			v.VisitMember_candidate(cand)
		}
	}

	id, ok := ctx.Id_().(*parser.Id_Context)
	if (id != nil) && ok {
		arg := new(c.ARG)
		log.Debugf("JOP Func: %v ", id.GetText())
		v.VisitId_(id, arg)
	}
	return ret
}

func (v *MyVisitor) VisitUid(ctx *parser.UidContext) (ret *c.RET) {
	ret = new( c.RET)
	log.Debugf("Entry ")
	s := ctx.GetText()
	log.Debugf("UID : [%v] ", s)

	num, ok := ctx.Num().(*parser.NumContext)
	if (num != nil) && ok {
		log.Debugf("Num: %v ", num.GetText())
		ret = v.VisitNum(num)
	}

	id, ok := ctx.Id_().(*parser.Id_Context)
	if (id != nil) && ok {
		arg := new(c.ARG)
		log.Debugf("ID_: %v ", id.GetText())
		ret = v.VisitId_(id, arg)
	}

	bt, ok := ctx.Bt().(*parser.BtContext)
	if (bt != nil) && ok {
		log.Debugf("BT : %v ", bt.GetText())
		ret = v.VisitBt(bt, c.ARG{})
	}

	bf, ok := ctx.Bf().(*parser.BfContext)
	if (bf != nil) && ok {
		log.Debugf("BF: %v ", bf.GetText())
		ret = v.VisitBf(bf)
	}

	st, ok := ctx.Strings().(*parser.StringsContext)
	if (st != nil) && ok {
		log.Debugf("strings: %v ", st.GetText())
		ret = v.VisitStrings(st)
	}
	log.Debugf("Returning : %v " , ret.Text())
	return ret
}

func (v *MyVisitor) VisitFcall(ctx *parser.FcallContext) (ret *c.RET) {
	ret = new( c.RET)
	log.Debugf("Entry ")
	s := ctx.GetText()
	log.Debugf("fcall : [%v] ", s)
	return ret
}

func (v *MyVisitor) VisitMatch_b(ctx *parser.Match_bContext) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	log.Debugf("Match_b : [%v] ", s)
	return ret
}

func (v *MyVisitor) VisitCurly(ctx *parser.CurlyContext) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	log.Debugf("Curly : [%v] ", s)
	return ret
}

func (v *MyVisitor) VisitList_(ctx *parser.List_Context) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	log.Debugf("List : [%v] ", s)
	return ret
}

func (v *MyVisitor) VisitExpr(ctx *parser.ExprContext) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	log.Debugf("string : [%v] ", s)
	return ret
}

func (v *MyVisitor) VisitJop_func(ctx *parser.Jop_funcContext) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	log.Debugf("string : [%v] ", s)
	return ret
}

func (v *MyVisitor) VisitId_(ctx *parser.Id_Context, pArg *c.ARG) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new(c.RET)
	ret.Err = errors.New(c.ERR_GENERIC)
	s := new(string)
	*s = ctx.GetText()
	log.Debugf("string : [%v] ", s)
	if pArg.GetRef {
		if _, ok := ns[c.NS_GLOBAL][*s]; ok {
			ret.ValueRef = ns[c.NS_GLOBAL][*s]
		} else {
			log.Warnf("Variable [%v] not found. ", s)
			return ret
		}
	} else {
		val := new(c.JI)
		val.Type = c.JT_STR
		val.Ptr = s
		ret.ValueRef = val
	}
	ret.Err = nil
	return ret
}

func (v *MyVisitor) VisitMember_candidate(ctx *parser.Member_candidateContext) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	log.Debugf("string : [%v] ", s)

	k, ok := ctx.Possible_key().(*parser.Possible_keyContext)
	if (k != nil) && ok {
		log.Debugf("Key: %v ", k.GetText())
		v.VisitPossible_key(k)
	}
	l := ctx.AllPossible_num()
	for i := 0; i < len(l); i++ {
		index, ok := ctx.Possible_num(i).(*parser.Possible_numContext)
		if (index != nil) && ok {
			log.Debugf("index: %v ", index.GetText())
			v.VisitPossible_num(index)
		}
	}

	return ret
}

func (v *MyVisitor) VisitPossible_key(ctx *parser.Possible_keyContext) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	log.Debugf("string : [%v] ", s)

	st, ok := ctx.Possible_str().(*parser.Possible_strContext)
	if (st != nil) && ok {
		log.Debugf("Possible str : %v ", st.GetText())
		v.VisitPossible_str(st)
	}

	n, ok := ctx.Possible_num().(*parser.Possible_numContext)
	if (n != nil) && ok {
		log.Debugf("Possible num : %v ", n.GetText())
		v.VisitPossible_num(n)
	}

	b, ok := ctx.Possible_bool().(*parser.Possible_boolContext)
	if (b != nil) && ok {
		log.Debugf("Possible bool : %v ", b.GetText())
		v.VisitPossible_bool(b)
	}
	return ret
}

func (v *MyVisitor) VisitPossible_num(ctx *parser.Possible_numContext) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	log.Debugf("Possible num  : [%v] ", s)

	id, ok := ctx.Id_().(*parser.Id_Context)
	if (id != nil) && ok {
		arg := new(c.ARG)
		log.Debugf("id_ : %v ", id.GetText())
		v.VisitId_(id, arg)
	}

	num, ok := ctx.Num().(*parser.NumContext)
	if (num != nil) && ok {
		log.Debugf("num : %v ", num.GetText())
		v.VisitNum(num)
	}

	mb, ok := ctx.Match_b().(*parser.Match_bContext)
	if (mb != nil) && ok {
		log.Debugf("match b : %v ", mb.GetText())
		v.VisitMatch_b(mb)
	}

	fc, ok := ctx.Fcall().(*parser.FcallContext)
	if (fc != nil) && ok {
		log.Debugf("fcall : %v ", fc.GetText())
		v.VisitFcall(fc)
	}

	return ret
}

func (v *MyVisitor) VisitPossible_str(ctx *parser.Possible_strContext) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	log.Debugf("string : [%v] ", s)

	id, ok := ctx.Id_().(*parser.Id_Context)
	if (id != nil) && ok {
		arg := new(c.ARG)
		log.Debugf("id_ : %v ", id.GetText())
		v.VisitId_(id, arg)
	}

	st, ok := ctx.Strings().(*parser.StringsContext)
	if (st != nil) && ok {
		log.Debugf("strings : %v ", st.GetText())
		v.VisitStrings(st)
	}

	mb, ok := ctx.Match_b().(*parser.Match_bContext)
	if (mb != nil) && ok {
		log.Debugf("match_b : %v ", mb.GetText())
		v.VisitMatch_b(mb)
	}

	f, ok := ctx.Fcall().(*parser.FcallContext)
	if (f != nil) && ok {
		log.Debugf("fcall : %v ", f.GetText())
		v.VisitFcall(f)
	}

	return ret
}

func (v *MyVisitor) VisitPossible_bool(ctx *parser.Possible_boolContext) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	log.Debugf("possible bool : [%v] ", s)
	return ret
}

func (v *MyVisitor) VisitStrings(ctx *parser.StringsContext) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	s1 := new(string)
	*s1 = s
	log.Debugf("string : [%v] ", s)
	ret.ValueRef = new(c.JI)
	ret.ValueRef.Type = c.JT_STR
	ret.ValueRef.Ptr = s1
	return ret
}

func (v *MyVisitor) VisitNum(ctx *parser.NumContext) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new(c.RET)
	value := new(c.JI)
	ret.ValueRef = value
	s := ctx.GetText()
	log.Debugf("num : [%v] ", s)

	if ctx.INT() != nil {
		s = ctx.INT().GetText()
		i, err := strconv.Atoi(s)
		if err != nil {
			log.Warnf("Err : %v ", err)
			value.Type = c.JT_INVALID
			return ret
		}
		j := new(c.JI_INT)
		*j = c.JI_INT(i)
		value.Ptr = j
		value.Type = c.JT_INT
	}

	if ctx.FLT() != nil {
		s = ctx.FLT().GetText()
		f, err := strconv.ParseFloat(s, 64)
		if err != nil {
			log.Warnf("Err : %v ", err)
			value.Type = c.JT_INVALID
			return ret
		}
		g := new(c.JI_FLOAT)
		*g = c.JI_FLOAT(f)
		value.Ptr = g
		value.Type = c.JT_FLT
	}

	log.Debugf("Returning : [%v]", ret.Text())
	return ret
}

func (v *MyVisitor) VisitBt(ctx *parser.BtContext, args c.ARG) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	log.Debugf("BT : [%v] ", s)
	a := new(bool)
	*a = true
	value := new(c.JI)
	value.Type = c.JT_BOOL
	value.Ptr = a
	ret.ValueRef = value
	return ret
}

func (v *MyVisitor) VisitBf(ctx *parser.BfContext) (ret *c.RET) {
	log.Debugf("Entry ")
	ret = new( c.RET)
	s := ctx.GetText()
	log.Debugf("BF : [%v] ", s)
	a := new(bool)
	*a = false
	value := new(c.JI)
	value.Type = c.JT_BOOL
	value.Ptr = a
	ret.ValueRef = value
	return ret
}

func logErr(err error) {
	log.Errorf("Error : %v ", err)
}

// func (v *MyVisitor) Visit__(ctx *parser.LinesContext)(c.RET){
// log.Debugf("Entry ")
// s := ctx.GetText()
// log.Debugf("string : [%v] " , s)
// 	return nil
// }
