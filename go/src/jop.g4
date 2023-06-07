grammar jop;


/*
 * Parser Rules
 */

code	: CMT*EOF ;

/*
 * Lexer Rules
 */
CMT 	: '//' ;
