grammar jop;


/*
 * Parser Rules
 */
all     : code* EOF;
code	: (lines|block)+ ;
lines   : ( assign | CMT )+ ;
block   : ( OC lines + CC )  ;
assign  : ID EQ rvalue SEMIC;
rvalue 	: uid ;
uid 	: ( num | ID | BT | BF | string ) ;
string  : STR+;
num     : ( INT | FLT ) ;

/*
 * Lexer Rules
 */

fragment T1 					: [a-z_] ;
fragment T2 					: [A-Z] ;
fragment LETTERS				: (T1|T2)+ ;
fragment ESC		: '\\\\' | '\\"' ;

CMT					: '//'.*?  '\n' ;
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
SEMIC				: ';' ;
EXP					: '^' ;
DLR					: '$' ;
PERC				: '%' ;
AMP					: '&' ; 
OR					: '|';
BACKSLASH			: '\\';
EXCL				: '!' ;
AsT					: '@' ;
BT					: 'true'	;			// Boolean true
BF					: 'false'	;			// Boolean false
INT					: [0-9]+ ;
FLT					: INT '.' INT ;
JOP					: 'jop';
INT_KEY				: '_key' ;
INT_VALUE			: '_val' ;
SYS_DEF				: '_';					// System defined internal macros/functions.
OTHERS				: [ \n\t\r]+ -> skip;
STR					: '"' (ESC | . )*? '"' ;  
ID					: LETTERS  (LETTERS | INT)* ;

MCMT				: '/*' .*? '*/' ;




// Skip to any.
ANY     			: .+?;