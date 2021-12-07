from Lexer import return_tokens
from Lexer import entrada
from scope import symbol
from Ensamblador import fin
from Ensamblador import inicio
from Ensamblador import obtener_valores
from Ensamblador import obtener_valores_if
from Ensamblador import obtener_valores_else
from Ensamblador import obtener_valores_func
from Ensamblador import fin_if
from Ensamblador import fin_else
from Ensamblador import main_i
from Ensamblador import fin_func
from Ensamblador import obtener_valores_return
from Ensamblador import assig_var
import pandas as pd
import sys
import graphviz

symbol_table=[]
symbol_table2=[]

class nodo: 
    global id
    def __init__(self, token, valor, padre = None):
      self.children = []
      self.valor = valor
      self.token = token
      self.visitado = False 
      self.dead = False 
      
    def agregar_hijo(self, hijo):
      self.children.append(hijo)
      hijo.padre = self

    def Preorden(self): 
      nodes=[]
      nodes.append(self)
      while (len(nodes)): 
          curr = nodes[0]
          nodes.pop(0)
          for it in range(len(curr.children)-1,-1,-1): 
              nodes.insert(0,curr.children[it])

    def insertS(self, hijo, numero): 
      nodes=[]
      nodes.append(self)
      while (len(nodes)): 
          curr = nodes[0]
          if len(curr.children) == 0 and curr.dead == False:
            hijo = nodo(hijo, numero)
            curr.agregar_hijo(hijo)
            return
          nodes.pop(0)
          cont = 0
          for it in range(len(curr.children)-1,-1,-1): 
              nodes.insert(0,curr.children[it])
              if curr.children[it].visitado == True:
                cont = cont + 1
          if cont == 0 and curr.dead == False:
            hijo = nodo(hijo, numero)
            curr.agregar_hijo(hijo)
            return

    def visitarNodo(self):
      nodes=[]
      nodes.append(self)
      while (len(nodes)): 
          curr = nodes[0]
          if curr.visitado == True:
            curr.dead = True
          if curr.visitado == False:
            curr.visitado = True
            return
          nodes.pop(0)
          for it in range(len(curr.children)-1,-1,-1): 
              nodes.insert(0,curr.children[it]) 

def sintaxis(): 
  if len(entrada) == 0:
    return True
  else:
    return False 

def parsing():

  stack = return_tokens('Prueba.txt') 
  df = pd.read_csv('tablaF.csv', index_col=0)
  stack =["$"] 
  entrada.append("$")
  valorToken = "PROGRAM"
  valorInput = entrada[0]
 
  numero = 1 
  raiz = nodo('PROGRAM', numero)
  raiz.visitado = True


  while (df.at[valorToken,valorInput]) == (df.at[valorToken,valorInput]):
    data = (df.at[valorToken,valorInput]).split(" ",2)
    data = data.pop()
    data = data.split(" ")
    if data[0] != 'ε':
      ramas=[]
      for i in range(len(data)):
        Token = data.pop()
        ramas.append(Token)
        
        stack.append(Token)
      ramas.reverse()
      for i in ramas:
        numero = numero + 1
        raiz.insertS(i, numero)
    else:
      numero = numero + 1
      raiz.insertS(data[0],numero)
      raiz.visitarNodo()

    valorToken = stack.pop()
    raiz.visitarNodo()

    while valorToken == valorInput:
      entrada.remove(valorInput)
      if len(entrada) == 0:
        break
      raiz.visitarNodo()

      valorToken = stack.pop()
      valorInput = entrada[0]
    
    if len(entrada) == 0: 
      break
    if valorToken.islower():
      break

  raiz.Preorden()
  
  recordT(raiz)
  definir_ensamblador(raiz,'Prueba.txt')
  crear_grafico(raiz)



def hijosN(nodo, list1):
  for x in nodo.children: 
    if len(x.children)==0:
      list1.append( x.token)
      x.visitado=True
    else:
      x.visitado=True
      hijosN(x, list1)
  return list1

def findParents(nodo, principal):
  if nodo.padre.token=="PRINC":
    principal.append(0)
  elif nodo.padre.token=="FUNCS":
   principal.append(1)
  else:
    findParents(nodo.padre,principal)


