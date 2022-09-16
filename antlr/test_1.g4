grammar test_1;

/*
 * Parser Rules
 */
almostAll				: .*?lines.*?EOF ;
//text1			:  (rule1 | var)*EOF ;
//rule1			:  rule1 OTHERS | rule1 var | rule1 string | string ;
//string			: ('"'(LETTERS)*'"')+ ;
lines				: lines strings | lines rule1 | strings | rule1 ;
strings				: '"'(OTHERS | rule1)+'"' ;
rule1				: var ;
var					: var LETTERS
					| var NUMBERS
					| LETTERS 
					| LETTERS NUMBERS 
					;



/*
 * Lexer Rules
 */

/*
	This is test 1 for ANTLR 4 grammar.
*/

T1 					: [a-z] ;
T2 					: [A-Z] ;
LETTERS				: (T1|T2)+ ;
NUMBERS				: [0-9]+ ;
OTHERS				: [ \n\t\r]+ ;
FLT					: NUMBERS '.' NUMBERS | NUMBERS;
STR					: '"' ('\\"' | . )*? '"'; 
// STRING			: ".*?(?!\\\")."     <-- This is regex for string for reference
//QUOTE				: '"';


