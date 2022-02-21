def parse_regex(regex):
    return parse_regex_rec(None, None, regex)

# first_regex -> operandul din stanga al operatiei in forma prenex, la final va
# reprezenta forma prenex a regex-ului
# operator -> operatorul dintre primul si al doilea operand regex
# regex -> restul regex-ului ce are operandul din dreapta alaturi de alti
# operanzi si operatori
def parse_regex_rec(first_regex, operator, regex):
    if regex == "":
        return first_regex

    regex_len = len(regex)
    for i in range(regex_len):
        ch = regex[i]
        if ch == " ":
            continue
        elif ch == "|":
            return parse_regex_rec(first_regex, "|", regex[i+1:regex_len])
        elif ch not in "*+":
            curr_regex = ch

            # procesez caracterele ASCII non-alfanumerice
            if ch == "'":
                i += 1
                ascii_ch = "'"
                while regex[i] != "'":
                    ascii_ch += regex[i]
                    i += 1

                curr_regex = ascii_ch + "'"

            # parsez regex-ul dintre paranteze, va merge recursiv
            # in jos daca exista niveluri inferioare de paranteze
            if ch == "(":
                i += 1
                parantheses_regex = ""

                # stiva o folosesc pentru a numara parantezele ca sa
                # diferentiez intre perechea lui "(" si alte paranteze ")"
                # interioare de pe niveluri inferioare
                stack = ["("]
                while len(stack) > 0:
                    if regex[i] == "(":
                        stack.append("(")
                    elif regex[i] == ")":
                        stack.pop()

                    parantheses_regex += regex[i]
                    i += 1

                curr_regex = parse_regex(parantheses_regex[0:-1])
                i -= 1

            # daca regex-ul are */+ la final, atunci adaug plus-ul
            # si star-ul la forma prenex
            i += 1
            if i != regex_len:
                if regex[i] == "*":
                    curr_regex = "STAR  " + curr_regex
                    i += 1
                elif regex[i] == "+":
                    curr_regex = "PLUS  " + curr_regex
                    i += 1

            # daca nu e vreun prim operand, atunci regex-ul curent
            # va fi primul operand pentru operatia curenta
            # altfel, va fi al doilea operand si in functie de operator
            # adaug la forma prenex
            rest_of_regex = regex[i:regex_len]
            if first_regex == None:
                first_regex = curr_regex
            else:
                if operator == None:
                    first_regex = "CONCAT  " + first_regex + "  " + curr_regex
                elif operator == "|":
                    first_regex = "UNION  " + first_regex + "  " + curr_regex

            return parse_regex_rec(first_regex, operator, rest_of_regex)
