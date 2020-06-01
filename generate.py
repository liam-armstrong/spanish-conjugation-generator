from bs4 import BeautifulSoup
from requests import get
import random, csv

base = "https://www.linguasorb.com/spanish/verbs/most-common-verbs"
file = open('out.csv', 'w')
tenses = {"Subjunctive Present", "Indicative Present", "Indicative Imperfect", "Indicative Preterite"}
subjects = ["Yo", "Tu", "El/Elles/Usted", "Nosotros", "Vosotros", "Ellos/Elles/Ustedes"]
verbs = set()
solutions = {}

def populateVerbs():
    for i in range(1, 3):
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
            tds = row.find_all('td')
            span = tds[1].a.span
            verbs.add(span.get_text())

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
                    if(key == 'existir Indicative Preterite'):
                        print("here")
                    solutions[key] = row[7:12]
        
        for verb in tuple(verbs):
            key = verb + " Indicative Present"
            if not key in solutions:
                verbs.remove(verb)

def generateQuestions():
    file.write("question, answer \n")
    for verb in verbs:
        subjectInt = random.randrange(0, 5, 1)
        while(subjectInt == 4):
            subjectInt = random.randrange(0, 5, 1)
        tense = random.choice(tuple(tenses))
        solution = solve(subjectInt, verb, tense)
        file.write(subjects[subjectInt] + " + " + verb + " in " + tense + ", " + solution + "\n")

def solve(subject, verb, tense):
    key = verb + " " + tense
    return solutions[key][subject]

populateVerbs()
populateSolutions()
generateQuestions()