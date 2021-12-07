def inicio():
  file = open("ensamblador.s", "w")
  file.write(".data\n\n\n.text\n")
  file.close()
  
def main_i():
  file = open("ensamblador.s", "a")
  file.write("\nmain:\n\n")
  file.close()
  
def fin():
  file = open("ensamblador.s", "a")
  file.write("\njr $ra")

def obtener_valores_func(simbolos, stack,Visited,val):
  if 'ε' in simbolos:
    simbolos=list(filter(('ε').__ne__, simbolos))
  temporal=[]
  for i in range(len(stack)):
    if (stack[i][0]==simbolos[0]) and (Visited[i]=="F"):
      for ii in range(len(simbolos)):
        temporal.append(stack[i+ii][1])
        Visited[ii]="T"
      break
  t=func_ensamblador(simbolos, temporal,val)
  return t


def fin_func(temp):
  file = open("ensamblador.s", "a")
  file.write("\nlw $ra 4($sp)\naddiu $sp $sp "+str(4*len(temp) + 8)+"\nlw $fp 0($sp)\njr $ra\n\n")

def func_ensamblador(simbolos, temporal,val):
  temp=[]
  for i in range(len(simbolos)):
    if simbolos[i] =="id" and i>1:
      temp.append(temporal[i])
    if simbolos[i] =="par_fin":
      break
  file = open("ensamblador.s", "a")
  file.write("\nlabel_"+str(temporal[1])+":\n")
  file.write("\nmove $fp $sp\nsw $ra 0($sp)\naddiu $sp $sp -4\n\n")
  return temp
  
  
def obtener_valores_return(simbolos, stack,Visited,val,var):
  if 'ε' in simbolos:
    simbolos=list(filter(('ε').__ne__, simbolos))
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

  ens_return(simbolos, temporal,var)

def ens_return(simbolos, temporal, var):
  file = open("ensamblador.s", "a")
  if len(temporal)==3:
    if temporal[2].isdigit()==True:
      file.write("\nli $a0," +str(temporal[2])+"\n\n")
    else:
      for i in range(len(var)):
        if var[i]== temporal[2]:
          file.write("\nlw $a0, "+str(8+(4*i))+"($sp)\nsw $a0, 0($sp)\naddiu $sp $sp -4\n\n")
      if len(var)==0:
        file.write("la $t0, var_"+temporal[2]+"_fun\nlw $a0, 0($t0)\nsw $a0, 0($sp)\naddiu $sp, $sp, -4")
  else:
    temp=separar(simbolos,temporal)
    tempS=separar_simb(simbolos,temporal)
    suma(temp,tempS,var)
  



def obtener_valores(simbolos, stack,Visited,val,padre,var):
  if 'ε' in simbolos:
    simbolos=list(filter(('ε').__ne__, simbolos))
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

  tabla_temp= separar(simbolos,temporal)
  tempS=separar_simb(simbolos,temporal)
  definir_valor(val, temporal[1], padre)
  if len(tabla_temp)==1:
    asignar_valor(tabla_temp)
  else:
    suma(tabla_temp,tempS, var)
  reserva_variable(-1,temporal[1],padre)
  
def separar_simb(s,t):
  temporal=[]
  for i in range(len(s)):
    if s[i]!='number' and s[i]!='id' and i!=(len(s)-1) and s[i]!='return' and s[i]!='oper_asign' and s[i]!='par_init' and s[i]!='par_fin'and s[i]!='key_init' and s[i]!='key_fin':
      temporal.append(t[i])
    elif s[i]=='id' and s[i+1]=='oper_identico':
      pass
  return temporal


def separar(s,t):
  temporal=[]
  for i in range(len(s)):
    if s[i]=='number':
      temporal.append(t[i])
    elif s[i]=='id' and s[i+1]!='oper_identico':
      temporal.append(t[i])
  return temporal

def obtener_valores_else():
  file = open("ensamblador.s", "a")
  file.write("\nlabel_false:\n")

def fin_else():
  file = open("ensamblador.s", "a")
  file.write("\nb label_end\n")

def fin_if():
  file = open("ensamblador.s", "a")
  file.write("\nlabel_end:\n")

def obtener_valores_if(simbolos, stack,Visited,val):
  if 'ε' in simbolos:
    simbolos=list(filter(('ε').__ne__, simbolos))
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


  e_1=temporal[2]
  e_2=temporal[4]
  operador=temporal[3]
  if_ens(e_1,e_2,operador)
  

  return temporal 

  
