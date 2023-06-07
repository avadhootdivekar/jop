package jop

import (
	"fmt"
	"testing"
)

var s1 = `
5 + 4 
// This is a comment
`

func Test_1(*testing.T)(){
	fmt.Printf("Testing...\n")
	// s := "Hello there  // Hi		"
	Process(s1)
}


