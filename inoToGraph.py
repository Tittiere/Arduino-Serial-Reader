import matplotlib.pyplot as plt                                                                                                         #importo le libs che mi serviranno
from datetime import datetime
import serial
import time
import os

def checkArdInfoExist():                                                                                                                #controllo se esiste il file con i dati relativi ad arduino
    corrotto = False                                                                                                                    #var per controllare che il file con i dati sia ok
    try:
        ardInfo = open('ardInfo.txt', 'r')                                                                                              #provo ad aprire il file in lettura
        infos = ardInfo.read()
        lista = infos.split('\'')                                                                                                       #splitto la stringa letta                                                                                                                     #prendo solo i valori che mi interessano
        infos = []
        try:
            for i in range(1, len(lista), 2):
                infos.append(lista[i])
            ardInfo.close()
            print('Porta seriale = ' + str(infos[0]) + ' baudrate = ' + str(infos[1]) + ' numero dati = ' + str(infos[2] + '\nNomi dei dati:'))
            for i in range(3, len(infos), 1):
                print(infos[i])
        except IndexError:                                                                                                              #evito che il programma crashi se trova il file dati vuoto/con testo a caso
            ardInfo.close()
            print('Le vecchie informazioni non sono più disponibili, inseriscine di nuove')
            corrotto = True
        if corrotto == True:
            esiste = True
            infos = ardGetData(esiste)                                                                                                  #se si le chiedo con funzione e le ottengo
            ardInfo = open('ardInfo.txt', 'w')                                                                                          #apro il file in scrittura
            ardInfo.write(str(infos))                                                                                                   #scrivo le informazioni appena ottenute
            ardInfo.close()
        else:
            answ = input('Vuoi cambiare le info della scheda arduino?\n(Y/N)\n')                                                            #chiedo se si vuole cambiare infos
            if answ == 'y' or answ == 'Y':
                esiste = True
                infos = ardGetData(esiste)                                                                                                  #se si le chiedo con funzione e le ottengo
                ardInfo = open('ardInfo.txt', 'w')                                                                                          #apro il file in scrittura
                ardInfo.write(str(infos))                                                                                                   #scrivo le informazioni appena ottenute
                ardInfo.close()                                                                                                             #chiudo il file
            else:
                ardInfo = open('ardInfo.txt', 'r')                                                                                          #se no le leggo dal file già esistente
                infos = ardInfo.read()
                lista = infos.split('\'')                                                                                                   #splitto la stringa letta
                infos = []                                                                                                                  #prendo solo i valori che mi interessano
                for i in range(1, len(lista), 2):
                    infos.append(lista[i])
                ardInfo.close()
    except FileNotFoundError:
        esiste = False
        infos = ardGetData(esiste)
        ardInfo = open('ardInfo.txt', 'w')                                                                                              #se non esiste lo apro in scrittura
        ardInfo.write(str(infos))                                                                                                       #scrivo le informazioni appena ottenute
        ardInfo.close()
    return infos
        
def ardGetData(esiste):
    infos = []                                                                                                                          #lista a cui saranno attribuiti i valori finali       
    aus = input('Su che porta seriale è collegato arduino? (Es.: \'COM7\')\n')                                                          #chiedo la seriale
    while True:                                                                                                                         #controllo se la seriale è un valore accettabile
        if aus.startswith('com') == False and aus.startswith('COM') == False or (len(aus) != 4 and len(aus) != 5) or aus[-1].isdigit() == False:
            aus = input('La porta inserita non è valida. Inserisci una porta simile a \'COM7\'\n')
        else:
            infos.append(aus)                                                                                                           #se il valore è accettabile allora lo salvo
            break
    aus = input('Inserisci la baudrate della scheda arduino: (Es.: \'9600\')\n')                                                        #chiedo la baudrate
    while True:
        if aus.isdigit() == False:                                                                                                      #controllo che sia un numero
            aus = input('Il numero inserito non è valido.\nInserisci una baudrate valida come \'9600\':\n')
        else:
            infos.append(aus)                                                                                                           #aggiungo il valore alla lista
            break
    aus = input('Inserisci il numero di dati che il programma dovrà leggere\n')                                                         #chiedo il numero di dati
    while True:
        if aus.isdigit() == False or float(aus) <= 0:                                                                                   #controllo che sia un numero
            aus = input('Il numero inserito non è valido.\nInserisci un numero valido\n')
        else:
            infos.append(aus)                                                                                                           #aggiungo il valore alla lista
            break
    print('Inserisci i nomi in ordine dei dati che vuoi stampare')                                                                      #chiedo i nomi dei dati
    if int(infos[2]) == 1:
        aus = input('Inserisci il nome della variabile\n')
        infos.append(aus)
    else:
        for i in range(int(infos[2])):
            aus = input('Inserisci il nome della variabile numero ' + str(i+1) + '\n')
            infos.append(aus)
    return infos                                                                                                                        #ritorno l'array di valori

