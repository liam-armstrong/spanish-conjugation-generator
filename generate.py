from bs4 import BeautifulSoup
from requests import get
import random, csv, sys, getopt

base = "https://www.linguasorb.com/spanish/verbs/most-common-verbs"
file = open('out.csv', 'w')
tenses = {"Subjunctive Present", "Indicative Present", "Indicative Imperfect", "Indicative Preterite"}
subjects = ["Yo", "Tu", "El/Elles/Usted", "Nosotros", "Vosotros", "Ellos/Elles/Ustedes"]
verbs = set()
solutions = {}
topVerbs = 100
numQuestions = 100
include2ndP = False

try:
    opts, args = getopt.getopt(sys.argv[1:],"n:t:v",["num=","top="])
except getopt.GetoptError:
    print('Usage: generate.py -n <numberofquestions> -t <topTverbs>')
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-t", "--top"):
        if(int(arg) > 100):
            print("-t is too large, defaulting to 100")
        else:
            topVerbs = int(arg)
    elif opt in ("-n", "--num"):
        numQuestions = int(arg)
    elif opt == "-v":
        include2ndP = True

def populateVerbs():
    count = 0
    for i in range(1, 5):
        url = ""
        if i == 1:
            url = base
        else:
            url = base + "/" + str(i)
        html = BeautifulSoup(get(url).text, "lxml")
        flag = True

        for row in html.find_all('tr'):
            if flag:
                flag = False
                continue
            if(count >= topVerbs):
                return
            tds = row.find_all('td')
            span = tds[1].a.span
            verbs.add(span.get_text())
            count += 1

def populateSolutions():
    with open('verbdb.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        flag = True
        for row in reader:
            if flag:
                flag = False
                continue
            if row[0] in verbs:
                tense = row[3] + " " + row[5]
                if tense in tenses:
                    key = row[0] + " " + tense
                    solutions[key] = row[7:12]
        
        for verb in tuple(verbs):
            key = verb + " Indicative Present"
            if not key in solutions:
                verbs.remove(verb)
        
        return len(solutions) * ((include2ndP*1) + 5)

def generateQuestions(maxProblems):
    file.write("question, answer \n")
    verbTuple = tuple(verbs)
    tenseTuple = tuple(tenses)
    i = 0
    while(i < numQuestions):
        verb = random.choice(verbTuple)
        tense = random.choice(tenseTuple)
        subjectInt = random.randrange(0, 5, 1)
        while(subjectInt == 4 and not include2ndP):
            subjectInt = random.randrange(0, 5, 1)
        solution = solve(subjectInt, verb, tense)
        if(solution == 0):
            if(i >= (maxProblems * 0.8)):
                print("Argument -n is larger than maximum ("+ str(maxProblems * 0.9) + ")")
                sys.exit(2)
            continue
        else:
            i += 1
            file.write(subjects[subjectInt] + " + " + verb + " in " + tense + ", " + solution + "\n")
        

def solve(subject, verb, tense):
    key = verb + " " + tense
    ans = solutions[key][subject]
    if ans == 0:
        return 0
    solutions[key][subject] = 0
    return ans

populateVerbs()
print(len(verbs))
maxProblems = populateSolutions()
generateQuestions(maxProblems)