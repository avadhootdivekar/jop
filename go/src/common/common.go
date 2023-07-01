package common

import (
	"fmt"
	"reflect"
)

const (
	// JT ==> JOP Type
	JT_INVALID              = -1
	JT_INT                  = 1
	JT_FLT                  = 2
	JT_STR                  = 3
	JT_LIST                 = 4
	JT_DICT                 = 5
	JT_FUNC                 = 6
	JT_BOOL                 = 7
	LOGFILE                 = "zap.conf"
	NS_GLOBAL               = "global"
	NS_LOCAL                = "local"
	ERR_GENERIC             = "Generic error"
	ERR_INVALID_PARAMS      = "Invalid params"
	ERR_INSUFFICIENT_MEMORY = "Insufficient memory"
)

type Intf interface{}

type JI struct {
	Ptr  Intf
	Type int
}

type ARG struct {
	ValueRef *JI
	GetRef   bool // Indicate that caller expects reference to be returned - NOT value.
}

type RET struct {
	ValueRef *JI
	Err      error
}

type Status struct {
	Value JI
	Err   error
}

type JI_INT int
type JI_FLOAT float64
type JI_LIST []*JI
type JI_DICT map[JI]*JI
type NAMESPACE map[string]*JI
type NSPACE_COLLECTION map[string]NAMESPACE

// NOTE : Please keep in mind that go compiler checks if variable should go on stack or heap,
//  so var and new can be used interchangably without any concerns.
//  However for sake of clarity, we will prefer new () 

func Sample() {
	fmt.Printf("Sample function \n")
}

func (this *JI) Add(B *JI) (C *JI) {
	C = new(JI)
	switch this.Type {
	case JT_INT:
		if B.Type == JT_FLT {
			val := new(JI_FLOAT)
			C.Type = JT_FLT
			C.Ptr = val
			a, ok := this.Ptr.(JI_INT)
			if !ok {
				panic("Incorrect type.")
			}
			b, ok := B.Ptr.(JI_FLOAT)
			*val = JI_FLOAT(a) + b
		} else if B.Type == JT_INT {
			val := new(JI_INT)
			C.Type = JT_INT
			C.Ptr = val
			a, ok := this.Ptr.(JI_INT)
			if !ok {
				panic("Incorrect type.")
			}
			b, ok := B.Ptr.(JI_INT)
			*val = a + b

		} else {
			panic("Mismatched types")
		}
		break
	case JT_FLT:
		if B.Type == JT_INT {
			val := new(JI_FLOAT)
			C.Type = JT_FLT
			C.Ptr = val
			a, ok := this.Ptr.(JI_FLOAT)
			if !ok {
				panic("Incorrect type.")
			}
			b, ok := B.Ptr.(JI_INT)
			*val = a + JI_FLOAT(b)
		} else if B.Type == JT_FLT {
			val := new(JI_FLOAT)
			C.Type = JT_FLT
			C.Ptr = val
			a, ok := this.Ptr.(JI_FLOAT)
			if !ok {
				panic("Incorrect type.")
			}
			b, ok := B.Ptr.(JI_FLOAT)
			*val = a + b
		} else {
			panic("Mismatched types")
		}
		break
	case JT_STR:
		if B.Type == JT_STR {
			val := ""
			C.Type = JT_STR
			C.Ptr = &val
			a, ok := this.Ptr.(string)
			if !ok {
				panic("Incorrect type.")
			}
			b, ok := B.Ptr.(string)
			if !ok {
				panic("Incorrect type.")
			}
			val = a + b
		} else {
			panic("Mismatched types")
		}
		break
	case JT_LIST:
		if B.Type == JT_LIST {
			var val JI_LIST
			C.Type = JT_LIST
			C.Ptr = &val
			a, ok := this.Ptr.(JI_LIST)
			if !ok {
				panic("Incorrect type.")
			}
			b, ok := B.Ptr.(JI_LIST)
			// Append. For elementwise op , check function : ?
			val = append(val, a...)
			val = append(val, b...)
		} else {
			panic("Mismatched types")
		}
		break
	case JT_DICT:
		if B.Type == JT_DICT {
			val := make(JI_DICT)
			C.Type = JT_DICT
			C.Ptr = &val
			a, ok := this.Ptr.(JI_DICT)
			if !ok {
				panic("Incorrect type.")
			}
			b, ok := B.Ptr.(JI_DICT)
			// Append. For elementwise op , check function : ?
			val = a
			for k, v := range b {
				val[k] = v
			}
		} else {
			panic("Mismatched types")
		}
		break
	default:
		panic(fmt.Sprintf("Unsupported type : %v ", this.Type))
		break

	}
	return C
}

