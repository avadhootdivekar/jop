grammar jop;


/*
 * Parser Rules
 */
all     : code* EOF;
code	: (CMT|DIGITS|ANY) ;

/*
 * Lexer Rules
 */
DIGITS  			: [0-9]+;
CMT 				: '//' ;
OTHERS				: [ \n\t\r]+ -> skip;
ANY     			: .+?;
