def __sub_comments(self, beg: str, end: str) -> str:
    """Removes comments from beg to end"""
    # input_lines = self.__input_lines
    # instr = False
    # arr = []
    # for i in range(len(input_lines)-1):
    #     if input_lines[i] == '"':
    #         instr = not instr
    #     elif not instr and input_lines[i] == beg[0] and input_lines[i+1] == beg[1]:
    #         j = i + input_lines[input_lines.find(beg):].find(end) + len(end)
    #         arr.append((i, j))
    # for i in range(len(arr) - 1, -1, -1):
    #     input_lines = input_lines[:arr[i][0]] + input_lines[arr[i][1]:]
    # return input_lines

    input_lines = self.__input_lines
    final = ""
    instr = False
    in_comment = False
    for i in range(len(input_lines) - 1):
        # if in_comment and input_lines[i] == end[0] and (len(end) == 1 or input_lines[i + 1] == end[1]):
        if in_comment and (len(end) == 1 and input_lines[i] == end[0]) or (
                len(end) == 2 and input_lines[i] == end[0] and input_lines[i + 1] == end[1]):
            in_comment = False
        elif in_comment:
            continue
        elif input_lines[i] == '"':
            final += '"'
            instr = not instr
        elif instr:
            final += input_lines[i]
        elif input_lines[i] == beg[0] and input_lines[i + 1] == beg[1]:
            in_comment = True
        else:
            final += input_lines[i]

    return final


def __sub_comments2(self, beg: str, end: str) -> str:
    """Removes comments from beg to end"""

    input_lines = self.__input_lines
    final = ""
    instr = False
    in_comment = False
    for i in range(len(input_lines) - 1):
        if in_comment and input_lines[i] == "*" and input_lines[i + 1] == "/":
            in_comment = False
        elif in_comment:
            continue
        elif input_lines[i] == '"':
            final += '"'
            instr = not instr
        elif instr:
            final += input_lines[i]
        elif input_lines[i] == beg[0] and input_lines[i + 1] == beg[1]:
            in_comment = True
        else:
            final += input_lines[i]

    return final