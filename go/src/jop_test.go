package jop

import (
	"fmt"
	"testing"
)

var s1 = `
a = 5  ;
b = "This is a string."    ;
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
