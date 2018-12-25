#! /usr/bin/env python
#coding=utf-8
from __future__ import division

v_table={} # variable table

def getNums(t):
    global lst
    lst = []
    for i in t.getchildren():
        if i.getdata() == '[NUMS]':
            getNums(i)
        else:
            lst .append(i.getvalue())
    return lst

def update_v_table(name, value):
    v_table[name] = value


def trans(node):

    
    # Translation

    # Assignment
    if node.getdata()=='[ASSIGNMENT]':
        ''' statement : exp '=' exp
                        | exp '=' factor
                        | VARIABLE '=' exp   
                        | VARIABLE '=' factor
                        | VARIABLE '=' nums
                        | VARIABLE '=' function'''
        if node.getchild(0).getdata() == '[EXP]':
            key1 = node.getchild(0).getchild(0).getdata()
            index1 = int(trans(node.getchild(0).getchild(2)))
            if node.getchild(2).getdata() == '[EXP]':
                key2 = node.getchild(2).getchild(0).getdata()
                index2 = int(trans(node.getchild(2).getchild(2)))
                v_table[key1][index1] = v_table[key2][index2]
            else:
                value = trans(node.getchild(2))
                v_table[key1][index1] = value
        else:
            key1 = node.getchild(0).getdata()
            if node.getchild(2).getdata() == '[EXP]':
                key2 = node.getchild(2).getchild(0).getdata()
                index2 = int(trans(node.getchild(2).getchild(2)))
                update_v_table(key1, v_table[key2][index2])
            else:
                value = trans(node.getchild(2))
                update_v_table(key1, value)
    
    # Operation
    elif node.getdata() == '[OPERATION]':
        '''operation : VARIABLE DPLUS
                    |VARIABLE '=' factor '+' factor
                    | VARIABLE '=' factor '-' factor
                    | VARIABLE '=' '(' factor '+' factor ')' DIV factor
                    | VARIABLE '=' '(' factor '-' factor ')' DIV factor'''
        if len(node.getchildren())==2:
            value = v_table[node.getchild(0).getdata()]
            update_v_table(node.getchild(0).getdata(), value+1)

        elif len(node.getchildren()) == 5:
            arg0=trans(node.getchild(2))
            arg1=trans(node.getchild(4))
            op=node.getchild(3).getdata()

            if op == '+':
                value = arg0+arg1
            else:
                value = arg0-arg1
            node.getchild(0).setvalue(value)
            update_v_table(node.getchild(0).getdata(), value)
        else:
            arg0 = trans(node.getchild(3))
            arg1 = trans(node.getchild(5))
            op = node.getchild(4).getdata()
            if op == '+':
                sum = arg0+arg1
            else:
                sum = arg0-arg1
            arg2 = trans(node.getchild(8))
            value = sum // arg2
            node.getchild(0).setvalue(value)
            update_v_table(node.getchild(0).getdata(), value)

    
    # If
    elif node.getdata()=='[IF]':
        r'''if : IF '(' condition ')' '{' statements '}' '''
        global ifcondition
        children = node.getchildren()
        trans(children[0])
        condition=children[0].getvalue()
        if condition:
            ifcondition = True
            for c in children[1:]:
                trans(c)
        else:
            ifcondition = False

    elif node.getdata()=='[ELIF]':
        r'''elif : ELIF '(' condition ')' '{' statements '}' '''
        if ifcondition == False:
            children = node.getchildren()
            trans(children[0])
            condition=children[0].getvalue()
            if condition:
                ifcondition = True
                for c in children[1:]:
                    trans(c)
            else:
                ifcondition = False

    elif node.getdata()=='[ELSE]':
        r'''else : ELSE '{' statements '}' '''
        if ifcondition == False:
            ifcondition = True
            children = node.getchildren()
            trans(children[0])

                
    # While
    elif node.getdata() == '[WHILE]':
        r'''while : WHILE '(' condition ')' '{' statements '}' '''
        global isBreak
        isBreak = False
        children = node.getchildren()
        while trans(children[0]):
            for c in children[1:]:
                trans(c)
            if isBreak:
                break

    elif node.getdata() == '[FOR]':
        ''' FOR '(' statements ';' condition ';' statements ')' '{' statements '}' '''
        global isBreak
        isBreak = False
        children = node.getchildren()
        # the transformation order is 0 1 3 2
        trans(children[0])
        while trans(children[1]):
                for c in children[3:]:
                    trans(c)
                trans(children[2])
                if isBreak:
                    break
            
                
    # Condition
    elif node.getdata() == '[CONDITION]':
        r'''condition : factor '>' factor
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
        temp = node.getchild(0).getdata()
        if node.getchild(0).getdata()=='[FACTOR]':
            arg0 = trans(node.getchild(0))
            if node.getchild(2).getdata() == '[EXP]':
                key2 = node.getchild(0).getchild(2).getdata()
                index2 = int(trans(node.getchild(2).getchild(2)))
                arg1 = v_table[key2][index2]
            else:
                arg1 = trans(node.getchild(2))
        if node.getchild(0).getdata()=='[EXP]':
            key1 = node.getchild(0).getchild(0).getdata()
            index1 = int(trans(node.getchild(0).getchild(2)))
            arg0 = v_table[key1][index1]
            if node.getchild(2).getdata()=='[EXP]':
                key2 = node.getchild(0).getchild(2).getdata()
                index2 = int(trans(node.getchild(2).getchild(2)))
                arg1 = v_table[key2][index2]
            else:
                arg1 = trans(node.getchild(2))

        op=node.getchild(1).getdata()

        if op=='>':
            node.setvalue(arg0>arg1)
        elif op=='<':
            node.setvalue(arg0<arg1)
        elif op == '<=':
            node.setvalue(arg0 <= arg1)
        elif op == '>=':
            node.setvalue(arg0 >= arg1)
        elif op == '==':
            node.setvalue(arg0 == arg1)



    elif node.getdata()=='[FACTOR]':
        child = node.getchild(0)
        if child.getvalue() == None:
            value = v_table[child.getdata()]
        else:
            value = child.getvalue()
        node.setvalue(value)

    elif node.getdata()=='[NUMS]':
        node.setvalue(getNums(node))

    elif node.getdata()=='[FUNCTION]':
        function_name = node.getchild(0).getdata()
        v_naem = node.getchild(2).getdata()
        if function_name=='len':
           value = len(v_table[v_naem])
        node.setvalue(value)

    elif node.getdata()=='[BREAK]':
        isBreak = True

    # Print
    elif node.getdata() == '[PRINT]':
        '''print : PRINT '(' VARIABLE ')' '''
        arg = v_table[node.getchild(2).getdata()]
        print arg


    else:
        for c in node.getchildren():
            trans(c)
    
    return node.getvalue()


