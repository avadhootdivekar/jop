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

type JI_BOOL bool
type JI_INT int
type JI_FLOAT float64
type JI_STR string
type JI_LIST []*JI

// Key is JI struct. If value of the structure is same, the key is same thus value / access would be same.
// i.e. Access would still be valid if variable is copied.
// Check example code : https://go.dev/play/p/-gmO-TchReT
type JI_DICT map[JI]*JI
type NAMESPACE map[string]*JI
type NSPACE_COLLECTION map[string]NAMESPACE

// NOTE : Please keep in mind that go compiler checks if variable should go on stack or heap,
//  so var and new can be used interchangably without any concerns.
//  However for sake of clarity, we will prefer new () 

func Sample() {
	log("Sample function \n")
}

func (this *JI_DICT) GetKeys()(ls *[]JI){
	v := new([]JI)
	ls = v
	if this == nil{
		return ls
	}
	for k := range *this{
		*ls = append(*ls, k)		
	}
	return ls
}

func (this *JI)In(ls *JI_LIST)(ret bool){
	if this == nil || ls == nil{
		return false
	}
	for i:=0 ; i<len(*ls) ; i++ {
		if (this.IsEqualVal((*ls)[i]) ){
			return true
		}
	}
	return false
}

func (this *JI)InKeys(d *JI_DICT)(ret bool) {
	if this ==nil || d == nil {
		return false
	}	
	for k := range(*d) {
		if this.IsEqualVal(&k){
			return true
		}
	}
	return false
}

func (this *JI_LIST) GetValueInstance(in *JI)(out *JI , found bool){
	out = nil
	if (this == nil) || (in==nil){
		return out , false
	}
	for i:=0 ; i<len(*this) ; i++ {
		if (in.IsEqualVal((*this)[i]) ){
			out = (*this)[i]
			return out, true
		}
	}
	return out, false
}

func (this *JI_DICT)GetKeyInstance(in *JI)(out *JI , found bool){
	out = nil
	if (this ==nil) || (in == nil ){
		return out, false
	}	
	for k := range(*this) {
		if in.IsEqualVal(&k){
			out = &k
			return out, true
		}
	}
	return out, false
}

func (this *JI_DICT)GetValueInstance(in *JI)(out *JI , found bool){
	out = nil
	if (this ==nil) || (in == nil ){
		return out, false
	}	
	for _ , v := range(*this) {
		if in.IsEqualVal(v){
			out = v
			return out, true
		}
	}
	return out, false
}

func (this *JI)InValue(d *JI_DICT)(ret bool) {
	if this ==nil || d == nil {
		return false
	}	
	for _ , v := range(*d) {
		if this.IsEqualVal(v){
			return true
		}
	}
	return false
}

func (this *JI)IsSimple()(ret bool){
	if this == nil {
		return false
	}
	switch this.Type{
	case JT_BOOL:
		return true
	case JT_INT:
		return true
	case JT_FLT:
		return true
	case JT_STR:
		return true
	case JT_LIST:
		return false
	case JT_DICT:
		return false
	default:
		panic(fmt.Sprintf("Invalid type : %v " , this.Type))
	}
}

func (this *JI)IsSameType(B *JI)(ret bool){
	if (this == nil ) || (B==nil) {
		return false
	}
	if this.Type == B.Type {
		return true
	}
	return false
}


