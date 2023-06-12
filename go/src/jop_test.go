package jop

import (
	"fmt"
	"testing"
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