def if_ens(e_1,e_2,operador):
  file = open("ensamblador.s", "a")
  if str(e_1).isdigit()==True:
    file.write("li $a0, "+str(e_1)+"\nsw $a0, 0($sp)\nadd $sp, $sp, -4\n\n")
  else:
    file.write("la $t0, var_"+str(e_1)+"\nlw $a0, 0($t0)\nsw $a0, 0($sp)\nadd $sp, $sp, -4\n\n")

  if str(e_2).isdigit()==True:
    file.write("li $a0, "+str(e_2)+"\nsw $a0, 0($sp)\nadd $sp, $sp, 4\n\n")
  else:
    file.write("la $t0, var_"+str(e_2)+"\nlw $a0, 0($t0)\nsw $t1, 0($sp)\nadd $sp, $sp, 4\n\n")

  if operador=="<":
    file.write("blt $a0, $t1, label_true\nlabel_true:\n")
  elif operador==">":
    file.write("bgt $a0, $t1, label_true:\nlabel_true:\n")
  elif operador=="==":
    file.write("beq $a0, $t1, label_true\nlabel_true:\n")
  elif operador==">=":
    file.write("bge $a0, $t1, label_true\nlabel_true:\n")
  elif operador=="<=":
    file.write("ble $a0, $t1, label_true\nlabel_true:\n")
  elif operador=="!=":
    file.write("bne $a0, $t1, label_true\nlabel_true:\n")


  



def definir_valor(val,id, padre): 
  with open('ensamblador.s', 'r') as file:
    data = file.readlines()
  
  if padre==0:
    data[val] = "var_"+str(id)+": .word 0:1\n\n"
  else:
    data[val] = "var_"+str(id)+"_fun: .word 0:1\n\n"

  with open('ensamblador.s', 'w') as file:
    file.writelines(data)
  

def reserva_variable(val,id,padre):
  with open('ensamblador.s', 'r') as file:
    data = file.readlines()
  if padre==0:
    data[val] = "la $t0, var_"+str(id)+"\nsw $a0, 0($t0)\n\n"
  else:
    data[val] = "la $t0, var_"+str(id)+"_fun\nsw $a0, 0($t0)\n\n"
  with open('ensamblador.s', 'w') as file:
    file.writelines(data)

def asignar_valor(valor):
  file = open("ensamblador.s", "a")
  file.write("\nli $a0, "+str(valor[0])+"\n\n")


def suma(valores, simb,var):
  file = open("ensamblador.s", "a")
  for i in range(len(valores)-1):
    if str(valores[i]).isdigit()==False:
      if len(var)==0:
        file.write("la $t0, var_"+str(valores[i])+"\nlw $a0, 0($t0)\nsw $a0, 0($sp)\naddiu $sp, $sp, -4\n")
      else:
        for i in range(len(var)):
          if valores[i]==var[i]:
            file.write("\nlw $a0, "+str(8+(4*i))+"($sp)\nsw $a0, 0($sp)\naddiu $sp $sp -4\n")
    else:
      file.write("\nli $a0," +str(valores[i])+"\nsw $a0 0($sp)\naddiu $sp $sp-4\n")
      

  if str(valores[-1]).isdigit()==False:
      if len(var)==0:
        file.write("la $t0, var_"+str(valores[-1])+"\nlw $a0, 0($t0)\nsw $a0, 0($sp)\naddiu $sp, $sp, 4\n")
      else:
        for i in range(len(var)):
          if valores[i]==var[i]:
            file.write("\nlw $a0, "+str(8+(4*i))+"($sp)\nsw $a0, 0($sp)\naddiu $sp $sp -4\n")
  else:
    file.write("\nli $a0," +str(valores[-1])+"\n")

  for i in range(len(simb)):
    file.write("\nlw $t1 4($sp)\n\n")
    if simb[len(simb)-(1+i)]==str("+"):
      file.write("\n\nadd $a0 $t1 $a0\n\n")
    elif simb[len(simb)-(1+i)]==str("-"):
      file.write("\n\nsub $a0 $t1 $a0\n\n")
    file.write("addiu $sp $sp 4\n")
    
  file.close()


def assig_var(simbolos, stack,Visited,val,var):
  if 'ε' in simbolos:
    simbolos=list(filter(('ε').__ne__, simbolos))
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

  tabla_temp= separar(simbolos,temporal)
  tempS=separar_simb(simbolos,temporal)
  file = open("ensamblador.s", "a")
  if len(tempS)==0 and len(tabla_temp)==2:
    file.write("\nli $a0, "+str(tempS[1])+"\n\n")
  elif len(tempS)>0:
    suma(tabla_temp,tempS,var)
  elif len(tempS)==0 and len(tabla_temp)>2:
    file.write("\nsw $fp 0($sp)\naddiu $sp $sp-4\n")
    for i in range(2,len(tabla_temp)):
      if str(i).isdigit()==True:
        file.write("\nli $a0, "+str(tabla_temp[i])+"\nsw $a0 0($sp)\naddiu $sp $sp -4\n\n")
      else:
        file.write("\nla $t0, var_"+str(tabla_temp[i])+"\nlw $a0, 0($t0)\nsw $a0, 0($sp)\naddiu $sp, $sp, -4n\n\n")
    
    file.write("jal label_"+str(tabla_temp[1])+"\n\n")

