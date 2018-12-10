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
                  | print'''
    if len(t)==2:
        t[0]=node(['STATEMENT'])
        t[0].add(t[1])

def p_assignment(t):
    '''assignment : VARIABLE '=' NUMBER'''
    if len(t)==4:
        t[0]=node('[ASSIGNMENT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(num_node(t[3]))

def p_operation(t):
    '''operation : VARIABLE '=' expression '''
    if len(t)==4:
        t[0]=node('[OPERATION]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])

def p_expression(t):
    '''expression : expression '+' term
                  | expression '-' term
                  | term'''
    if len(t)== 4:
        t[0]=node('[EXPRESSION]')
        t[0].add(t[1])
        t[0].add(node(t[2]))
        t[0].add(t[3])
    if len(t) == 2:
        t[0] = node('[EXPRESSION]')
        t[0].add(t[1])

def p_term_1(t):
    '''term : term '*' VARIABLE
            | term '/' VARIABLE'''
    if len(t)== 4:
        t[0]=node('[TERM]')
        t[0].add(t[1])
        t[0].add(node(t[2]))
        t[0].add(node(t[3]))

def p_term_2(t):
    '''term : term '*' NUMBER
            | term '/' NUMBER'''
    if len(t)== 4:
        t[0]=node('[TERM]')
        t[0].add(t[1])
        t[0].add(node(t[2]))
        t[0].add(num_node(t[3]))

def p_term_3(t):
    '''term : NUMBER'''
    if len(t)==2:
        t[0]=node('[TERM]')
        t[0].add(num_node(t[1]))

def p_term_4(t):
    '''term : VARIABLE'''
    if len(t)== 2:
        t[0] = node('[TERM]')
        t[0].add(node(t[1]))


def p_print(t):
    '''print : PRINT '(' variable_s ')' '''
    if len(t)==5:
        t[0]=node('[PRINT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])
        t[0].add(node(t[4]))

def p_variable_s(t):
    '''variable_s : variable_s ',' VARIABLE
                 | VARIABLE'''
    if len(t)==4:
        t[0]=node('[VARIABLE_S]')
        t[0].add(t[1])
        t[0].add(node(t[3]))
    elif len(t)==2:
        t[0]=simple_node(t,'[VARIABLE_S]')

def p_error(t):
    print("Syntax error at '%s'" % t.value)

yacc.yacc()