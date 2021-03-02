from lark import Lark

parser= Lark(r"""
	//start symbol
    query: create | drop  | delete | update | select | insert

	// insert stmt
    insert: "INSERT INTO "i NAME ["(" name_expr ")"] "VALUES"i "(" insert_expr ")" -> insert
    insert_expr: literal[comma insert_expr] -> insert_expression
    name_expr: NAME [ comma name_expr] -> column_expression
    
    // create stmt
    create: "create table"i NAME "("expr ")"-> create
    
    expr: primary_expr  -> only_primary
    | primary_expr comma non_primary_expr  -> primary_beg 
    | non_primary_expr comma primary_expr comma non_primary_expr  -> primary_mid
    | non_primary_expr comma primary_expr -> primary_end


    primary_expr: NAME dtype "PRIMARY KEY"i -> pri

    non_primary_expr: NAME dtype [constraints] [comma non_primary_expr] -> non_primary

    dtype: "int"i -> int
    | "char"i
    | "date"i



    constraints: "not null"i
    | "unique"i -> unique
    | "foreign key"i

    
    // drop stmt
    drop: "drop table"i NAME -> drop_clause


    // update stmt
    update: "UPDATE"i NAME "SET"i update_ex ["WHERE"i where_ex] 
    update_ex: NAME "=" literal [comma update_ex ]

    
    // delete stmt
    delete: "DELETE FROM"i NAME ["WHERE"i where_ex] -> delete_stmt

    // select stmt
    select: "SELECT"i [select_mode] select_expr "FROM"i from_expr [join NAME "ON"i boolean_expr ] ["WHERE"i where_ex] ["GROUP BY"i grp_expr ] ["HAVING"i boolean_expr] ["ORDER BY"i ord_expr] ["LIMIT"i limit_expr]
    limit_expr: [NUMBER ["OFFSET"i NUMBER] ] | "ALL"i
    select_expr: "*" | NAME".*" | NAME"."NAME | NAME | select_expr comma select_expr
    grp_expr: NAME"."NAME | NAME | grp_expr comma grp_expr
    ord_expr: NAME"."NAME ["ASC"i|"DESC"i] | NAME ["ASC"i|"DESC"i] | ord_expr comma ord_expr
    select_mode: "DISTINCT"i | "ALL"i 
    from_expr: NAME[comma from_expr] -> from_expression
    | "(" select ")" ["as"i NAME ] -> nested_query
    join: "LEFT JOIN"i
    |"INNER JOIN"i
    |"RIGHT JOIN"i


	
	// common stmt ( where, operator, expression, literal)
    where_ex: boolean_expr
    boolean_expr: paren_expr
    | boolean_expr "OR"i boolean_expr -> or_oper
    | boolean_expr "AND"i  boolean_expr -> and_oper

    paren_expr: operator
    | "(" boolean_expr "AND"i operator ")" -> and_oper
    |  "(" boolean_expr "OR"i operator ")" -> or_oper

    operator: equal| notequal| greater| greater_equal| less| less_equal| between

    equal: expression "=" expression -> equal
    notequal: expression "<>" expression ->not_equal
    greater: expression ">" expression ->greater_than
    greater_equal: expression ">=" expression -> greater_than_equal
    less: expression "<" expression ->less_than
    less_equal: expression "<=" expression -> less_than_equal
    between: expression "BETWEEN"i expression "AND"i expression ->between

    expression: [NAME"."](NAME|"*") ->attribute_name
    | literal
    
    
    literal : "true" ->true
    | "false" -> false
    | NUMBER -> number
    | NAME ->  string
    | "\"" /[a-zA-Z0-9_'-' ]+/"\"" -> single_quoted_string
    | "'" /[a-zA-Z0-9_'-' ]+/"'" -> double_quoted_string

   
    comma: "," -> comma
	
      

%import common.CNAME -> NAME
%import common.NUMBER -> NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
%import common.WS
%ignore WS
""",start='query')


try:
    text = ""
    with open("input.txt","r") as f:
        for i in f.readlines():
            text += i
    print(text)
    print(parser.parse(text).pretty())
except Exception as e: 
    print(e)
    print("Incorrect Syntax")
