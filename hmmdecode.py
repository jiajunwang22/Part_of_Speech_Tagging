# -*- coding: UTF-8 -*-

import numpy as np
import json
import operator
import datetime

starttime = datetime.datetime.now()
initialA = {}
tags = []
N = 0
unseen = []

def VITERBI(A, B, T, viterbi):
    backpointer = np.full((len(tagMap) + 1, len(T) + 1), -2)

    N = len(A)
    unseen = []
    #initialization step
    #first word is seen word
    if T[0] in Emissions:

        for state in range(0, N):
            #has word,tag pair
            curstate = tagMap[state]
            if curstate in Emissions[T[0]]:
                viterbi[state, 0] = initialA[curstate] + B[T[0]][curstate]
                backpointer[state, 0] = -1


    #first word is unseen word
    else:
        unseen.append(T[0])

        for state in range(0, N):
            viterbi[state, 0] = initialA[tagMap[state]]
            backpointer[state, 0] = -1

    previousViterbi = []
    #recursion setp
    for time in range(1, len(T)):
        maxRatio = -np.inf
        #seen word
        if T[time] in Emissions:
            for state in range(0, N):
                curstate = tagMap[state]
                #has word,tag pair
                if curstate in Emissions[T[time]]:

                    previousViterbi[:] = {}
                    for pstate in range(0, N):
                        # print("has word recursion:")
                        if viterbi[pstate,time - 1] != -np.inf:
                            # print(state, curstate, pstate)
                            previousViterbi.append(viterbi[pstate, time - 1] + A[state, pstate])
                        else:
                            previousViterbi.append(-np.inf)
                    narray = np.array(previousViterbi)
                    # print(narray)
                    # print(np.amax(narray))
                    # print(T[time],B[T[time]][curstate])
                    viterbi[state, time] = np.amax(narray) + B[T[time]][curstate]
                    backpointer[state, time] = np.argmax(narray)

        #unseen word
        else:
            unseen.append(T[time])

            for state in range(0, N):
                # print("no word recursion:")
                curstate = tagMap[state]
                previousViterbi[:] = {}
                for pstate in range(0, N):
                    if viterbi[pstate, time - 1] != -np.inf:
                        previousViterbi.append(viterbi[pstate, time - 1] + A[state, pstate])
                    else:
                        previousViterbi.append(-np.inf)
                narray = np.array(previousViterbi)
                viterbi[state, time] = np.amax(narray)
                backpointer[state, time] = np.argmax(narray)
                # print("unseen word: %s" % time, state, curstate, T[time], viterbi[state][time],
                #       backpointer[state, time])
    print("unseen %s" % unseen)

    #termination step
    previousViterbi[:] = {}
    for s in range(0, N):
        if viterbi[s, len(T) - 1] != -np.inf:
            previousViterbi.append(viterbi[s, len(T) - 1] + terminalA[tagMap[s]])
        else:
            previousViterbi.append(-np.inf)
    # narray = np.array(previousViterbi)


    backpointer[N, len(T)] = np.argmax(previousViterbi)
    return backpointer

tags = []
transitions = []
emissions = []
Words = []
with open("output.txt","r") as file:

    text = json.loads(file.read().decode("utf-8"))
    initialA = {k.encode("UTF-8"): v for k, v in text["initialA"].items()}
    terminalA = {k.encode("UTF-8"): v for k, v in text["terminalA"].items()}
    Emissions = {k.encode("UTF-8"): v for k, v in text["Emission"].items()}
    Transition = {k.encode("UTF-8"): v for k, v in text["Transition"].items()}

A = []
tags = Transition.keys()
list = {}
for dict in Transition:
    if dict in initialA:
        list[dict] = reduce(operator.add, Transition[dict].values())
    else:
        list[dict] = reduce(operator.add, Transition[dict].values())

print(list)
total = reduce(operator.add, initialA.values()) + len(tags)
print(total - len(tags))
print(len(tags))
print(len(list))
for key in list:
    if key in initialA:
        initialA[key] = np.log(float(initialA[key] + 1) / total)
    else:
        initialA[key] = np.log(float(1) / total)
    if key in terminalA:
        terminalA[key] = np.log(float(terminalA[key] + 1) / total)
    else:
        terminalA[key] = np.log(float(1) / total)

print(initialA)
print(terminalA)

tagMap = {}
index = 0
#ti is current, t2 is previous
test = {}
for t1 in tags:
    tagMap[index] = t1
    index = index + 1
    test[t1] = {}
    for t2 in tags:

        if t2 in Transition[t1]:
            test[t1][t2] = np.log(float(Transition[t1][t2] + 1)/(list[t1] + len(tags)))
            A.append(np.log(float(Transition[t1][t2] + 1)/(list[t1] + len(tags))))
        else:
            test[t1][t2] = np.log(float(1)/(list[t1] + len(tags)))
            A.append(np.log(float(1)/(list[t1] + len(tags))))
print(tagMap)

print("hello")
print(test)
A = np.array(A).reshape(len(list),len(list))

for key, values in Emissions.items():
    for k, v in Emissions[key].items():
        Emissions[key][k] = np.log(float(v) / list[k])

output = []


with open("en_dev_raw.txt","r") as file:
    lines = file.readlines()
    for line in lines:
        words = line.split(" ")
        viterbi = np.full((len(tagMap) + 2, len(words)), -np.inf)

for line in lines:
    words = line.split()
    viterbi = np.full((len(tagMap) + 1, len(words)), -np.inf)
    result = VITERBI(A, Emissions, words, viterbi)
    print ("backpointer:")
    print(result)
    l = []
    col = len(words)
    row = len(tagMap)
    while True:
        state = result[row, col]
        if state == -1:
            break
        l.append(tagMap[state])
        col = col - 1
        row = state

    wordtag = []
    l.reverse()
    i = 0
    for word in words:
        wordtag.append(word + "/" + l[i])
        i = i + 1
    output.append(wordtag)



with open("OUT.txt","w") as w:
    for line in output:
        w.write(" ".join(str(word) for word in line)+"\n")

endtime = datetime.datetime.now()

print("cost: %s " % (endtime - starttime))