func (this *JI)IsEqualVal(B *JI)(ret bool){
	if (this == nil) && (B == nil) {
		return true
	}
	if (this == nil) || (B == nil) {
		return false
	}
	switch this.Type {
	case JT_INT:
		if this.IsSameType(B) {
			if *(this.Ptr.(*JI_INT)) == *(B.Ptr.(*JI_INT)) {
				return true
			} else { 
				return false
			}
		}else {
			return false
		}
	case JT_FLT:
		if this.IsSameType(B) {
			if *(this.Ptr.(*JI_FLOAT)) == *(B.Ptr.(*JI_FLOAT)) {
				return true
			} else { 
				return false
			}
		}else {
			return false
		}
	case JT_STR:
		if this.IsSameType(B) {
			if *(this.Ptr.(*JI_STR)) == *(B.Ptr.(*JI_STR)) {
				return true
			} else { 
				return false
			}
		}else {
			return false
		}
	case JT_LIST:
		if this.IsSameType(B) {
			j1 := *( this.Ptr.(*JI_LIST) )
			j2 := *( B.Ptr.(*JI_LIST) )
			l1 := len(j1)
			l2 := len(j2)
			if l1 == l2 {
				for i:=0 ; i<l1 ;  i++ {
					if j1[i].IsEqualVal(j2[i]) {
						continue
					} else{
						return false
					}
				}
				return true
			} else { 
				return false
			}
		}else {
			return false
		}
	case JT_DICT:
		if this.IsSameType(B) {
			d1 := *(this.Ptr.(*JI_DICT))
			d2 := *(B.Ptr.(*JI_DICT))
			if len(d1) == len(d2){
				kl1 := d1.GetKeys()
				for i:=0 ; i<len(*kl1) ; i++ {
					if  ((*kl1)[i].InKeys(&d2) ) {
						k2 , ok := d2.GetKeyInstance(&(*kl1)[i])
						if ok &&( d1[(*kl1)[i]].IsEqualVal(d2[*k2])) {
							continue
						} else{
							return false
						}
					} else {
						// log("k1:%v , v1:%v , v2:%v , d1:%v , d2:%v  \n" , &(*kl1)[i]  , d1[(*kl1)[i]] , d2[(*kl1)[i]] , d1 , d2)
						return false
					}
				}
				return true
			} else {
				return false
			}
		}else {
			return false
		}
	default:
		return false
	}
}

func (this *JI) Add(B *JI) (C *JI) {
	C = new(JI)
	switch this.Type {
	case JT_INT:
		if B.Type == JT_FLT {
			val := new(JI_FLOAT)
			C.Type = JT_FLT
			C.Ptr = val
			a, ok := this.Ptr.(*JI_INT)
			if !ok {
				panic(fmt.Sprintf("Incorrect type %v , expected JI_INT" , reflect.TypeOf(this.Ptr) ))
			}
			b, ok := B.Ptr.(JI_FLOAT)
			*val = JI_FLOAT(*a) + b
		} else if B.Type == JT_INT {
			val := new(JI_INT)
			C.Type = JT_INT
			C.Ptr = val
			a, ok := this.Ptr.(*JI_INT)
			if !ok {
				panic(fmt.Sprintf("Incorrect type %v , expected JI_INT" , reflect.TypeOf(this.Ptr) ))
			}
			b, ok := B.Ptr.(*JI_INT)
			*val = *a + *b
		} else {
			panic("Mismatched types")
		}
		break
	case JT_FLT:
		if B.Type == JT_INT {
			val := new(JI_FLOAT)
			C.Type = JT_FLT
			C.Ptr = val
			a, ok := this.Ptr.(*JI_FLOAT)
			if !ok {
				panic(fmt.Sprintf("Incorrect type %v , expected *JI_FLOAT" , reflect.TypeOf(a) ))
			}
			b, ok := B.Ptr.(*JI_INT)
			*val = *a + JI_FLOAT(*b)
		} else if B.Type == JT_FLT {
			val := new(JI_FLOAT)
			C.Type = JT_FLT
			C.Ptr = val
			a, ok := this.Ptr.(*JI_FLOAT)
			if !ok {
				panic(fmt.Sprintf("Incorrect type %v , expected *JI_FLOAT" , reflect.TypeOf(this.Ptr) ))
			}
			b, ok := B.Ptr.(*JI_FLOAT)
			*val = *a + *b
		} else {
			panic("Mismatched types")
		}
		break
	case JT_STR:
		if B.Type == JT_STR {
			val := JI_STR("")
			C.Type = JT_STR
			C.Ptr = &val
			a, ok := this.Ptr.(*JI_STR)
			if !ok {
				panic(fmt.Sprintf("Incorrect type %v , expected *string" , reflect.TypeOf(a) ))
			}
			b, ok := B.Ptr.(*JI_STR)
			if !ok {
				panic(fmt.Sprintf("Incorrect type %v , expected *string" , reflect.TypeOf(a) ))
			}
			val = *a + *b
		} else {
			panic("Mismatched types")
		}
		break
	case JT_LIST:
		if B.Type == JT_LIST {
			var val JI_LIST
			C.Type = JT_LIST
			C.Ptr = &val
			a, ok := this.Ptr.(*JI_LIST)
			if !ok {
				panic(fmt.Sprintf("Incorrect type %v , expected *JI_LIST" , reflect.TypeOf(a) ))
			}
			b, ok := B.Ptr.(*JI_LIST)
			// Append. For elementwise op , check function : ?
			val = append(val, *a...)
			val = append(val, *b...)
		} else {
			panic("Mismatched types")
		}
		break
	case JT_DICT:
		if B.Type == JT_DICT {
			val := make(JI_DICT)
			C.Type = JT_DICT
			C.Ptr = &val
			a, ok := this.Ptr.(*JI_DICT)
			if !ok {
				panic("Incorrect type.")
			}
			b, ok := B.Ptr.(*JI_DICT)
			// Append. For elementwise op , check function : ?
			val = *a
			for k, v := range *b {
				val[k] = v
			}
		} else {
			panic("Mismatched types")
		}
		break
	default:
		panic(fmt.Sprintf("Unsupported type : %v \n", this.Type))
		break

	}
	return C
}

