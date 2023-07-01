package jop

import (
	"fmt"
	"testing"
	c "jop/common"
)

var s1 = `
a = 5  ;
d = 5385093485 ;
f = true ;
b = "This is a string."    ;
a = 7+7;
alpha = (p.q + s.t) ;

// This is a comment
{
	c = 10;
}


`

func Test_1(*testing.T) {
	fmt.Printf("Testing...\n")
	err := Init()
	if err != nil {
		fmt.Printf("Init failed. \n")
	}
	log.Debugf("Log configured. ")

	// s := "Hello there  // Hi		"
	Process(s1)
}


func Test_NewJI(t *testing.T){
	A := c.NewJI(5)
	log.Debugf("A : %v " , A.Text())
	A = c.NewJI("abra ca dabra")
	log.Debugf("A : %v " , A.Text())
	A = c.NewJI([]c.Intf{"abcd" , 567 , true})
	log.Debugf("A : %v " , A.Text())
	A = c.NewJI(map[c.Intf]c.Intf { 45 : 56})
	log.Debugf("A : %v " , A.Text())

}