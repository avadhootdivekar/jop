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
					| a ( '^' )+
					| ( '^' )+ a
					;
lines				: lines line+
					| line+
					;

assign				: (id_ | member)  eq  ( rvalue)  ;

line				: ( assign ';' 	)
					| ( rvalue  ';'	)
					| ( CMT			)
					;

strings				: STR ;

block				: '{' (lines | block )+ '}' ; 

rule1				: member ;


rvalue				: (uid | member | fcall | match_b | curly | list_ | expr) ;

member				: ( id_ (SEP|root) ((member_candidate ) ((SEP|root) member_candidate)* )			)
					| ( id_ all_depth						)
					;

member_candidate	: (uid | match_b | M );

/* uid are unique identifiers. These can be vars,numbers, strings or even function names without branckets etc. */ 
uid					: (num | id_ | bt | bf | strings) ;
id_					: ID ;
bt					: BT ;
bf 					: BF ;
fcall				: ID match_b;
match_b				: '(' (match_b | rvalue | getParent)* ')' ;
m_pool				: (member)+ ;
num					: (INT | FLT) ;
all_depth			: SEP SEP ;
statement			: (rvalue | fcall );
curly				: ( OC curly (',' curly)* CC 	)
					| ( OC pair (',' pair)* CC		) 
 					| ( OC curly (',' pair)* CC  	)
					| ( OC pair (',' curly)* CC  	)
					| (OC CC) ;

list_				: ( OS uid (',' uid|curly )* CS )
					| ( OS curly (',' curly|uid )* CS )
					| (OS CS)
					;

expr				: ( (expr_1)  b_op expr)
					| ( (expr_1) SEP b_op expr)
					| expr_1 ;

expr_1				: ( member | fcall | curly | match_b | uid);

b_op				: (dict_b_op | math_b_op);
math_b_op			: ( (SEP P) | (SEP N) | (SEP M) | (SEP D) );
dict_b_op			: (P | N ) ;
math_u_op			: (P P | N N ) ;
getParent			: SEP '<' ;
pair				: uid ':'  (uid | curly | list_ ) ;
regex				: SYS_DEF 're' strings ;
sys_fcall			: SYS_DEF fcall;
root				: ROOT;
eq					: EQ;

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
fragment ESC		: '\\\\' | '\\"' ;
J_LIT				: '"""' (ESC | . )*? '"""' ;
SEP					: '.' ; //stands for seperator.
EQ					: '=' ;
P					: '+' ; 
N					: '-' ;
M					: '*' ;
D					: '/' ;
ROOT				: './';
OB					: '(' ;
CB					: ')' ;
OC					: '{' ;
CC					: '}' ;
OS					: '[' ;
CS					: ']' ;
BT					: 'true'	;			// Boolean true
BF					: 'false'	;			// Boolean false
INT					: [0-9]+ ;
OTHERS				: [ \n\t\r]+ -> skip;
FLT					: INT '.' INT ;
SYS_DEF				: '_';					// System defined internal macros/functions.
STR					: '"' (ESC | . )*? '"' ; 
ID					: LETTERS  (LETTERS | INT)* ;
// ERR_ID				: INT (LETTERS | INT)* ;
EXP					: '^'; 
// STRING			: ".*?(?!\\\")."     <-- This is regex for string for reference
//QUOTE				: '"';
MCMT				: '/*' .*? '*/' ;


