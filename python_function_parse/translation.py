#! /usr/bin/env python
# coding=utf-8
from __future__ import division

f_table = {}  # function table


class Tran:
    def __init__(self):
        self.v_table = {}  # variable table
        self.isReturn = False

    def update_v_table(self, name, value):
        self.v_table[name] = value

    def getNums(self,t):
        global lst
        lst = []
        for i in t.getchildren():
            if i.getdata() == '[NUMS]':
                self.getNums(i)
            else:
                lst .append(i.getvalue())
        return lst

    def getcsname(self,t):
        global vnlst
        vnlst = []
        for i in t.getchildren():
            if i.getdata() == '[CANSHU]':
                self.getcsname(i)
            else:
                vn = i.getchild(0).getchild(0).getdata()
                vnlst.append(vn)
        return vnlst

    def getcsvalue(self,t):
        global vnlst
        vnlst = []
        for i in t.getchildren():
            temp = i.getdata()
            if i.getdata() == '[CANSHU]':
                self.getcsvalue(i)
            else:
                csvalue = self.trans(i)
                vnlst.append(csvalue)
        return vnlst


    def trans(self,node):

        # Translation
        temp = node.getdata()
        # Assignment
        if node.getdata()=='[ASSIGNMENT]':
            ''' statement : exp '=' exp
                            | exp '=' factor
                            | VARIABLE '=' exp
                            | VARIABLE '=' factor
                            | VARIABLE '=' nums
                            | VARIABLE '=' len'''

            if node.getchild(0).getdata() == '[EXP]':
                key = node.getchild(0).getchild(0).getdata()
                index = int(self.trans(node.getchild(0).getchild(2)))
                self.v_table[key][index] = self.trans(node.getchild(2))
            else:
                key = node.getchild(0).getdata()
                value = self.trans(node.getchild(2))
                self.update_v_table(key, value)

        # Operation
        elif node.getdata() == '[OPERATION]':
            '''operation : VARIABLE '=' calexp
                        | VARIABLE ADDEQU factor
                        | VARIABLE SUBEQU factor '''
            if node.getchild(1).getdata() == '=':
                self.update_v_table(node.getchild(0).getdata(), self.trans(node.getchild(2)))
            if node.getchild(1).getdata() == '+=':
                a = self.v_table[node.getchild(0).getdata()]
                self.update_v_table(node.getchild(0).getdata(), a+1)
            if node.getchild(1).getdata() == '-=':
                a = self.v_table[node.getchild(0).getdata()]
                self.update_v_table(node.getchild(0).getdata(), a-1)

        elif node.getdata() == '[CALEXP]':
            '''calexp : calexp '+' factor
                    | calexp '-' factor
                    | len
                    | factor'''
            arg0 = self.trans(node.getchild(0))
            if len(node.getchildren())==3:
                op = node.getchild(1).getdata()
                arg1 = self.trans(node.getchild(2))
                if op=='+':
                    value=arg0+arg1
                else:
                    value=arg0-arg1

                node.setvalue(value)
            else:
                node.setvalue(arg0)

        # If
        elif node.getdata()=='[IF]':
            r'''if : IF '(' conditions ')' '{' statements '}' '''
            global ifcondition
            children = node.getchildren()
            condition = self.trans(children[0])
            if condition:
                ifcondition = True
                for c in children[1:]:
                    self.trans(c)
            else:
                ifcondition = False

        elif node.getdata()=='[ELIF]':
            r'''elif : ELIF '(' conditions ')' '{' statements '}' '''
            if ifcondition == False:
                children = node.getchildren()
                self.trans(children[0])
                condition=children[0].getvalue()
                if condition:
                    ifcondition = True
                    for c in children[1:]:
                        self.trans(c)
                else:
                    ifcondition = False

        elif node.getdata()=='[ELSE]':
            r'''else : ELSE '{' statements '}' '''
            if ifcondition == False:
                ifcondition = True
                children = node.getchildren()
                self.trans(children[0])


        # While
        elif node.getdata() == '[WHILE]':
            r'''while : WHILE '(' conditions ')' '{' statements '}' '''
            global isBreak
            isBreak = False
            children = node.getchildren()
            while self.trans(children[0]):
                for c in children[1:]:
                    self.trans(c)
                if isBreak:
                    break

        elif node.getdata() == '[CONDITIONS]':
            r'''conditions : conditions AND condtion
                            | condition '''
            if len(node.getchildren())==1:
                value = self.trans(node.getchild(0))
            else:
                arg0 = self.trans(node.getchild(0))
                op = node.getchild(1).getdata()
                arg1 = self.trans(node.getchild(2))
                if op == 'and':
                    value = (arg0 and arg1)
            node.setvalue(value)



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

            arg0 = self.trans(node.getchild(0))
            op=node.getchild(1).getdata()
            arg1 = self.trans(node.getchild(2))

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
            name =child.getdata()
            if child.getvalue() == None:
                value = self.v_table[child.getdata()]
            else:
                value = child.getvalue()
            node.setvalue(value)

        elif node.getdata()=='[EXP]':
            key = node.getchild(0).getdata()
            index = int(self.trans(node.getchild(2)))
            value = self.v_table[key][index]
            node.setvalue(value)

        elif node.getdata()=='[NUMS]':
            node.setvalue(self.getNums(node))

        elif node.getdata()=='[LEN]':
            v_name = node.getchild(0).getdata()
            value = len(self.v_table[v_name])
            node.setvalue(value)
        elif node.getdata()=='[BREAK]':
            isBreak = True


        # Print
        elif node.getdata() == '[PRINT]':
            '''print : PRINT '(' VARIABLE ')' '''
            arg = self.v_table[node.getchild(2).getdata()]
            print arg

        elif node.getdata() == '[FUNCTION]':
             # canshu at here is different with RUNFUNCTION, it without value
            r'''function : DEF VARIABLE '(' canshu ')' '{' statements '}' '''
            fname = node.getchild(0).getdata()  #function's name
            vname = self.getcsname(node.getchild(1)) #canshu list
            print 'canshu list  = %s' % vname
            f_table[fname] = (vname, node.getchild(2))  # function_name dict: (canshu_names, function node(or called dress))

        elif node.getdata() == '[RUNFUNCTION]':
            r'''runfunction : VARIABLE '(' canshu ')' '''
            fname = node.getchild(0).getdata()
            vname1 = self.getcsvalue(node.getchild(1))
            vname0, fnode = f_table[fname]
            t = Tran()
            for i in range(len(vname0)):
                t.update_v_table(vname0[i],vname1[i])
            t.trans(fnode)

        elif node.getdata() == '[RETURN]':
            r'''return : RETURN
                        | RETURN CALEXP'''
            temp = node.getdata()
            if len(node.getchildren()) == 1:
                node.setvalue(self.trans(node.getchild(0)))
            else:
                node.setvalue(None)
            self.isReturn = True

        else:
            for c in node.getchildren():
                if self.isReturn:
                    break
                self.trans(c)

        return node.getvalue()