def main():
    infos = checkArdInfoExist()
    arduino = serial.Serial(infos[0], baudrate = int(infos[1]), timeout = 0.01)                                                         #dichiaro porta di arduino, baudrate e timeout (ogni quanto controllo la seriale)
    values = []                                                                                                                         #array per i valori di arduino
    tempo = []                                                                                                                          #array per i valori del tempo
    pureData = []                                                                                                                       #dato puro da aggiungere alla matrice finale
    tZero = time.time()                                                                                                                 #tempo di inizio del programma
    ora = datetime.now()                                                                                                                #data e ora da segnarmi nel file dove salvo i dati
    firstdata = False                                                                                                                   #inizializzo la variabile che mi indicherà se è stato registrato il primo dato numerico
    f = open('dati.txt', 'a')                                                                                                           #creo o apro il file dei dati
    f.write(str(ora))                                                                                                                   #segno data ed ora
    f.close()                                                                                                                           #chiudo il file
    print('Inizio a leggere il monitor seriale...\nCtrl+c per stoppare e mostrare il grafico')
    try:
        while True:                                                                                                                     #ciclo che controlla la seriale
            arduinoData = arduino.readline()                                                                                            #leggo la riga
            try:
                decodedValue = str(arduinoData[0:len(arduinoData)].decode("utf-8"))                                                     #traduco il dato appena letto
            except UnicodeDecodeError:                                                                                                  #se il dato è nullo evito che il programma crashi
                pass
            spltValue = decodedValue.split('*')                                                                                         #splitto il dato per avere solo quello
            pureData = []                                                                                                               #inizializzo la variabile per l'array finale di dati
            try:
                if firstdata == False:                                                                                                  #se il primo dato non è ancora stato registrato resetto il timer
                    tZero = time.time()
                prova = spltValue[1]                                                                                                    #provo a causare un IndexError così da controllare se il dato è numerico o meno
                for j in range(1, len(spltValue)-1, 1):                                                                                 #se il dato è accettabile allora salvo solo la parte numerica di esso in un vettore
                    try:
                        pureData.append(float(spltValue[j]))                                                                            #aggiungo il valore come float
                    except ValueError:                                                                                                  #se c'è un backslash nella stringa sfuggito a split lo tolgo
                        aus = spltValue[j].split('\'')
                        pureData.append(float(aus[1]))
                values.append(pureData)                                                                                                 #appendo il vettore finale alla matrice di dati
                if firstdata == False:                                                                                                  #qui il dato è stato registrato, quindi, se non l'ho fatto, lo segno nella variabile
                    firstdata = True
                aus = time.time()-tZero
                aus = "{:.3f}".format(aus)                                                                                              #arrotondo il tempo ai millesimi di secondo
                tempo.append(float(aus))                                                                                                #segno il tempo in cui ricevo il dato
            except IndexError:
                x = "haha x go brr"
    except KeyboardInterrupt:                                                                                                           #quando l'utente ferma il programma con ctrl+c eseguo il seguente
        dati = open('dati.txt', 'a')                                                                                                    #apro il file dei dati
        dati.write('\nLista di tempi:\t\t\tLista dei dati:\n')                                                                          #scrivo nel file tempo e dato
        i = 1
        while i <= len(tempo):                                                                                                          #scrivo i dati e il tempo con un format sensato
            dati.write(str(i) + '. ' + str(tempo[i-1]) + '\t\t\t' + str(values[i-1]) + '\n')
            i += 1
        
        dati.close()                                                                                                                    #chiudo il file
        
        filename = open('tempo.txt', 'a')
        filename.write(str(ora) + '\n\n')
        for k in range(len(tempo)):
            temp = str(tempo[k]).split('.')
            temp = ','.join(temp)
            filename.write(str(temp) + '\n')
        filename.close()

        for i in range(int(infos[2])):                                                                                                  #ciclo per far vedere tutti i grafici in caso siano più di uno
            aus = []
            for j in range(len(tempo)):                                                                                                 #ciclo per trasferire il valore dalla matrice ad un vettore apposito
                aus.append(values[j][i])
            aus2 = []
            for k in range(len(aus)):
                temp = str(aus[k]).split('.')
                temp = ','.join(temp)
                aus2.append(temp)
            filename = open(infos[i+3] + '.txt', 'a')
            filename.write(str(ora) + '\n\n')
            for k in range(len(aus2)):
                filename.write(aus2[k] + '\n')
            filename.close()
            plt.plot(tempo, aus)                                                                                                        #faccio il grafico con tempo su x e valori su y
            plt.xlabel('Tempo (s)')                                                                                                     #nomi degli assi
            plt.ylabel(infos[i+3])
            plt.title('Grafico tempo/' + str(infos[i+3]))                                                                               #nome del grafico
            plt.show()                                                                                                                  #faccio vedere il grafico

            #ATTENZIONE!! I GRAFICI VENGONO FATTI VISUALIZZARE AD UNO AD UNO, CHIUDERE UN GRAFICO PER MOSTRARE QUELLO SUCCESSIVO
main()