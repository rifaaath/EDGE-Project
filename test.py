import os
from analysis import analyze_code

code = '''a = [1,2,3]
b = [4,5,6]
c = a + b
'''
source = 'python'
dest = 'javascript'

result = analyze_code(code, source, dest)
print(result)
