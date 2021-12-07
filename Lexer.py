
import ply.lex as lex


reserved = {
    'si' : 'if',
    'entonces' : 'else',
    'mientras' : 'while',
    'Detente' : 'break',
    'gimnasio': 'class',
    'regresa' : 'return',
    'cierto' : 'true',
    'falacia' : 'false',
    'llama' : 'func',
    'y' : 'and',
    'o' : 'or',
    'es': 'is',
    'entero' : 'integer',
    'letra' : 'character',
    'palabra' : 'string',
    'boleano' : 'boolena',
    'pokebola' : 'main',
    'obten' : 'input',
    'habla' : 'output',
    'trata':'try',
    'captura': 'catch',
    'entrenador' : 'funtion',
    'yo_te_elijo' : 'print'
}
 
tokens = ('comment_init',
'comment_fin',
'id',
'char',
'number',
'oper_suma',
'oper_dif',
'oper_div',
'oper_mult',
'oper_asign',
'oper_mod',
'oper_mayor',
'oper_menor',
'oper_identico',
'oper_diferente',
'oper_neg',
'oper_mayorigu',
'oper_menorigu',
'par_init',
'par_fin',
'key_init',
'key_fin',
'corch_init',
'corch_fin',
'comma',
'texto', 'break_line') + tuple(reserved.values()) #

t_comment_init = r'snorlax/'
t_comment_fin = r'/snorlax'

t_oper_identico = r'=='
t_oper_mayorigu = r'>='
t_oper_menorigu = r'<='
t_oper_diferente = r'\!=' 
t_oper_suma = r'\+'
t_oper_dif = r'-'
t_oper_mult = r'\*'
t_oper_div = r'/'
t_par_init = r'\('
t_par_fin = r'\)'
t_oper_asign = r'='
t_oper_mod = r'%'
t_oper_mayor = r'>'
t_oper_menor = r'<'
t_oper_neg = r'\!'
t_key_init = r'{'
t_key_fin = r'}'
t_corch_init = r'\['
t_corch_fin = r'\]'
t_comma = r','
t_break_line = r'\;'

entrada = [] 

def t_texto(t):
  r'"([^\\"]|\\")*"'
  t.type = reserved.get(t.value,'texto')   
  return t

def t_char(t):
     r'\|([^\\"]|\\")\|'
     t.type = reserved.get(t.value,'char')   
     return t

def t_id(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'id')   
     return t

def t_number(t):
  r'\d+'
  t.value = int(t.value) 
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
  print("Illegal character ’ %s’" % t.value[0])
  t.lexer.skip(1)

def find_column(input, token):
  line_start = input.rfind('\n', 0, token.lexpos) + 1
  return (token.lexpos - line_start) + 1

lexer = lex.lex()



def return_tokens(file):
  tokens=list()
  f = open(file, 'r')
  mensaje = f.read()
  f.close()
  lexer.input(mensaje)
  while True:
    tok = lexer.token()
    if not tok:
      break 
    tokens.append([tok.type, tok.value, tok.lineno, tok.lexpos])
    entrada.append(tok.type);

  return tokens