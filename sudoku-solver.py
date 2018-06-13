#! /usr/bin/python3

#Python sudoku solver using a backtracking algorithm.

# Author:    LuZiffer
# Copyright: GPLv3, 2016 

#This script can be found online on GitHub:
# https://github.com/LuZiffer/Sudoku-Solver 


#We will pick a random solutions if multiple exist
from random import randint

#Example sudoku problem.
example = [
    1,2,3, 4,5,6, 7,8,9, 
    4,5,6, 7,8,9, 1,2,3, 
    7,8,9, 1,2,3, 4,5,6, 

    2,3,1, 5,4,7, 6,9,8, 
    5,4,7, 6,9,8, 3,1,2, 
    6,9,8, 2,3,1, 5,4,7, 

    0,0,0, 0,0,0, 0,0,0, 
    0,0,0, 0,0,0, 0,0,0, 
    8,6,4, 0,0,0, 0,0,0, 
]


#Check whether adding a digit into the problem at the position index would be valid.  
def is_valid (problem, digit, index):
    if digit==0: return False #Inserting an empty digit is not valid. 
    
    #Row
    for i in range(0, 9):
        if i == index % 9: continue
        if problem[ int(index/9)*9 + i ] == digit: return False

    #Column 
    for i in range(0, 9):
        if i == int(index/9): continue
        if problem[ i*9 + index%9  ] == digit: return False

    #Block (use left upper corner as base index)
    base = int(int(index/9)/3)*3*9 + int((index%9)/3)*3
    for i in range(0, 9):
        if i == int((index - base)/9)*3 + (index - base)%3: continue
        if problem[base + 9*int(i/3) + i%3 ] == digit: return False

    return True


#Check whether the field was already given by checking whether it was empty at beginning. 
def field_given (problem, index):
    return problem[index] > 0

#Find index to last not given field.
def last_changeable_field (problem, index):
    i=index-1
    while  i >= 0 and field_given(problem, i):
        i -= 1
    return i

#Sudoku is empty if all entries are zero
def sudoku_empty (problem):
    for i in range(0,81):
        if problem[i]>0: return False
    return True
    

#Output
def print_sudoku (sudoku):
    s = ""
    
    if sudoku_empty (sudoku):
        s = " -/- "
    else:
        for i in range (0,81):

            #Save digit as ascii character
            digit = sudoku[i]
            if digit==0: s+= "-"
            else: s += str(digit)

            #Seperate columns and rows
            if (i+1)%3==0: s += (" ") 
            if (i+1)%9==0: s += ("\n") 
            if (i+1)%27==0: s +=("\n")
    
    #Output sudoku
    print (s)

#Check whether all fields are valid.
#(Caveat! This does not tell whether the problem is soluble.)
def problem_valid (problem):
    for i in range (0,81):
        if not problem[i] == 0:
            if not is_valid(problem, problem[i], i):
                return False
    return True

#Sudokus can be interpreted as 81 digit numbers.
#Thus we will order them canonically by imposing an alphabetical big-endian order.     
def is_larger (a, b):
    for i in range (0, 81):
        if a[i] > b[i]: return True
    return False


#Find alphabetically next smallest solution using positive backtracking
def find_next_solution (previous, problem):
    #Check problem
    if not problem_valid(problem):
        print ("No valid problem!")
        return [0]*81

    #Initialize next sudoku
    next = problem[0:81]

    #Ensure not taking same solution
    larger = False
    previous = previous[0:81] #Copy previous array to local variable to not make changes.
    previous [last_changeable_field(problem, 81)] += 1

    #Loop through next sudoku
    i = 0
    while i < 81:
        #Given values are fixed
        while i < 81 and field_given(problem, i): i+=1
        if i == 81: break

        #Find next smallest fitting digit
        if not larger: digit = max( previous[i], next[i] )
        else: digit = next[i]
        
        while digit <= 9:
            if is_valid (next, digit, i):
                next[i] = digit
                i += 1
                break
            else:
                digit += 1
                larger = True
            
        #If there is no fitting digit, start backtracking
        if digit>9:

            #Find last wrong assumption
            j = last_changeable_field(problem, i)
            while next[j]==9 and j>=0:
                j = last_changeable_field(problem, j)
        
            #Check unsolvability 
            if j<0: return [0]*81

            #Otherwise iterate wrongly assumed grid  
            next[j] += 1
            for k in range (j+1, i+1):
                if not field_given (problem, k): next[k]=0
            i = j
            
    return next

#The sudoku solver
def solve(problem):
    solutions = []
    s = [0]*81
    while True:
        s = find_next_solution(s, problem)
        if not sudoku_empty(s):
            solutions.append(s)
        else: return solutions


#Now let us run a test for debugging.
if __name__=='__main__':
    print('Sudoku solver.\nLuZiffer 2016, GPLv3\n') #Greet the user
    
    #Show the initial problem.
    print("Problem:")
    print_sudoku(example)
    print ("")
    
    #Solve the example the numbers of solutions and some specific random one.
    print("Solutions:")
    solutions = solve(example)

    #Print the number of solutions found 
    print ("There are "+str( len(solutions) ) + " solutions. Let's see one.")
    
    #Now print some specific random one
    index = randint(0, len(solutions)-1)
    print ("Printing the soduku number " + str(index+1)+':')
    print_sudoku( solutions[index] )
    print ("")
    
