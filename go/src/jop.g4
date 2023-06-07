grammar jop;


/*
 * Parser Rules
 */
all     : code* EOF;
code	: (CMT|DIGITS) ;

/*
 * Lexer Rules
 */
DIGITS  			: [0-9]+;
CMT 				: '//' ;
OTHERS				: [ \n\t\r]+ -> skip;
ANY     			: .+?;
