package common

import (
	"fmt"
)

const (
	// JT ==> JOP Type 
	JT_NUM 		= 1
	JT_STR 		= 2
	JT_LIST 	= 3
	JT_DICT 	= 4
)


type Intf interface{}

type JI struct {
	Ptr Intf 
	Type int
}

type Status struct{
	Value 		JI
	Err 		error
}

func Sample()(){
	fmt.Printf("Sample function \n")
}