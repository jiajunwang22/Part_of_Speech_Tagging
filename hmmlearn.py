# -*- coding: UTF-8 -*-
import json
import datetime
import operator
import numpy as np

starttime = datetime.datetime.now()
print(starttime)
Transition = {}
Emission = {}
initialA = {}
terminalA = {}
A = []
numdigit = 0
digit = {}
with open("en_train_tagged.txt","r") as file:
    lines = file.readlines()
    for line in lines:
        pairs = line.split()
        previousTag = "STARTSTATE"
        for pair in pairs:
            part = pair.rsplit("/",1)

            if previousTag == "STARTSTATE":
                if part[1] not in initialA:
                    initialA[part[1]] = 1
                else:
                    initialA[part[1]] = initialA[part[1]] + 1
            # transition
            if part[1] not in Transition:
                Transition[part[1]] = {}
                Transition[part[1]][previousTag] = 1
            else:
                if previousTag not in Transition[part[1]]:
                    Transition[part[1]][previousTag] = 1
                else:
                    Transition[part[1]][previousTag] = Transition[part[1]][previousTag] + 1

            #emission
            if part[0].isdigit():
                if part[1] not in digit:
                    digit[part[1]] = {}
                else:
                    if part[0] not in digit[part[1]]:
                        digit[part[1]][part[0]] = 1
                    else:
                        digit[part[1]][part[0]] += 1
            if part[0] not in Emission:
                Emission[part[0]] = {}
                Emission[part[0]][part[1]] = 1
            else:
                if part[1] not in Emission[part[0]]:
                    Emission[part[0]][part[1]] = 1
                else:
                    Emission[part[0]][part[1]] = Emission[part[0]][part[1]] + 1

            previousTag = part[1]

        if previousTag not in terminalA:
            terminalA[previousTag] = 1
        else:
            terminalA[previousTag] = terminalA[previousTag] + 1
words = {}
for word in Emission:
    for key in Emission[word]:
        if key not in words:
            words[key] = {}
        if word not in words[key]:
            words[key][word] = 0
        words[key][word] += Emission[word][key]

print(words)
print(numdigit)
for key in digit:
    if len(digit[key]) != 0:
        print(key,reduce(operator.add,digit[key].values()),digit[key])
    else:
        print(key, 0, digit[key])
for tag in words:
    print(tag,reduce(operator.add, words[tag].values()))

json_in = json.dumps({"initialA": initialA, "terminalA": terminalA, "Transition": Transition, "Emission": Emission}, separators=(',', ': '), encoding="utf-8")

with open("output.txt","w") as w:
    print>>w, json_in.encode("UTF-8")

endtime = datetime.datetime.now()

print("cost: %s" % (endtime - starttime))