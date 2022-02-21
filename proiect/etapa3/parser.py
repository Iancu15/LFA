from ast import *

def parse_lexems(lexem_token_pairs):
    expr_enders = ["NEWLINE", "DO", "THEN"]
    lexem_token_pairs_len = len(lexem_token_pairs)

    def token_of_index(index):
        (token, _) = lexem_token_pairs[index]
        return token

    def assert_token(index, token_cmp):
        token = token_of_index(index)
        assert token == token_cmp

    def assert_token_list(index, token_cmp_list):
        token = token_of_index(index)
        assert token in token_cmp_list

    def ignore_indentation(index):
        index_after_indentation = index
        token = token_of_index(index_after_indentation)
        while token == "INDENTATION":
            index_after_indentation += 1
            token = token_of_index(index_after_indentation)

        return index_after_indentation

    def ignore_newline(index):
        if token_of_index(index) == "NEWLINE":
            return index + 1

        return index

    # creez recursiv expresia printr-o recursivitate in coada in care
    # salvez in left_expr expresia cumulata
    def parse_expr_rec(height, index, left_expr, operator):
        (token, lexem) = lexem_token_pairs[index]
        if token in expr_enders:
            return left_expr

        if token == "OPERATOR":
            assert left_expr != None
            operator_type = lexem.replace(" ", "")
            return parse_expr_rec(height, index + 1, left_expr, operator_type)

        type = None
        if token == "VARIABLE":
            type = 'v'
        elif token == "INTEGER":
            type = 'i'
        else:
            return None

        # se intra aici doar la inceput
        if left_expr == None:
            expr = Expr(height, type, lexem)
            return parse_expr_rec(height, index + 1, expr, None)

        # adauga noua expresia la expresia deja construita
        assert operator != None
        right_expr = Expr(height, type, lexem)
        expr = Expr(height - 1, operator, left_expr, right_expr)
        return parse_expr_rec(height - 1, index + 1, expr, None)

    def parse_expr(height, index):
        index = ignore_indentation(index)
        number_of_operations = 0

        # calculez numarul de operatori pentru a stii inaltimea maxima
        # asta pentru ca expresiile de la inceput o sa aiba inaltimile cele
        # mai mari si ultimul operator ar trebui sa aiba inaltimea height
        # primita ca parametru
        for i in range(index, lexem_token_pairs_len):
            token = token_of_index(i)
            if token == "OPERATOR":
                number_of_operations += 1

            if token in expr_enders:
                break

        return (i, parse_expr_rec(height + number_of_operations, index, None, None))

    # cat timp nu s-a ajuns la final(la "END") construiesc lista de instructiuni
    def parse_instruction_list(height, index):
        index = ignore_indentation(index)
        instruction_list = []
        curr_token = token_of_index(index)
        curr_index = index
        while curr_token != "END":
            (next_index_prog, prog) = parse_prog(height + 1, curr_index)
            instruction_list.append(prog)
            curr_index = ignore_indentation(next_index_prog)
            curr_token = token_of_index(curr_index)

        return (curr_index, InstructionList(height, instruction_list))

    # parseaza programul in functie de ce tip este si il constuieste folosind
    # functiile parse_expr, parse_instruction_list sau chiar parse_prog la
    # nevoie
    def parse_prog(height, index):
        index = ignore_indentation(index)
        (token, lexem) = lexem_token_pairs[index]
        if token == "VARIABLE":
            var = Expr(height + 1, 'v', lexem)
            assert_token(index + 1, "ASSIGN")
            (next_index_expr, expr) = parse_expr(height + 1, index + 2)
            assert_token(next_index_expr, "NEWLINE")
            return (next_index_expr + 1, Assign(height, var, expr))
        elif token == "BEGIN":
            (next_index_instr_lst, instr_list) = parse_instruction_list(height, index + 1)
            next_index_instr_lst = ignore_indentation(next_index_instr_lst)
            assert_token(next_index_instr_lst, "END")
            return (next_index_instr_lst + 1, instr_list)
        elif token == "WHILE":
            (next_index_expr, expr) = parse_expr(height + 1, index + 1)
            assert_token(next_index_expr, "DO")
            (next_index_prog, prog) = parse_prog(height + 1, next_index_expr + 1)
            next_index_prog = ignore_indentation(next_index_prog)
            assert_token(next_index_prog, "OD")
            return (next_index_prog + 1, While(height, expr, prog))
        elif token == "IF":
            (next_index_expr, expr) = parse_expr(height + 1, index + 1)
            assert_token(next_index_expr, "THEN")
            (next_index_prog_then, prog_then) = parse_prog(height + 1, next_index_expr + 1)
            next_index_prog_then = ignore_indentation(next_index_prog_then)
            assert_token(next_index_prog_then, "ELSE")
            (next_index_prog_else, prog_else) = parse_prog(height + 1, next_index_prog_then + 1)
            next_index_prog_else = ignore_indentation(next_index_prog_else)
            assert_token(next_index_prog_else, "FI")
            return (next_index_prog_else + 1, If(height, expr, prog_then, prog_else))

        return None

    (_, prog) = parse_prog(0, 0)
    return prog
