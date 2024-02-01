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
	log.Debugf("A : %v " , A)
	A = c.NewJI("abra ca dabra")
	log.Debugf("A : %v " , A)
	A = c.NewJI([]c.Intf{"abcd" , 567 , true})
	log.Debugf("A : %v " , A)
	A = c.NewJI(map[int]int { 45 : 56})
	log.Debugf("A : %v " , A)
	A = c.NewJI(map[c.Intf]c.Intf { 45 : 56 , "abcd":"efgh" , true:false})
	log.Debugf("A : %v " , A)

}

func Test_JiAdd(t *testing.T){
	var A,B,C *c.JI
	A = c.NewJI(3456)
	B = c.NewJI(1234)
	C = A.Add(B)
	log.Debugf("A:%v , B:%v , C:%v " , A,B,C)
	A = c.NewJI(45.908)
	B = c.NewJI(13.6798)
	C = A.Add(B)
	log.Debugf("A:%v , B:%v , C:%v " , A,B,C)
	A = c.NewJI("This is first string ")
	B = c.NewJI("This is second string ")
	C = A.Add(B)
	log.Debugf("A:%v , B:%v , C:%v " , A,B,C)
	A = c.NewJI([]int{23 , 34 , 45})
	B = c.NewJI([]int{45 , 67 , 12})
	C = A.Add(B)
	log.Debugf("A:%v , B:%v , C:%v " , A,B,C)
	A = c.NewJI(map[float64]int{34:45 , 12:23})
	B = c.NewJI(map[float64]int{34:45 , 12:23})
	C = A.Add(B)
	log.Debugf("A:%v " , A)
	log.Debugf("B:%v " , B)
	log.Debugf("C:%v " , C)
}

func Test_IsEqual(t *testing.T){
	var A,B *c.JI
	A = c.NewJI(3456)
	B = c.NewJI(3456)
	if A.IsEqualVal(B) {
		log.Debugf("Int Values are equal")
	} else {
		t.Errorf("Failed, A:%v , B:%v " , A , B)
	}
	
	A = c.NewJI(34.789)
	B = c.NewJI(34.789)
	if A.IsEqualVal(B) {
		log.Debugf("Float Values are equal")
	} else {
		t.Errorf("Failed, A:%v , B:%v " , A , B)
	}

	A = c.NewJI("abcd")
	B = c.NewJI("abcd")
	if A.IsEqualVal(B) {
		log.Debugf("String Values are equal")
	} else {
		t.Errorf("Failed, A:%v , B:%v " , A , B)
	}

	A = c.NewJI([]string {"abc" , "def" , "ghi"})
	B = c.NewJI([]string {"abc" , "def" , "ghi"})
	if A.IsEqualVal(B) {
		log.Debugf("List Values are equal")
	} else {
		t.Errorf("Failed, A:%v , B:%v " , A , B)
	}

	A = c.NewJI(map [float64] string {4.5 :"xyz" , 145.467:"pqr"})
	B = c.NewJI(map [float64] string {4.5 :"xyz" , 145.467:"pqr"})
	if A.IsEqualVal(B) {
		log.Debugf("Map Values are equal")
	} else {
		t.Errorf("Failed, A:%v , B:%v " , A , B)
	}


	A = c.NewJI(3456)
	B = c.NewJI(-1234)
	if !A.IsEqualVal(B) {
		log.Debugf("Int Values are not equal")
	} else {
		t.Errorf("Failed, A:%v , B:%v " , A , B)
	}
	
	A = c.NewJI(34.789)
	B = c.NewJI(0)
	if  ! A.IsEqualVal(B) {
		log.Debugf("Float Values are not equal")
	} else {
		t.Errorf("Failed, A:%v , B:%v " , A , B)
	}

	A = c.NewJI("abcd")
	B = c.NewJI("pqrs")
	if ! A.IsEqualVal(B) {
		log.Debugf("String Values are not equal")
	} else {
		t.Errorf("Failed, A:%v , B:%v " , A , B)
	}

	A = c.NewJI([]string {"abc" , "def" , "ghi"})
	B = c.NewJI([]string {"abc" , "def" })
	if ! A.IsEqualVal(B) {
		log.Debugf("List Values are not equal")
	} else {
		t.Errorf("Failed, A:%v , B:%v " , A , B)
	}

	A = c.NewJI(map [float64] string {4.5 :"xyz" , 145.467:"pqr"})
	B = c.NewJI(map [float64] string {4.5 :"xyz" , 13.098:"pqr"})
	if  !A.IsEqualVal(B) {
		log.Debugf("Map Values are not equal")
	} else {
		t.Errorf("Failed, A:%v , B:%v " , A , B)
	}

}

func Test_JiSub(t *testing.T){
	var A,B,C,D *c.JI
	A = c.NewJI(3456)
	B = c.NewJI(3456)
	C = A.Sub(B)
	D = c.NewJI(0)
	if C.IsEqualVal(D) {
		log.Debugf("Int Sub validated")
	} else {
		t.Errorf("Failed, A:%v , B:%v , C:%v , D:%v " , A , B, C , D)
	}


	// If we add more decimal, subtraction gives little diffrent results being a float.
	A = c.NewJI(12.34)
	B = c.NewJI(10.0)
	C = A.Sub(B)
	D = c.NewJI(2.34)
	if C.IsEqualVal(D) {
		log.Debugf("Float Sub validated")
	} else {
		t.Errorf("Failed, A:%v , B:%v , C:%v , D:%v " , A , B, C , D)
	}
	
	A = c.NewJI([]int {2,3,4,5})
	B = c.NewJI([]int {12,13,14,15})
	C = A.Sub(B)
	D = c.NewJI([]int {-10,-10,-10,-10})
	if C.IsEqualVal(D) {
		log.Debugf("List Sub validated")
	} else {
		t.Errorf("Failed, A:%v , B:%v , C:%v , D:%v " , A , B, C , D)
	}
	
	A = c.NewJI( map[float32]int {4.2:2, 4.3:3, 4.4:4, 4.5:5})
	B = c.NewJI(map[float32]int {4.2:12, 4.3:13, 4.4:14, 4.5:15})
	C = A.Sub(B)
	D = c.NewJI(map[float32]int {4.2:-10, 4.3:-10, 4.4:-10, 4.5:-10})
	if C.IsEqualVal(D) {
		log.Debugf("List Sub validated")
	} else {
		t.Errorf("Failed, A:%v , B:%v , C:%v , D:%v " , A , B, C , D)
	}


}

