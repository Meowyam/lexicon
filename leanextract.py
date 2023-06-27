import sys
import re
import itertools

x = sys.argv[1]
keywords = []
cats = []
f = open(x,"r")
lines = f.readlines()

def combineIS(arr):
  i = 0
    while i < len(arr) - 1:
      if arr[i] == "IS" and arr[i+1].isupper():
          fixed_arr = arr[i] + " " + arr[i + 1]
          arr[i] = fixed_arr
          del arr[i + 1]
        else:
          i += 1

    return arr

for l in lines:
    words = l.split()
    # words = combineIS(wordarr)

    for w in words:
        if w.isupper():
          print(w)
          keywords.append((re.sub(r'[()\[\],]', '',  w)))
        elif re.match(r'^[A-Z][a-zA-Z]*$', w):
          cats.append(w)

    print(lines)
    print("---")
    # print(list(set(keywords)))
    # print(list(set(cats)))

with open("LeanSyntax.gf", 'w') as abs:
    abs.write('abstract LeanSyntax = {\n\ncat = \n')

    for cat in sorted(list(set(cats))):
      abs.write('  ' + cat + '; \n')

    abs.write('\nfun = \n')

    for fun in sorted(list(set(keywords))):
      abs.write('  ' + fun + '; \n')

    abs.write('\n\n}')