func NewJI(val Intf)(ret *JI){
	ret = new(JI)
	v := reflect.ValueOf(val)
	switch v.Kind()  {
	case reflect.Bool:
		p := val.(bool)
		ret.Type = JT_BOOL
		ret.Ptr = &p
		break;
	case reflect.Int:
		p := JI_INT( val.(int))
		ret.Type = JT_INT
		ret.Ptr = &p
		break;
	case reflect.Float32:
		p := JI_FLOAT(val.(float32) )
		ret.Type = JT_FLT
		ret.Ptr = &p
		break;
	case reflect.Float64:
		p := JI_FLOAT( val.(float64))
		ret.Type = JT_FLT
		ret.Ptr = &p
		break;
	case reflect.String:
		p := val.(string)
		ret.Type = JT_STR
		ret.Ptr = &p
		break;
	case reflect.Slice:
		p := val.([] Intf)
		var a *JI
		array := new(JI_LIST)
		ret.Type = JT_LIST
		for i:=0 ; i< len(p) ; i++ {
			a = NewJI(p[i])
			*array = append(*array, a)
			fmt.Printf("\npi : %v , a : %v \n" , p[i] , a.Text())
		} 
		ret.Ptr = array
		break;
	case reflect.Map:
		p := val.(map [Intf] Intf)
		var a  JI
		var b *JI
		dictionary := make (JI_DICT)
		ret.Type = JT_DICT
		for k,v := range p {
			a = *NewJI(k)
			b = NewJI(v)
			dictionary[a] = b
		} 
		ret.Ptr = &dictionary
		break
	default:
		fmt.Printf("Failed to generate the JI from %v of type %v" , val , reflect.TypeOf(val))
		break
	}	
	return ret
}

func (this *NAMESPACE) GetVarValue(s string) (out *JI) {
	out = new(JI)
	if val, ok := (*this)[s]; ok {
		*out = *val
	} else {
		out.Ptr = nil
		out.Type = JT_INVALID
	}
	return out
}

func (this *NAMESPACE) GetVarRef(s string) (out *JI) {
	out = new(JI)
	if val, ok := (*this)[s]; ok {
		// Original out is grbage collected.
		out = val
	} else {
		out.Ptr = nil
		out.Type = JT_INVALID
	}
	return out
}

func (this *NAMESPACE) Contains(s string) (out bool) {
	if _, ok := (*this)[s]; ok {
		return true
	} else {
		return false
	}
}

func NewNamespace() (out *NAMESPACE) {
	var m NAMESPACE
	m = make(map[string]*JI)
	out = &m
	return out
}

func (this *JI) Text() (s string) {
	var t string
	val := ""
	// s = fmt.Sprintf("Type : %v , ptr : %v ", this.Type, this.Ptr)
	switch this.Type {
	case JT_DICT:
		t = "JT_DICT"
		v, ok := this.Ptr.(*JI_DICT)
		if !ok {
			return fmt.Sprintf("Invalid dict , type : [%v] ", reflect.TypeOf(this.Ptr))
		}
		val += "["
		for k,v := range *v {
			val += fmt.Sprintf("%v:%v ," , k.Text() , v.Text())
		}
		val += "]"
		break
	case JT_INT:
		t = "JT_INT"
		v, ok := this.Ptr.(*JI_INT)
		if !ok {
			return fmt.Sprintf("Invalid int , type : [%v] ", reflect.TypeOf(this.Ptr))
		}
		val = fmt.Sprintf("%v", *v)
		break
	case JT_FLT:
		t = "JT_FLT"
		v, ok := this.Ptr.(*JI_FLOAT)
		if !ok {
			return fmt.Sprintf("Invalid float , type : [%v] ", reflect.TypeOf(this.Ptr))
		}
		val = fmt.Sprintf("%v", *v)
		break
	case JT_STR:
		t = "JT_STR"
		v, ok := this.Ptr.(*string)
		if !ok {
			return fmt.Sprintf("Invalid string , type : [%v] ", reflect.TypeOf(this.Ptr))
		}
		val = fmt.Sprintf("%v", *v)
		break
	case JT_LIST:
		t = "JT_LIST"
		v, ok := this.Ptr.(*JI_LIST)
		if !ok {
			return fmt.Sprintf("Invalid list , type : [%v] ", reflect.TypeOf(this.Ptr))
		}
		val = "["
		for i :=0 ; i<len(*v) ; i++ {
			val += fmt.Sprintf("%v, " , (*v)[i].Text() )
		}
		val += "]"
		break

	}
	s = fmt.Sprintf("[Type : %v , val : %v]", t, val)
	return s
}

func (this *RET) Text()(s string){
	return fmt.Sprintf("[err : %v , valueRef : %v ]" , this.Err , this.ValueRef.Text())
}

func (this *NAMESPACE) Text() (s string) {
	i := 0
	var m *map[string]*JI
	m = (*map[string]*JI)(this)
	for k, v := range *m {
		i++
		s += fmt.Sprintf("[key : %v , val : %v, ptr : %v ]  ", k, v.Text(), v)
	}
	s += fmt.Sprintf(" Count : %v ", i)
	return s
}

func (this *NSPACE_COLLECTION) Text() (s string) {

	i := 0
	var m *map[string]NAMESPACE
	m = (*map[string]NAMESPACE)(this)
	for k, v := range *m {
		i++
		s += fmt.Sprintf("[key : %v  , val : %v, ptr : %v ]  ", k, v.Text(), v)
	}
	s += fmt.Sprintf(" Count : %v ", i)
	return s
}