def recordT(raiz):
  stack= return_tokens('Prueba.txt')       
  Visited=["F"] *len(stack) 
  list2=[]
  list3=[]
  nodos = []
  principal=[]
  principal2=[]
  simbolos2=[]
  nodos.append(raiz)
  while (len(nodos)):
    curr = nodos[0]
    nodos.pop(0)
    simbolos=[]
    curr.visitado= False
    if curr.token == "VAR_DECL":
      
      findParents(curr,principal)
      for x in curr.children: 
        if len(x.children)==0:
          simbolos.append(x.token)
        else:
          hijosN(x, list2)
          for i in list2:
            simbolos.append(i)
          list2.clear()
    elif curr.token == "ASSIG_VAR":
      findParents(curr,principal2)
      for x in curr.children: 
        if len(x.children)==0:
          simbolos2.append(x.token)
        else:
          hijosN(x, list3)
          for i in list3:
            simbolos2.append(i)
          list3.clear()

         

    if len(simbolos)>0:
      simbolos.remove('ε')

      stack= return_tokens('Prueba.txt') 
      temporal=[]
      linea=0
      for i in range(len(stack)):
        if (stack[i][0]==simbolos[0]) and (Visited[i]=="F"):
          linea=stack[i][2]
          break
          
      for d in range(len(stack)):
        if stack[d][2]==linea:
          temporal.append(stack[d][1])
          Visited[d]="T"

      symb=symbol(simbolos,linea,temporal,principal)
      
      coincidence=0
      if len(symbol_table)==0:
        symbol_table.append(symb)
      else:
        for i in reversed(symbol_table):
          if symb.lexema==i.lexema:
            print("Error semantico, linea", symb.valor)
            break
          else:
            coincidence=coincidence+1
        if coincidence>0:
          symbol_table.append(symb)

      principal.clear()

    for i in symbol_table:
      if i.padre==1:
        symbol_table.remove(i)  
          
    for t in symbol_table:
      for temp1 in range(len(t.token)):
        if t.token[temp1]=="id" and t.token[temp1+1]!="oper_asign":
          
          temp_var=0
          for temp2 in symbol_table:
            for temp3 in temp2.lexema:
              if t.lexema[temp1]==temp3 and t.valor!=temp2.valor:
                temp_var=temp_var+1
          if temp_var==0:
            rpta= "Error sintactico, variable " + t.lexema[temp1] +" no declarada"
            sys.exit(rpta) 
    
    for t1 in symbol_table:
      if t1.token[0]=='string':
        y='texto'
        for t2 in t1.token:
          if y!=t2:
            if t2=='number':
              print("Error de asignacion de variables")
              symbol_table.remove(t1)
      elif t1.token[0]=='integer':
        y='number'
        for t2 in t1.token:
          if y!=t2:
            if t2=='texto':
              print("Error de asignacion de variables")
              symbol_table.remove(t1)
      

    
    if len(simbolos2)>0 and len(symbol_table)>len(simbolos2):
      if 'ε' in simbolos2:
        simbolos2.remove('ε')
      temporal=[]
      linea=0
      
      for i in range(len(stack)):
        if (stack[i][0]==simbolos2[0]) and (Visited[i]=="F"):
          linea=stack[i][2]
          break
          
      for d in stack:
        if d[2]==linea:
          temporal.append(d[1])
      symb1=symbol(simbolos,linea,temporal,principal2)

      error=0
      for temporal in symbol_table:
        if temporal.lexema==symb1.lexema[0]:
          coincidence=0
          if len(symbol_table2)==0:
            symbol_table2.append(symb1)
          else:
            for i in reversed(symbol_table2):
              if symb.lexema==i.lexema:
                print("Error semantico, linea", symb1.valor)
                break
              else:
                coincidence=coincidence+1
            if coincidence>0:
              symbol_table2.append(symb1)
            principal2.clear()
            error=0
            break
        else:
          error=error+1
      if error>0:
        print("Error sintactico")
        simbolos2.clear()

    for i in symbol_table2:
      if i.padre==1:
        symbol_table2.remove(i)
    

    for it in reversed(curr.children): 
      nodos.insert(0,it)     
        
      
def Print_table():
  for i in symbol_table:
    print(i.token,i.lexema)


def crear_grafico(raiz): 
  g = graphviz.Digraph('G', filename='grafico.gv')
  nodos = []
  nodos.append(raiz)

  while (len(nodos)):
    curr = nodos[0]
    g.node(str(curr.valor), str(curr.token))
    nodos.pop(0)
    for it in range(len(curr.children)): 
      nodos.insert(0,curr.children[it])
      if curr.children[it].token.islower():
        g.node(str(curr.children[it].valor), str(curr.children[it].token), color='lightcoral')
      else:
        g.node(str(curr.children[it].valor), str(curr.children[it].token), color='lightblue')
      
      g.edge(str(curr.valor),str(curr.children[it].valor))
  g.view()


