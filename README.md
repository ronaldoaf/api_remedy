# api_remedy
Uma aplicação do API do  Remedy (ITSM) em Python. Utilizando o Jython


## Configuração
Alterar o arquivo ```remedy/settings.py``` preenchendo as seguintes variáveis: 


```python
#usuario do remedy
REMEDY_USERNAME =  u"usuario"

#senha do usuário do remedy 
REMEDY_PASSWORD = u"senha"

# nome ou ip do servidor
REMEDY_SERVER = u"x.x.x.x"   

#porta tcp do servidor remedy 
REMEDY_TCP_PORT = 9000 
```

## Exemplo de uso

```bash
java -jar jython.jar teste.py
```


### arquivo teste.py
```python
# -*- coding: utf-8 -*-

from remedy import remedy
from remedy.fields import HelpDeskFields as INC




#-----Exemplo de QUERY------------------------------------------------------------------------------


#Define um novo objeto chamado "r" que é instância da classe "remedy"
with remedy() as r:

	#Lista de campos que serão mostrados
	fields=[
		INC.incident_number,
		INC.short_description,
		INC.assigned_group
		]

	#Utiliza o metódo "query" para pesquisar o incidente
	#Argumentos:
	#	-> Nome do formulário
	#	-> String de consulta no formato:  ('campo' operador "valor") and ...
	#	-> Lista de campos a serem mostradods [campo1, campo2, ... ] todos númericos
    regs=r.query(INC.form_name,"'%s'=\"INC000001234567\" " % ( INC.incident_number ), fields )
    
	
	#Para cada registro encontrado
	for reg in regs:
		#Exibe os campos 'Incident Number' e 'Short Description'
		print reg[INC.incident_number], reg[INC.short_description]





#-----Exemplo de UPDATE ----------------------------------------------------------------------------

#Define um novo objeto chamado "r" que é instância da classe "remedy"
with remedy() as r:
	#Lista de tuplas (campo, novo_valor)
	fields=[
		( INC.short_description, u"Nova descrição" )
		]
	
	#Utiliza o metódo "update" para atualizar o incidente
	#Argumentos:
	#	-> Nome do formulário
	#	-> Campo chave 
	#   -> Valor do campo chave
	#	-> #Lista de tuplas (campo, novo_valor) dos campos que serão atualizados
    regs=r.update(INC.form_name,INC.incident_number, "INC000001234567", *fields )

```
