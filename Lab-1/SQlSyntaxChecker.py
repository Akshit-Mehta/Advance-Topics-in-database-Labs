from lark import Lark

parser= Lark(r"""
    query: create | drop  | delete | update | select | insert

    insert: "INSERT INTO "i space NAME space ["(" insert_expr ")"] space "VALUES"i space "(" insert_expr ")"
    insert_expr: literal[space comma space insert_expr] -> insert_expression
    
    create: "create table"i space NAME space "("space expr space")"space -> create
    
    expr: pri_expr  -> only_pri
    | pri_expr space comma space non_pri_expr  -> pri_beg 
    | non_pri_expr space comma space pri_expr space comma space non_pri_expr  -> pri_mid
    | non_pri_expr space comma space pri_expr -> pri_end
    | non_pri_expr -> no_pri

    pri_expr: NAME space dtype space "PRIMARY KEY"i -> pri

    non_pri_expr: NAME space dtype space constraints -> non_pri

    dtype: "int"i -> int
    | "char"i
    | "date"i

    constraints: "not null"i
    | "unique"i -> unique
    | "foreign key"i

    
    
    drop: "drop table"i NAME space -> drop_clause


        
    update: "UPDATE"i space NAME space "SET"i space update_ex space ["WHERE"i space where_ex] space
    update_ex: NAME space "=" space literal space [comma space update_ex space]

    
    
    delete: "DELETE FROM"i space NAME space ["WHERE"i space where_ex] space

    
    select: "SELECT"i space [select_mode] space select_expr space "FROM"i space from_expr space [join space NAME space "ON"i space boolean_expr ] space ["WHERE"i space where_ex] space ["GROUP BY"i space grp_expr space] space ["HAVING"i space boolean_expr] space ["ORDER BY"i space ord_expr] space ["LIMIT"i space limit_expr]
    limit_expr: [NUMBER space ["OFFSET"i space NUMBER] space] | "ALL"i
    select_expr: "*" | NAME".*" | NAME"."NAME | NAME | select_expr space comma space select_expr
    grp_expr: NAME"."NAME | NAME | grp_expr space comma space grp_expr
    ord_expr: NAME"."NAME ["ASC"i|"DESC"i] | NAME ["ASC"i|"DESC"i] | ord_expr space comma space ord_expr
    select_mode: "DISTINCT"i
    | "ALL"i 
    from_expr: NAME -> from_expression
    | "(" space select space ")" ["as"i space NAME space] -> nested_query
    join: "LEFT JOIN"i
    |"INNER JOIN"i
    |"RIGHT JOIN"i



    where_ex: boolean_expr
    boolean_expr: paren_expr
    | space boolean_expr space "OR"i space boolean_expr space -> or_oper
    | space boolean_expr space "AND"i space  boolean_expr space -> and_oper

    paren_expr: operator
    | space"(" space boolean_expr "AND"i operator space ")" space -> and_oper
    |  space"(" space boolean_expr "OR"i operator space ")" space-> or_oper

    operator: equal| notequal| greater| greater_equal| less| less_equal| between

    equal: space expression space "=" space expression space -> equal
    notequal: space expression space "<>" space expression space ->not_equal
    greater: space expression space ">" space expression space ->greater_than
    greater_equal: space expression space ">=" space expression space -> greater_than_equal
    less: space expression space "<" space expression space ->less_than
    less_equal: space expression space "<=" space expression space -> less_than_equal
    between: space expression space "BETWEEN"i space expression space "AND"i space expression ->between

    expression: [NAME"."](NAME|"*") ->attribute_name
    | literal
    literal : "true" ->true
    | "false" -> false
    | NUMBER ->number
    | NAME ->string
    | "'"literal[space literal]"'" -> quoted_string

    

    comma: "," -> comma
    space: [/(\s)+/] -> space
      

%import common.CNAME -> NAME
%import common.NUMBER -> NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
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
