import re
import json
rules = {}
printer = []
callStack = []
rules = {}

print("Enter the productions(Use @ for Epsilon):")

for i in input().split(' '):
    NT = ""
    rule = re.split('->|\|', i)
    length = len(rule)
    NonTerminal = {'RHS': [],
                   'first': [],
                   'follow': []}
    for index, j in enumerate(rule):
        if index == 0:
            NT = j
            continue
        NonTerminal['RHS'].append(j)
        if index == length-1:
            rules[NT] = NonTerminal

start = input("Enter the start symbol:")


def first(NT):
    f = []
    for i in rules[NT]['RHS']:
        if i[0].islower() or i[0].isnumeric():
            f.append(i[0])
        elif i[0] == '@':
            f.append("@")
        elif i[0].isupper():
            for j in first(i[0]):
                if j == '@':
                    count = 1
                    Break = True
                    while True:
                        try:
                            if i[count].islower() or i[count].isnumeric():
                                f.append(i[count])
                                break
                            for k in first(i[count]):
                                if(k == '@'):
                                    count += 1
                                    Break = False
                                    break
                                f.append(k)
                            if(Break):
                                break
                            Break = True
                        except:
                            f.append("@")
                            break
                else:
                    f.append(j)
    return f


def follow(NT):
    f = []
    if NT == start:
        f.append('$')
    for LHS in rules.keys():
        for j in rules[LHS]['RHS']:
            if NT in j:
                try:
                    index = j.find(NT)
                    if j[index+1].islower() or j[index+1].isnumeric():
                        f.append(j[index+1])
                    elif j[index+1].isupper():
                        for k in first(j[index+1]):
                            if k == "@":
                                count = 1
                                Break = True
                                while True:
                                    if j[index+1+count].islower() or j[index+1+count].isnumeric():
                                        f.append(j[index+1+count])
                                        break
                                    for ele in first(j[index+1+count]):
                                        if(k == '@'):
                                            count += 1
                                            Break = False
                                            break
                                        f.append(ele)
                                if(Break):
                                    break
                                Break = True
                            else:
                                f.append(k)
                except:
                    if not LHS in callStack:
                        callStack.append(LHS)
                        for k in follow(LHS):
                            f.append(k)
    return f


for NT in rules.keys():
    rules[NT]["first"] = list(set(first(NT)))
    printer.append("FIRST(%s)=%s" % (NT, list(set(first(NT)))))

printer.append("\n\n")
for NT in rules.keys():
    callStack.clear()
    rules[NT]["follow"] = list(set(follow(NT)))
    callStack.clear()
    printer.append("FOLLOW(%s)=%s" % (NT, list(set(follow(NT)))))


for i in printer:
    print(i)

print("\n")
