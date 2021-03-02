from lark import Lark

parser = Lark(r"""

	?query: /select/i /(\s)+/ [[/Distinct/i | /All/i] /(\s)+/ ] selection_expression /(\s)+/ from_clause -> select
		| delete
		| ("Distinct"|"ALL"|"null")attribute -> testing_ke_liye 
		
	?attribute: /[a-zA-Z0-9]+/ -> att
	
	?from_clause: /from/i table_expression -> from_clause
	
	?table_expression: (NAME | "("query")" /(\s)+/ /as/i /(\s)+/ NAME | "("query")" /(\s)+/ NAME ) -> table_expression
	
	?selection_expression: ("*" | NAME["."NAME | ".*" ])[comma selection_expression | comma /(\s)+/ selection_expression ]  -> name
		
	?where_expression: NAME"."attribute"=" attribute
	
	?delete: "DELETE"/(\s)+/"FROM"/(\s)+/ NAME -> delete_query 
	
    ?comma: ","				-> comma
	

%import common.CNAME -> NAME
%import common.NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
	""",start='query')
	
try:
	with open("input.txt","r") as f:
		text = f.read()
	print(parser.parse(text).pretty())
except Exception as e: 
	print(e)
	print("Incorrect Syntax")
	
#print(parser.parse(text).pretty())
         
