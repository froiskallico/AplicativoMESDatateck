#!/usr/bin/python
# coding=UTF-8

#importando biblioteca
import sqlite3
import time

# conectando...
conn = sqlite3.connect('TESTEPDS.db')
#Definindo um cursor
cur = conn.cursor()

print ("\n" * 500)
print ("Teste de Atendimento Automatico de PDS e recebimento de sinal de entrada")
print ("\n" * 3)

while True:
    user_choice = input("Ola, o que deseja: [C]adastrar | [D]eletar? | [O]perar | [V]isualizar?  ")
    user_choice = user_choice.lower()

    def cadastro():
        print ("\n --- CADASTRO --- \n")
        reqnum = int(input("Numero da Requisicao: "))
        pd = int(input("Numero do PD: "))
        qtd = int(input("Quantidade do PD: "))
        prioridade = int(input("Prioridade: "))
        string_cadastro = reqnum, pd, qtd, 0, 0, 0, prioridade
        cur.execute("INSERT INTO pds (REQNUM, PD, QTD, QTD_CORT, CRT_FINAL, QTD_ATD, PRIOR) VALUES " + str(string_cadastro) + ";")

    def deleta():
        print ("\n --- DELETAR --- \n")
        pd = int(input("Digite o item a Deletar: "))
        cur.execute("DELETE FROM pds WHERE ID = " + str(pd))

    def operar():
        print ("\n --- OPERAR --- \n")
        cur.execute("SELECT ID, REQNUM, PD, QTD, QTD_CORT FROM pds WHERE PRIOR = (SELECT MIN(PRIOR) FROM pds WHERE QTD_CORT < QTD)")
        prioridade = cur.fetchone()
        pd_id = prioridade[0]
        reqnum = prioridade[1]
        pd = prioridade[2]
        qtd = prioridade[3]
        qtd_cortado = prioridade[4]

        print ("ID em corte: ", pd_id)
        print ("Requisicap em corte: ", reqnum)
        print ("PD em corte: ", pd)
        print ("Quantidade a cortar: ", qtd)
        print ("Quantidade cortada: ", qtd_cortado)

        start = input("Deseja iniciar o corte [S] ou [N]? ")
        start.lower()
        if start == 's':
            print ("START!")
            while qtd_cortado < qtd:
                try:
                    time.sleep(0.5)
                    qtd_cortado += 1
                    cur.execute("UPDATE pds SET QTD_CORT = %s WHERE ID = %s;" % (qtd_cortado, pd_id))
                    conn.commit()
                    time.sleep(0.05)
                    print ("Qtd cortada: %04d" % qtd_cortado)                  
                    
                except KeyboardInterrupt:
                    print ("Você interrompeu a execucao")
                    visualiza()
                    time.sleep(3)
                    break
            else:
                cur.execute("UPDATE pds SET CRT_FINAL = 1 WHERE ID = %s;" % (pd_id))
                
    def visualiza():
        #Print header.
        cur.execute("SELECT * from pds;")
        names = [description[0] for description in cur.description]

        for name in names:
            print ('%-14s' % name, end='|')
        print("")
        for name in names:
            print ("-" * 14 + "|", end="")
        print("")
        for linha in cur.fetchall():
            for campo in linha:
                print ("%-14s" % campo, end="|")
            print ("")
    if user_choice == "c":
        cadastro()
    elif user_choice == "d":
        deleta()
    elif user_choice == "o":
        operar()
    elif user_choice == "v":
        visualiza()
    
    conn.commit()
    
conn.close()
