# -*- coding: utf-8 -*-
'''
    Este modulo contém as classes e metodos relacionados a API do REMEDY
'''

import sys
import os
from settings import *



REMEDY_JAVA_API_HOME=os.path.join( os.path.dirname( os.path.realpath(__file__) ), 'java_api' )


for jar in os.listdir(REMEDY_JAVA_API_HOME):
    if jar.endswith(".jar"): 
        sys.path.append(os.path.join(REMEDY_JAVA_API_HOME,jar))

from com.bmc.arsys.api import ARServerUser, ARException, Entry, Value



def cond(campo,operador,valor):
    if  type(valor) in [str, unicode]: return " '%s' %s \"%s\" " % (campo,operador,valor)
    else: return " '%s' %s %s " % (campo,operador,valor)
    
def AND(condicoes):
    return "(%s)" % ( " AND ".join( condicoes )  )
    
def OR(condicoes):
    return "(%s)" % ( " OR ".join( condicoes )  )  



class remedy(object):
    '''
        Esta classe contém os metodos que representam as operações realizados pelo Planejamento Open no Remedy
    '''
    
    def __init__(self):
        self.ars = ARServerUser(REMEDY_USERNAME, REMEDY_PASSWORD, '', REMEDY_SERVER)
        self.ars.setPort(REMEDY_TCP_PORT)
    
    def __enter__(self):
        try:
            self.ars.login()
        except ARException, e:
            print(e)
            sys.exit(1)
        return self

    def __exit__(self, type, value, traceback):
        self.ars.logout()
    
 
    def query(self,form_name,query,*args):
        #'''
        #    form_name=nome do formulário 
        #    query = string de consulta semelhante a SQL utilizado para localizar as Entry. Exemplo  '1'="INC000000123"
        #    *args = campos a serem adicionados nas Entries retornadas
        #    Retorna:
        #        uma lista contendo as Entries dos chamados designados ao grupo do Planejamento Open
        #'''
        entry_info_list = []
        
        qual = self.ars.parseQualification(form_name,query)
        stop = False
        start = 0
        query_range = 50
        while stop == False:
            try:
                result_list = self.ars.getListEntry(form_name, qual, start,query_range , None, None, False, None)
            except ARException, e:
                print e
                self.ars.logout()
                sys.exit(1)
            if len(result_list) > 0:
                [entry_info_list.append(x) for x in result_list]
                start = query_range
                query_range = query_range + query_range
            else:
                stop = True
        entry_list = []
        for entry_info in entry_info_list:
            try:
                if len(args) > 0:
                    entry = self.ars.getEntry(form_name,entry_info.getEntryID(),*args)
                else:
                    entry = self.ars.getEntry(form_name,entry_info.getEntryID(),None)
            except ARException, e:
                print e
                self.ars.logout()
                sys.exit(1)
            entry_list.append(entry)
        return entry_list
 
    def query_entry(self,form_name,field_id,field_value):
        '''
            Recebe como parameros:
                form_name = str contendo o nome do form no remedy
                field_id = int contendo o id do field utilizado na query
                field_value = valor do field utilizado na query
            Retorna:
                primeira EntryInfo encontrada 
        '''
        query = u"'%s' %s %s%s%s" % (unicode(field_id),u"LIKE",'"%',unicode(field_value),'%"')
        try:
            qual = self.ars.parseQualification(form_name,query)
        except ARException, e:
            print(e)
            sys.exit(1)
        try:
            return self.ars.getListEntry(form_name, qual, 0, 1, None, None, False, None)[0]
        except IndexError:
            return None
            
            
    def update(self,form_name,query_field, query_value,*args):
        #'''
        #    Recebe como parametros:
        #        form_name = string com o nome do formulario
        #        query_field = id do campo que será usado na busca da Entry
        #        query_value = valor do campo do campo  usa na busca da Entra
        #        *args = lista de  tuplas (id do campo a ser alterado, valor a ser atribuido)
        #'''

        #result= self.query(form_name,"'%s'=\"%s\" " % (query_field, query_value) )
        result= self.query_entry(form_name,query_field, query_value)
        
        entry_id = result.getEntryID()
        entry = Entry()
        for campo,valor in args:
            entry.put(campo,Value(valor))
        try:
            self.ars.setEntry(form_name, entry_id, entry, None, 0)
        except ARException, e:
            print(e)
            self.ars.logout()
            sys.exit(1)

 
 
def main():
    pass
   
if __name__ == "__main__":
    main()