func (this *JI)Sub(B *JI)(ret *JI){
	// Non need for nil check as we SHOULD panic if its nil.
	ret = new(JI)
	switch this.Type{
	case JT_BOOL:
		if B.Type == JT_BOOL {
			val := new(JI_BOOL)
			ret.Ptr = val
			ret.Type = JT_BOOL
			log("What should be done for a-b in bool ? \n")
		} else {
			panic(fmt.Sprintf("Mismatched Types bool vs %v \n" , B.Type) )
		}
		break;
	case JT_INT:
		if (B.Type == JT_INT) {
			val := new(JI_INT)
			ret.Type = JT_INT
			ret.Ptr = val
			aVal := this.Ptr.(*JI_INT)
			bVal := B.Ptr.(*JI_INT)
			*val = *aVal - *bVal
			return ret
		}  else {
			panic(fmt.Sprintf("Mismatched Types JT_INT vs %v \n" , B.Type) )
		}
		break
	case JT_FLT:
		if (B.Type == JT_FLT) {
			val := new(JI_FLOAT)
			ret.Type = JT_FLT
			ret.Ptr = val
			aVal := this.Ptr.(*JI_FLOAT)
			bVal := B.Ptr.(*JI_FLOAT)
			*val = *aVal - *bVal
			return ret
		}  else {
			panic(fmt.Sprintf("Mismatched Types JT_INT vs %v \n" , B.Type) )
		}
		break
	case JT_STR:
		if (B.Type == JT_STR) {
			val := new(JI_STR)
			ret.Type = JT_STR
			ret.Ptr = val
			// aVal := this.Ptr.(*JI_STR)
			// bVal := B.Ptr.(*JI_STR)
			// *val = *aVal - *bVal
			log("What  should be done for a-b in strings? \n")
			return ret
		}  else {
			panic(fmt.Sprintf("Mismatched Types JT_INT vs %v \n" , B.Type) )
		}
		break
	case JT_LIST:
		if (B.Type == JT_LIST) {
			val := new(JI_LIST)
			var val2 *JI
			ret.Type = JT_LIST
			ret.Ptr = val
			aVal := this.Ptr.(*JI_LIST)
			bVal := B.Ptr.(*JI_LIST)
			la := len(*aVal)
			lb := len(*bVal)
			if la != lb {
				panic("Length mismatch\n")
			}
			for i:=0 ; i<la ; i++ {
				val2 = (*aVal)[i].Sub((*bVal)[i])
				*val = append(*val , val2)
			}
			return ret
		}  else {
			panic(fmt.Sprintf("Mismatched Types JT_INT vs %v \n" , B.Type) )
		}
		break
	case JT_DICT:
		if (B.Type == JT_DICT) {
			val := new(JI_DICT)
			ret.Type = JT_DICT
			ret.Ptr = val
			aDict := this.Ptr.(*JI_DICT)
			bDict := B.Ptr.(*JI_DICT)
			ka := aDict.GetKeys()
			kb := bDict.GetKeys()
			if len(*ka) == len(*kb) {
				for i:=0 ; i< len(*ka) ; i++ {
					k := (*ka)[i]
					log("a:%v , b:%v , k:%v , a : %v , b : %v  " , (*aDict)[k] , (*bDict)[k] , k , *aDict , *bDict)
					(*val)[k] = (*aDict)[k].Sub((*bDict)[k])
				}
			} 
			return ret
		}  else {
			panic(fmt.Sprintf("Mismatched Types JT_INT vs %v \n" , B.Type) )
		}
		break
	default:
		panic(fmt.Sprintf("Unsupported Type : %v \n" , this.Type) )
	}
	return ret
}

