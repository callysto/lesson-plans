#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 2021

@author: TinaL5, adapted from lisacao, Laura G.F.
"""

# libraries
import random

################################ TEXT ENCODING

def soccer(text): # blocked out grey with emoji
    rvr = "\033[1;35m ⚽️ : \033[1;0m" + text + "\033[1;0m"
    return rvr

def task(text, check = False): # light blue with emoji option
    if check == True:
        blu = "\033[1;36m" + "✅ " + text + "\033[1;0m"
        return blu
    else:
        blu = "\033[1;36m" + text + "\033[1;0m"
        return blu

def bedazzle(text): # purple with randomized  emoji 
     sparkle = [" 🌟 ", " 🎉 ", " 🥳 ", " 🤩 ", " 🏆 ", " 😎 "]
     prl = "\033[1;35m" + random.choice(sparkle) + text + "\033[1;0m"
     return prl
   
def normal(text): # plain black 
     nrl = "\033[1;0m" + text + "\033[1;0m"
     return nrl
 
def code(text): # bright green 
     grn = "\033[1;32m" + text + "\033[1;0m"
     return grn
 
def tryagain(text, exclaim = True): # red with default emoji 
    if exclaim == False:
        red = "\033[1;31m" + text + "\033[1;0m"
        return red
    else:
        red = "\033[1;31m" + "❗️ " + text + "\033[1;0m"
        return red

# positive feedback for correct answers
def correct_answer(): # random positive reinforcement
    compliment = ["Amazing work!", "Nice job!", "Right on!", "You're out of this world!", "Great stuff!", "You rock!", "I wish I were this good!", "Correct!", "That was great!", "You're picking up on this really well!"]
    nice = print(bedazzle(random.choice(compliment)))
    return nice 


################################ CHALLENGE 1

# Question 1 
def challenge1(): # interpretation of scatter plots
    print(soccer(" Go back and look at the scatter plot Relationship between average ball possession (%) and total goals. The data points further from the trend line seem to tell a different story.\n"), task("Hover over the data points to find the team with average ball possession of 44% and 16 total goals. ", check = True))
    def Q1a(): # Monchengladbach total goals
        ans1 = str(input(normal("The team is: ")))
        if ans1 == "Monchengladbach":
            correct_answer()
        else: 
            print(tryagain(" Make sure to locate ball possession on the x-axis and total goals on the y-axis."),tryagain(" The team name starts with an M.", exclaim = False))
            Q1a()

    #execute
    Q1a()
            
################################ CHALLENGE 2

# Question 2 
def challenge2(): # interpretation of scatter plots
    print(soccer(" Go back and look at the scatter plot Relationship between average ball possession (%) and goal difference by team. Let's try to gain more insight into Monchengladbach who ties second with total goals of 16.\n"), task("Hover over the data points to determine Monchengladbach's goal difference. ", check = True))
    def Q2a(): # Monchengladbach goal difference
        ans1 = str(input(normal("Monchengladbach's goal difference is: ")))
        if ans1 == "7":
            correct_answer()
        else: 
            print(tryagain(" Make sure to locate average ball possession of 44% on the x-axis.", exclaim = False))
            Q2a()
            
    #execute
    Q2a()           
            
            
################################ CHALLENGE 3

# Question 3 
def challenge3(): # interpretation of scatter plots
    print(soccer(" Looking at the scatter plot Relationship between average ball possession (%) and goal difference by team, try to find the team with the second lowest average ball possession of 41%, total goals of 10, and a goal difference of 7.\n"), task("Hover over the data points to locate the team. ", check = True))
    def Q3a(): # Porto
        ans1 = str(input(normal("The team is: ")))
        if ans1 == "Porto":
            correct_answer()
            print('Porto only had 3 goals scored against them with their opponents possessing the ball 56% of the time and they were able to score 10 goals!')
        else: 
            print(tryagain(" Make sure to locate average ball possession of 41% on the x-axis and goal difference of 7 on the y-axis. The team's name starts with a P.", exclaim = False))
            Q3a()
            
    #execute
    Q3a() 