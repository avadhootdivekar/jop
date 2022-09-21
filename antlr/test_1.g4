grammar test_1;

/*
 * Parser Rules
 */
code 				: (lines | block+)+  EOF;
// Children sequqnces should be greedy in the sense that parser starts from first line.
// Thus anything before and after "lines" would be matched and parsing will end. catch
// Tokens out of first "lines" would not be considered because of ".*"
//text1			:  (rule1 | var)*EOF ;
//rule1			:  rule1 OTHERS | rule1 var | rule1 string | string ;
//string			: ('"'(LETTERS)*'"')+ ;

a					: '^'
					| a ( '^' | OTHERS )+
					| ( '^' | OTHERS )+ a
					;
lines				: lines line+
					| line+
					;

assign				: ID OTHERS* EQ OTHERS* ( rvalue) OTHERS*;

line				: assign ';'
					|  OTHERS 
					| rvalue  ';'
					| CMT
					;

strings				: STR ;

block				: '{' (lines | block | OTHERS)+ '}' ; 

rule1				: member ;

rvalue				: (num | id_ | bt | bf | strings | member | fcall) ;

/*
var					: var ID
					| var NUMBERS
					| ID 
					| ID NUMBERS 
					;
*/
member				: ID SEP ( ID | num | BT | BF | strings)+
					| member SEP ( ID | num | BT | BF | strings)+
					| ID SEP member
					| ID emb_fcall
					| member emb_fcall
					;

emb_fcall			: SEP match_b ;
id_					: ID ;
bt					: BT ;
bf 					: BF ;
fcall				: ID match_b;
match_b				: '(' (match_b | rvalue|OTHERS)* ')' ;
m_pool				: (member)+ ;
num					: (INT | FLT) ;

statement			: (rvalue | fcall );


//almostAll				: .*?lines.*?EOF ;
/*
 * Lexer Rules
 */

/*
	This is test 1 for ANTLR 4 grammar.
*/

CMT					: '//'.*?'\n' 
					| '//'.*? EOF ;
fragment T1 					: [a-z_] ;
fragment T2 					: [A-Z] ;
fragment LETTERS				: (T1|T2)+ ;
SEP					: '.' ; //stands for seperator.
EQ					: '=' ;
P					: '+' ; 
N					: '-' ;
M					: '*' ;
D					: '/' ;
OB					: '(' ;
CB					: ')' ;
OC					: '{' ;
CC					: '}' ;
OS					: '[' ;
CS					: ']' ;
BT					: 'true'	;			// Boolean true
BF					: 'false'	;			// Boolean false
INT					: [0-9]+ ;
OTHERS				: [ \n\t\r]+ ;
FLT					: INT '.' INT ;
fragment ESC		: '\\\\' | '\\"' ;
STR					: '"' (ESC | . )*? '"' ; 
ID					: LETTERS  (LETTERS | INT)* ;
// ERR_ID				: INT (LETTERS | INT)* ;
EXP					: '^'; 
// STRING			: ".*?(?!\\\")."     <-- This is regex for string for reference
//QUOTE				: '"';


