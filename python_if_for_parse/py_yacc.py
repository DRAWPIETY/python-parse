#! /usr/bin/env python
#coding=utf-8
import ply.yacc as yacc
from py_lex import *
from node import node,num_node

# YACC for parsing Python

def simple_node(t,name):
    t[0]=node(name)
    for i in range(1,len(t)):
        t[0].add(node(t[i]))
    return t[0]

def p_program(t):
    '''program : statements'''
    if len(t)==2:
        t[0]=node('[PROGRAM]')
        t[0].add(t[1])
        
def p_statements(t):
    '''statements : statements statement
                  | statement'''
    if len(t)==3:
        t[0]=node('[STATEMENTS]')
        t[0].add(t[1])
        t[0].add(t[2])
    elif len(t)==2:
        t[0]=node('[STATEMENTS]')
        t[0].add(t[1])

def p_statement(t):
    ''' statement : assignment
                  | operation
                  | print
                  | if
                  | while
                  | elif
                  | else
                  | break
                  | for'''
    if len(t)==2:
        t[0]=node(['STATEMENT'])
        t[0].add(t[1])
        
def p_assignment1(t):
    '''assignment : VARIABLE '=' factor'''
    if len(t)==4:
        t[0]=node('[ASSIGNMENT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])

def p_assignment2(t):
    '''assignment : VARIABLE '=' '[' nums ']' '''
    if len(t)==6:
        t[0]=node('[ASSIGNMENT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[4])


def p_assignment3(t):
    '''assignment : VARIABLE '='  exp '''
    if len(t)==4:
        t[0]=node('[ASSIGNMENT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])

def p_assignment4(t):
    '''assignment : exp '='  exp '''
    if len(t)==4:
        t[0] = node('[ASSIGNMENT]')
        t[0].add(t[1])
        t[0].add(node(t[2]))
        t[0].add(t[3])

def p_assignment5(t):
    '''assignment : exp '='  factor '''
    if len(t)==4:
        t[0] = node('[ASSIGNMENT]')
        t[0].add(t[1])
        t[0].add(node(t[2]))
        t[0].add(t[3])

def p_assignment7(t):
    '''assignment : VARIABLE '='  function '''
    if len(t)==4:
        t[0] = node('[ASSIGNMENT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])

def p_function(t):
    '''function : LEN '(' VARIABLE ')' '''
    if len(t)==5:
        simple_node(t,'[FUNCTION]')


def p_exp(t):
    '''exp : VARIABLE '[' factor ']' '''
    if len(t)==5:
        t[0]=node('[EXP]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])
        t[0].add(node(t[4]))

def p_nums(t):
    '''nums : nums ',' NUMBER
            | NUMBER'''
    if len(t)==4:
        t[0]=node('[NUMS]')
        t[0].add(t[1])
        t[0].add(num_node(t[3]))
    elif len(t)==2:
        t[0]=node('[NUMS]')
        t[0].add(num_node(t[1]))

def p_operation1(t):
    '''operation : VARIABLE '=' factor '+' factor
                | VARIABLE '=' factor '-' factor '''
    if len(t)==6:
        t[0]=node('[OPERATION]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])
        t[0].add(node(t[4]))
        t[0].add(t[5])

def p_operation2(t):
    '''operation : VARIABLE '=' '(' factor '+' factor ')' DIV factor
                |  VARIABLE '=' '(' factor '-' factor ')' DIV factor'''
    if len(t)==10:
        t[0]=node('[OPERATION]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(node(t[3]))
        t[0].add(t[4])
        t[0].add(node(t[5]))
        t[0].add(t[6])
        t[0].add(node(t[7]))
        t[0].add(node(t[8]))
        t[0].add(t[9])

def p_operation3(t):
    '''operation : VARIABLE DPLUS'''
    if len(t)==3:
        t[0]=node('[OPERATION]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))

def p_factor1(t):
    '''factor : NUMBER'''
    if len(t)==2:
        t[0]=node('[FACTOR]')
        t[0].add(num_node(t[1]))

def p_factor2(t):
    '''factor : VARIABLE'''
    if len(t)==2:
        t[0]=node('[FACTOR]')
        t[0].add(node(t[1]))

def p_print(t):
    '''print : PRINT '(' VARIABLE ')' '''
    if len(t)==5:
        t[0]=simple_node(t,'[PRINT]')
                
def p_if(t):
    r'''if : IF '(' condition ')' '{' statements '}' '''
    if len(t)==8:
        t[0]=node('[IF]')
        t[0].add(t[3])
        t[0].add(t[6])

def p_elif(t):
    r'''elif : ELIF '(' condition ')' '{' statements '}' '''
    if len(t)==8:
        t[0]=node('[ELIF]')
        t[0].add(t[3])
        t[0].add(t[6])

def p_else(t):
    r'''else : ELSE '{' statements '}' '''
    if len(t)==5:
        t[0]=node('[ELSE]')
        t[0].add(t[3])



def p_condition1(t):
    '''condition : factor '>' factor
                 | factor '<' factor
                 | factor LESSEQU factor
                 | factor MOREEQU factor
                 | factor EQEQ factor
                 | factor '>' exp
                 | factor '<' exp
                 | factor LESSEQU exp
                 | factor MOREEQU exp
                 | factor EQEQ exp
                 | exp '>' factor
                 | exp '<' factor
                 | exp LESSEQU factor
                 | exp MOREEQU factor
                 | exp EQEQ factor
                 | exp '>' exp
                 | exp '<' exp
                 | exp LESSEQU exp
                 | exp MOREEQU exp
                 | exp EQEQ exp'''
    if len(t)==4:
        t[0]=node('[CONDITION]')
        t[0].add(t[1])
        t[0].add(node(t[2]))
        t[0].add(t[3])

def p_while(t):
    r'''while : WHILE '(' condition ')' '{' statements '}' '''
    if len(t)==8:
        t[0]=node('[WHILE]')
        t[0].add(t[3])
        t[0].add(t[6])

def p_for(t):
    r'''for : FOR '(' statements ';' condition ';' statements ')' '{' statements '}' '''
    if len(t)==12:
        t[0]=node('[FOR]')
        t[0].add(t[3])
        t[0].add(t[5])
        t[0].add(t[7])
        t[0].add(t[10])

def p_break(t):
    r'''break : BREAK'''
    if len(t)==2:
        t[0]=node('[BREAK]')
        t[0].add(node(t[1]))

def p_error(t):
    print("Syntax error at '%s'" % t.value)

yacc.yacc()
