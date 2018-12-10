#! /usr/bin/env python
#coding=utf-8
from __future__ import division

v_table={} # variable table

def update_v_table(name,value):
    v_table[name]=value


def get_name(t):
    name_list = []
    global name_list
    for i in t.getchildren():
        if i.getdata() == '[VARIABLE_S]':
            get_name(i)
        else:
            name_list += list(i.getdata())
    return name_list


def set_term_v(t):
    temp = t.getdata()
    if len(t.getchildren())==1:
        if t.getchild(0).getvalue() == None:
            temp = t.getchild(0).getdata()
            value = v_table[t.getchild(0).getdata()]
        else:
            temp = t.getchild(0).getdata()
            value = t.getchild(0).getvalue()
        t.setvalue(value)
    elif len(t.getchildren())==3:
        set_term_v(t.getchild(0))
        v1 = t.getchild(0).getvalue()
        op = t.getchild(1).getdata()
        if t.getchild(2).getvalue() == None:
            v2 = v_table[t.getchild(2).getdata()]
        else:
            v2 = t.getchild(2).getvalue()

        if op == '*':
            t.setvalue(v1 * v2)
        else:
            t.setvalue(v1 / v2)

# the last one should to judge is number or variable
def set_exp_v(t):
    temp = t.getdata()
    if len(t.getchildren())==1:
        temp = t.getchild(0).getdata()
        set_term_v(t.getchild(0))
        t.setvalue(t.getchild(0).getvalue())
    elif len(t.getchildren())==3:
        temp1 = t.getchild(0).getdata()
        temp2 = t.getchild(2).getdata()
        set_exp_v(t.getchild(0))
        set_term_v(t.getchild(2))
        v1 = t.getchild(0).getvalue()
        op = t.getchild(1).getdata()
        v2 = t.getchild(2).getvalue()

        if op == '+':
            t.setvalue(v1 + v2)
        else:
            t.setvalue(v1 - v2)


# Translation
def trans(node):
    for c in node.getchildren():
        trans(c)

    # Assignment
    if node.getdata()=='[ASSIGNMENT]': 
        ''' statement : VARIABLE '=' NUMBER'''
        value=node.getchild(2).getvalue()
        node.getchild(0).setvalue(value)
        # update v_table
        update_v_table(node.getchild(0).getdata(),value)

    # Operation
    elif node.getdata()=='[OPERATION]':
        '''operation : VARIABLE '=' expression'''
        set_exp_v(node.getchild(2))
        value=node.getchild(2).getvalue()

        node.getchild(0).setvalue(value)
        # update v_table
        update_v_table(node.getchild(0).getdata(),value)


    # Print
    elif node.getdata()=='[PRINT]':
        '''print : PRINT '(' variable_s ')' '''
        name_list = get_name(node.getchild(2))
        for i in name_list:
            print v_table[i],
        print

        
        
            
            
        
        