func NewJI(val Intf)(ret *JI){
	ret = new(JI)
	var v reflect.Value
	if reflect.TypeOf(val) == reflect.TypeOf(reflect.Value{}) {
		v = val.(reflect.Value)
		val = v.Interface()
		log("Its a reflect value\n")
		log("v:%v , vKind:%v , valType:%v \n", v, v.Kind() , reflect.TypeOf(val))
		switch reflect.TypeOf(val) {	
		case reflect.TypeOf(5):
			v = reflect.ValueOf(val.(int))
			log("Type Identified as int \n")
			break
		case reflect.TypeOf(float64(5.4)):
			v = reflect.ValueOf(val.(float64))
			log("Type Identified as float64 \n")
			break
		case reflect.TypeOf("abcd"):
			v = reflect.ValueOf(val.(string))
			log("Type Identified as string \n")
			break
		case reflect.TypeOf(true):
			v = reflect.ValueOf(val.(bool))
			log("Type Identified as bool \n")
			break
		default:
			log("Failed to identify type \n")
			break;

		}
	} else {
		v = reflect.ValueOf(val)
	}

	log("NewJI v:%v , type(v):%v , val:%v , type(val):%v \n" , v , v.Type() , val , reflect.TypeOf(val) )
	switch v.Kind()  {
	case reflect.Bool:
		p := val.(bool)
		ret.Type = JT_BOOL
		ret.Ptr = &p
		log("bool : p : %v \n" , p)
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
		p := JI_STR( val.(string))
		ret.Type = JT_STR
		ret.Ptr = &p
		break;
	case reflect.Slice:
		var a *JI
		array := new(JI_LIST)
		ret.Type = JT_LIST
		for i:=0 ; i< v.Len() ; i++ {
			a = NewJI(v.Index(i).Interface())
			*array = append(*array, a)
		} 
		ret.Ptr = array
		break;
	case reflect.Map:
		iter := v.MapRange()
		var a  JI
		var b *JI
		dictionary := make (JI_DICT)
		ret.Type = JT_DICT
		
		for iter.Next() {
			k := reflect.Indirect(iter.Key())
			v := reflect.Indirect(iter.Value())
			a = *NewJI(k)
			b = NewJI(v)
			dictionary[a] = b
			log("\nAdded key-value to map  k:%v , v:%v , a:%v , b:%v , typek : %v , typev:%v   \n" , k, v, a ,b, k.Kind(),v.Kind() )
		} 
		ret.Ptr = &dictionary
		break
	default:
		log("Failed to generate the JI from %v of type %v. v.Kind :%v \n" , val , reflect.TypeOf(val) , v.Kind() )
		break
	}	
	log("Generated JI : %v \n" , ret)
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

func (this *JI) String() (s string) {
	var t string
	val := ""
	// s = fmt.Sprintf("Type : %v , ptr : %v ", this.Type, this.Ptr)
	switch this.Type {
	case JT_DICT:
		t = "JT_DICT"
		dictionary, ok := this.Ptr.(*JI_DICT)
		if !ok {
			return fmt.Sprintf("Invalid dict , type : [%v] ", reflect.TypeOf(this.Ptr))
		}
		val += "["
		for k,v := range *dictionary {
			val += fmt.Sprintf("%v:%v ," , &k , v)
		}
		val += "]"
		break
	case JT_BOOL:
		t = "JT_BOOL"
		v, ok := this.Ptr.(*bool)
		if !ok {
			return fmt.Sprintf("Invalid int , type : [%v] ", reflect.TypeOf(this.Ptr))
		}
		val = fmt.Sprintf("%v", *v)
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
		v, ok := this.Ptr.(*JI_STR)
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
			val += fmt.Sprintf("%v, " , (*v)[i] )
		}
		val += "]"
		break

	}
	s = fmt.Sprintf("[Type : %v , val : %v]", t, val)
	return s
}

func (this *RET) Text()(s string){
	return fmt.Sprintf("[err : %v , valueRef : %v ]" , this.Err , this.ValueRef)
}

func (this *NAMESPACE) Text() (s string) {
	i := 0
	var m *map[string]*JI
	m = (*map[string]*JI)(this)
	for k, v := range *m {
		i++
		s += fmt.Sprintf("[key : %v , val : %v, ptr : %v ]  ", k, v, v)
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
		s += fmt.Sprintf("[key : %v  , val : %v, ptr : %v ]  ", k, v, v)
	}
	s += fmt.Sprintf(" Count : %v ", i)
	return s
}


func log(s string, args ...interface{}){
	fmt.Printf(s, args...)
	fmt.Printf("\n")
}