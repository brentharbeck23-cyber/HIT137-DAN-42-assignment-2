import os

# ==========================================================
# TOKENIZER
# turns a string into a list
# ==========================================================
def tokenize_expression(text):
    tokens = []
    cursor = 0

    while cursor < len(text):
        char = text[cursor]

        #handle whitespace
        if char.isspace():
            cursor += 1
            continue

        #handles numbers (including decimals)
        if char.isdigit() or char == '.':
            number_str = ""
            while cursor < len(text) and (text[cursor].isdigit() or text[cursor] == '.'):
                number_str += text[cursor]
                cursor += 1
            tokens.append(("NUM", number_str))
            continue

        # handles oporators and parentheses
        if char in "+-*/":
            tokens.append(("OP", char))
        elif char == "(":
            tokens.append(("LPAREN", char))
        elif char == ")":
            tokens.append(("RPAREN", char))
        else:
            return None

        cursor += 1

    tokens.append(("END", ""))
    return tokens


# ==========================================================
# IMPLICIT MULTIPLICATION
# ==========================================================
def add_implicit_multiplication(tokens):
    new_tokens = []

    for i in range(len(tokens) - 1):
        t1 = tokens[i]
        t2 = tokens[i + 1]

        new_tokens.append(t1)

        if (
            (t1[0] == "NUM" and t2[0] == "LPAREN") or
            (t1[0] == "RPAREN" and t2[0] == "NUM") or
            (t1[0] == "RPAREN" and t2[0] == "LPAREN")
        ):
            new_tokens.append(("OP", "*"))

    new_tokens.append(tokens[-1])
    return new_tokens


# ==========================================================
# PARSER (NO CLASSES)
# takes the list of tokens and creates the 'tree'
# follows rules of BIMDAS
# ==========================================================
def parse(tokens):
    index = 0

    def peek():
        return tokens[index]

    def consume():
        nonlocal index
        t = tokens[index]
        index += 1
        return t

    def expression():
        node, val = term()

        while peek()[0] == "OP" and peek()[1] in "+-":
            op = consume()[1]
            right_node, right_val = term()

            if op == "+":
                val += right_val
            else:
                val -= right_val

            node = f"({op} {node} {right_node})"

        return node, val

    def term():
        node, val = factor()

        while peek()[0] == "OP" and peek()[1] in "*/":
            op = consume()[1]
            right_node, right_val = factor()

            if op == "*":
                val *= right_val
            else:
                if right_val == 0:
                    raise Exception()
                val /= right_val

            node = f"({op} {node} {right_node})"

        return node, val

    def factor():
        if peek()[0] == "OP" and peek()[1] == "-":
            consume()
            node, val = factor()
            return f"(neg {node})", -val

        if peek()[0] == "OP" and peek()[1] == "+":
            raise Exception()

        return primary()

    def primary():
        t = peek()

        if t[0] == "NUM":
            consume()
            return t[1], float(t[1])

        if t[0] == "LPAREN":
            consume()
            node, val = expression()

            if peek()[0] != "RPAREN":
                raise Exception()

            consume()
            return node, val

        raise Exception()

    tree, value = expression()

    if peek()[0] != "END":
        raise Exception()

    return tree, value


# ==========================================================
# TOKEN FORMAT
# ==========================================================
def format_tokens(tokens):
    return " ".join(f"[{t[0]}:{t[1]}]" for t in tokens)


# ==========================================================
# MAIN REQUIRED FUNCTION
# DEFINE OUTPUT PATH
# ==========================================================
def evaluate_file(input_path: str) -> list[dict]:
    results = []

    output_path = os.path.join(os.path.dirname(input_path), "output.txt")

    with open(input_path, "r") as f:
        lines = f.readlines()

    with open(output_path, "w") as out:
        for line in lines:
            expr = line.rstrip("\n")

            if expr.strip() == "":
                continue

            try:
                tokens = tokenize_expression(expr)
                if tokens is None:
                    raise Exception()

                tokens = add_implicit_multiplication(tokens)

                tree, value = parse(tokens)

                # format result
                if value.is_integer():
                    result_str = str(int(value))
                else:
                    result_str = str(round(value, 4))

                token_str = format_tokens(tokens)

                result = {
                    "input": expr,
                    "tree": tree,
                    "tokens": token_str,
                    "result": value
                }

            except:
                result = {
                    "input": expr,
                    "tree": "ERROR",
                    "tokens": "ERROR",
                    "result": "ERROR"
                }

            results.append(result)

            out.write(f"Input: {result['input']}\n")
            out.write(f"Tree: {result['tree']}\n")
            out.write(f"Tokens: {result['tokens']}\n")
            out.write(f"Result: {result['result']}\n\n")

    return results

# ================================================
# APPLY EVALUATOR FUNCTION TO INPUT FILE RESULTING IN OUTPUT FILE 
## EDIT FILE STRING "input.txt" IF NEEDED FOR DIFFERENT INPUT FILE NAME
# ================================================

if __name__ == "__main__":
    evaluate_file("input.txt")      
    

