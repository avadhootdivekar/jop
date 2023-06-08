package common

import (
	"fmt"
)

const (
	// JT ==> JOP Type
	JT_INVALID  = -1
	JT_NUM      = 1
	JT_STR      = 2
	JT_LIST     = 3
	JT_DICT     = 4
	JT_FUNC     = 5
	LOGFILE     = "zap.conf"
	ERR_GENERIC = "Generic error"
	NS_GLOBAL   = "global"
	NS_LOCAL    = "local"
)

type Intf interface{}

type JI struct {
	Ptr  Intf
	Type int
}

type Status struct {
	Value JI
	Err   error
}

type NAMESPACE map[string]*JI
type NSPACE_COLLECTION map[string]NAMESPACE

func Sample() {
	fmt.Printf("Sample function \n")
}

func (this *JI) Add(B *JI) (C *JI) {
	switch this.Type {
	case JT_NUM:
		if B.Type == JT_NUM {
			val := new(int)
			C.Type = JT_NUM
			C.Ptr = val
		} else {
			panic("Mismatched types")
		}

	}
	return C
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
	var val string
	s = fmt.Sprintf("Type : %v , ptr : %v ", this.Type, this.Ptr)
	switch this.Type {
	case JT_DICT:
		t = "JT_DICT"
		v, ok := this.Ptr.(map[string]*JI)
		if !ok {
			return "Invalid dict"
		}
		val = fmt.Sprintf("%v", v)
		break
	case JT_NUM:
		t = "JT_NUM"
		v, ok := this.Ptr.(int)
		if !ok {
			return "Invalid num"
		}
		val = fmt.Sprintf("%v", v)
		break
	case JT_STR:
		t = "JT_STR"
		v, ok := this.Ptr.(string)
		if !ok {
			return "Invalid str"
		}
		val = fmt.Sprintf("%v", v)
		break
	case JT_LIST:
		t = "JT_LIST"
		v, ok := this.Ptr.([]*JI)
		if !ok {
			return "Invalid list"
		}
		val = fmt.Sprintf("%v", v)
		break

	}
	s = fmt.Sprintf("Type : %v , val : %v ", t, val)
	return s
}

func (this *NAMESPACE) Text() (s string) {
	i := 0
	var m *map[string]*JI
	m = (*map[string]*JI)(this)
	for k, v := range *m {
		i++
		s += fmt.Sprintf("[key : %v , val : %v]  ", k, v)
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
		s += fmt.Sprintf("[key : %v , val : %v]  ", k, v)
	}
	s += fmt.Sprintf(" Count : %v ", i)
	return s
}
