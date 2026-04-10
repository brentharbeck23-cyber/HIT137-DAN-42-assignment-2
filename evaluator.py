
import os

# ==========================================================
# STEP 1: THE TOKENIZER
# This turns a string like "3 + 4" into a list: [NUM:3, OP:+, NUM:4]
# ==========================================================
def tokenize_expression(text):
    tokens = []
    cursor = 0

    while cursor < len(text):
        char = text[cursor]

        # Handle whitespace
        if char.isspace():
            cursor += 1
            continue

        # Handle numbers (including decimals)
        if char.isdigit() or char == '.':
            number_str = ""
            while cursor < len(text) and (text[cursor].isdigit() or text[cursor] == '.'):
                number_str += text[cursor]
                cursor += 1
            tokens.append(("NUM", float(number_str)))
            continue 

        # Handle operators and parentheses
        if char in "+-*/":
            tokens.append(("OP", char))
        elif char == "(":
            tokens.append(("LPAREN", char))
        elif char == ")":
            tokens.append(("RPAREN", char))
        else:
            raise ValueError(f"Unknown character found: {char}")

        cursor += 1

    tokens.append(("END", "EOF"))
    return tokens


# ==========================================================
# STEP 2: THE PARSER
# This takes the flat list of tokens and builds a "Tree" 
# that follows the rules of BODMAS/PEMDAS.
# ==========================================================
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def parse(self):
        """Entry point for building the tree."""
        return self.expression()

    def expression(self):
        """Handles Addition and Subtraction (Lowest priority)"""
        node = self.term()
        while self.current_token()[1] in ("+", "-"):
            operator = self.current_token()[1]
            self.advance()
            right_side = self.term()
            node = (operator, node, right_side)
        return node

    def term(self):
        """Handles Multiplication and Division"""
        node = self.factor()
        while self.current_token()[1] in ("*", "/"):
            operator = self.current_token()[1]
            self.advance()
            right_side = self.factor()
            node = (operator, node, right_side)
        return node

    def factor(self):
        """Handles Numbers, Negative signs, and Parentheses (Highest priority)"""
        token_type, value = self.current_token()

        # Handle negative numbers (e.g., -5)
        if token_type == "OP" and value == "-":
            self.advance()
            return ("neg", self.factor())

        # Handle raw numbers
        if token_type == "NUM":
            self.advance()
            return value

        # Handle nested math inside ( )
        if token_type == "LPAREN":
            self.advance()
            node = self.expression()
            if self.current_token()[0] != "RPAREN":
                raise ValueError("Missing matching closing parenthesis")
            self.advance()
            return node

        raise ValueError("Unexpected math syntax")


# ==========================================================
# STEP 3: TOOLS (Formatting and Solving)
# ==========================================================

def get_tree_string(node):
    """Converts the tree tuple into a readable string format."""
    if isinstance(node, float):
        # Return as int if it ends in .0, otherwise keep as float
        return str(int(node)) if node.is_integer() else str(node)
    
    if node[0] == "neg":
        return f"(neg {get_tree_string(node[1])})"
    
    op, left, right = node
    return f"({op} {get_tree_string(left)} {get_tree_string(right)})"


def calculate(node):
    """Recursively walks through the tree to find the final math answer."""
    if isinstance(node, float):
        return node

    if node[0] == "neg":
        return -calculate(node[1])

    op, left, right = node
    left_val = calculate(left)
    right_val = calculate(right)

    if op == "+": return left_val + right_val
    if op == "-": return left_val - right_val
    if op == "*": return left_val * right_val
    if op == "/": return left_val / right_val


# ==========================================================
# STEP 4: MAIN CONTROLLER
# ==========================================================

def process_math_file(filename):
    """Reads a file, solves equations, and saves to output.txt"""
    output_filename = os.path.join(os.path.dirname(filename), "output.txt")
    summary_results = []

    try:
        with open(filename, "r") as f_in, open(output_filename, "w") as f_out:
            for line in f_in:
                equation = line.strip()
                if not equation: continue

                try:
                    # Run the pipeline
                    tokens = tokenize_expression(equation)
                    parser = Parser(tokens)
                    tree = parser.parse()
                    answer = calculate(tree)

                    # Prepare strings for display
                    tree_display = get_tree_string(tree)
                    token_display = " ".join([f"[{t[0]}:{t[1]}]" if t[0] != "END" else "[END]" for t in tokens])
                    answer_display = f"{answer:.4f}".rstrip('0').rstrip('.') if not answer.is_integer() else str(int(answer))

                except Exception as e:
                    tree_display = token_display = answer_display = "ERROR"
                    answer = "ERROR"

                # Write to file
                f_out.write(f"Input:   {equation}\n")
                f_out.write(f"Tree:    {tree_display}\n")
                f_out.write(f"Tokens:  {token_display}\n")
                f_out.write(f"Result:  {answer_display}\n\n")

                summary_results.append({
                    "input": equation,
                    "tree": tree_display,
                    "tokens": token_display,
                    "result": answer
                })

    except FileNotFoundError:
        print(f"Error: Could not find file {filename}")
        
    return summary_results