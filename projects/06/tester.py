import re
s = "Example String"
lines = ["fhbf", "   hufhrui   jjrf\t  \n"]
lines = ["".join(lin.split()) for lin in lines if "".join(lin.split())]
print(lines)