def definir_ensamblador(raiz, arc):
  inicio()
  stack= return_tokens(arc)   
  val=0 
  Visited=["F"] *len(stack) 
  nodos = []
  nodos.append(raiz)
  while (len(nodos)):
    curr = nodos[0]
    nodos.pop(0)
    if curr.token == "PRINC" and curr.visitado==False:
      main_i()

    if curr.token == "IF_STAT" and curr.visitado==False:
      token_encontrar2(curr, "IF_STAT",val,Visited,stack,0,[])   

    if curr.token == "VAR_DECL" and curr.visitado==False:
      val=val+1
      token_encontrar(curr, "VAR_DECL",val,Visited,stack,0,[])

    if curr.token == "ASSIG_VAR" and curr.visitado==False:
      val=val+1
      a=token_encontrar_2(curr, "VAR_DECL",val,Visited,stack)
      assig_var(a,stack,Visited,val,[])

    if curr.token == "FUN_DECL":
      temporal=[]
      lista=[]
      for x in curr.children: 
        if x.token=="BLOQUE":
          break
        else:
          if len(x.children)==0:
            temporal.append(x.token)  
          else:
            hijosN(x,lista)
            for i in lista:
              temporal.append(i)
            lista.clear()
      t=obtener_valores_func(temporal, stack,Visited,val)
      for x in curr.children:
        if x.token=="BLOQUE":
          nod=[]
          nod.append(x)
          while(len(nod)):
            curr1=nod[0]
            nod.pop(0)
            if curr1.token == "IF_STAT" and curr.visitado==False:
              token_encontrar2(curr1, "IF_STAT",val,Visited,stack,1,t)   

            if curr1.token == "VAR_DECL" and curr.visitado==False:
              val=val+1
              token_encontrar(curr1, "VAR_DECL",val,Visited,stack,1,t)

            if curr1.token == "RETURN_STAT":
              val=val+1
              a=token_encontrar_2(curr1, "RETURN_STAT",val,Visited,stack)
              obtener_valores_return(a, stack,Visited,val,t)

            if curr1.token == "ASSIG_VAR" and curr.visitado==False:
              val=val+1
              a=token_encontrar_2(curr1, "VAR_DECL",val,Visited,stack)
              assig_var(a,stack,Visited,val,t)
              

            curr.visitado=True
            for it in reversed(curr1.children): 
              nod.insert(0,it)
              
      fin_func(t)
      

    curr.visitado=True
    for it in reversed(curr.children): 
      nodos.insert(0,it)

  fin()
  

def token_encontrar_2(curr, token,val,Visited,stack):
  temporal=[]
  lista=[]

  for x in curr.children: 
    if len(x.children)==0:
      temporal.append(x.token)  
    else:
      hijosN(x,lista)
      for i in lista:
        temporal.append(i)
      lista.clear()
    x.visitado=True
  return temporal

def token_encontrar(curr, token,val,Visited,stack,padre,var):
  temporal=[]
  lista=[]

  for x in curr.children: 
    if len(x.children)==0:
      temporal.append(x.token)  
    else:
      hijosN(x,lista)
      for i in lista:
        temporal.append(i)
      lista.clear()
    x.visitado=True
  obtener_valores(temporal, stack,Visited,val,padre,var)

  
def token_encontrar2(curr, token,val,Visited,stack,padre,var):
  temporal=[]
  lista=[]
  
  for x in curr.children: 
    if x.token=="BLOQUE" or  x.token=="ELSE_STAT":
      pass
    else:
      if len(x.children)==0:
        temporal.append(x.token)  
      else:
        hijosN(x,lista)
        for i in lista:
          temporal.append(i)
        lista.clear()
    x.visitado=True
  obtener_valores_if(temporal, stack,Visited,val)
  
  for x in curr.children:
    if x.token=="BLOQUE":
      val=val+1
      token_encontrar(x, "VAR_DECL",val,Visited,stack,padre,var)
    elif x.token=="ELSE_STAT":
      break
  
  for x in curr.children:
    if x.token=="ELSE_STAT":
      obtener_valores_else()
      for y in x.children: 
        if y.token=="BLOQUE":
          val=val+1
          token_encontrar(y, "VAR_DECL",val,Visited,stack,padre,var)
  fin_else()
   
  fin_if()




if __name__=='__main__':
  parsing() 
  
 





