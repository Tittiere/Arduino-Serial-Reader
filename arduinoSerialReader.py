import matplotlib.pyplot as plt
from datetime import datetime
import serial, time, json, os

path = os.path.dirname(os.path.realpath(__file__))
jsonPath = path + '\\config.json'
readmePath = path + '\\_README.txt'
config = {}

def loadJson():
    global config
    try:
        with open(jsonPath) as config_file:
            config = json.load(config_file)
        exit = False
    except:
        noJson()
        exit = True
    return exit

def updateJson():
    global config
    with open(jsonPath, 'w') as config_file:
        json.dump(config, config_file, indent=4)

def noJson():
    global config
    config['ardData'] = {
        'serialPort': 'e.g.: COM7',
        'baudrate': 'e.g.:9600',
    }
    config['dataNumber'] = 'number of individual data sent by arduino every time' 
    config['separator'] = 'the separator between the different types of data sent by arduino at a time (e.g.: \'*\')'
    config['dataNames'] = ['name1', 'name2', 'etc']
    config['numberFormat'] = 'EN for number format whith decimal dot like 1.15 or IT for number format with decimal comma like 1,15. If you want to paste the data in excel make sure to use the correct format.'
    content = '''To run the program, either fill in the config.json\nfile in this directory or restart the program and it\nwill let you input the data. If you have more than\none piece of data at a time, use aseparator like "*"\nto separate data, for example: *21.4*-12.3*0.01*\nRemember to choose the correct data format if you want\nto paste data to an excel file\ngithub.com/claristorio\n'''
    updateJson()
    file = open(readmePath, 'w')
    file.write(content)
    file.close()

def validData():
    global config
    aus = config['ardData']['serialPort']
    while True:
        if aus.startswith('com') == False and aus.startswith('COM') == False or (len(aus) != 4 and len(aus) != 5) or aus[-1].isdigit() == False:
            aus = input('The port is not valid. It must be similar to \'COM7\'\n')
        else:
            config['ardData']['serialPort'] = aus
            break

    aus = config['ardData']['baudrate']
    while True:
        if aus.isdigit() == False or int(aus) <= 0:
            aus = input('The baudrate value is not valid.\nInsert a valid baudrate, like \'9600\':\n')
        else:
            config['ardData']['baudrate'] = aus
            break

    aus = config['dataNumber']
    while True:
        if aus.isdigit() == False or int(aus) <= 0:
            aus = input('The number of data is not a valid number.\nInsert a valid number, like \'2\':\n')
        else:
            config['dataNumber'] = aus
            break
    if int(config['dataNumber']) > 1:
        aus = config['separator']
        while True:
            if aus == '-':
                aus = input('The separator cant be \'-\' because it could be confused whith minus\n')
            elif aus == "the separator between the different types of data sent by arduino at a time (e.g.: '*')":
                aus = input('Please, insert a character that will separate the data from arduino, such as \'*\'\n')
            else:
                config['separator'] = aus
                break
    else:
        config['separator'] = 'not needed'
    
    num = int(config['dataNumber'])
    lenNames = len(config['dataNames'])
    if num != lenNames:
        if num < lenNames:
            excess = lenNames - num
            print(f'The data names exceed by {excess} the number of data you entered.\nType the number of the name you want to remove')
            for i in range(excess):
                for i in range(lenNames):
                    print(str(i+1) + '. ' + config['dataNames'][i])
                aus = input()
                while True:
                    if aus.isdigit() == False or int(aus) > lenNames or int(aus) < 1:
                        print('The number you selected is not valid\nInsert a valid number, choose from the list:')
                        for i in range(lenNames):
                            print(str(i+1) + '. ' + config['dataNames'][i])
                        aus = input()
                    else:
                        break
                aus = config['dataNames'].pop(int(aus)-1)
                print(f'removed \'{aus}\'')
                if i != (excess-1) and excess != 1:
                    print('Select another element to remove from the list')
                lenNames = len(config['dataNames'])
        elif num > lenNames:
            defect = num - lenNames
            print(f'The data names are less than the number of data. ({defect} missing)')
            for i in range(defect):
                if defect == 1:
                    aus = input('Insert the missing data name\n')
                    config['dataNames'].append(aus)
                else:
                    aus = input(f'Insert the data name number {lenNames+i+1}\n')
                    config['dataNames'].append(aus)

    aus = config['numberFormat']
    if aus != 'EN' and aus != 'IT':
        aus = input('The number format is not valid.\nChoose a number format, 1 for EN or 2 for IT\n')
        while True:
            if aus.isdigit() == False and int(aus) != 1 and int(aus) != 2 :
                aus = input('The number format is not valid.\nChoose a number format, 1 for EN or 2 for IT\n')
            elif int(aus) == 1:
                config['numberFormat'] = 'EN'
                break
            elif int(aus) == 2:
                config['numberFormat'] = 'IT'
                break

    updateJson()

def autoConfigFirstTime():
    aus = input('Insert the serial port (e.g.: COM7)\n')
    while True:
        if aus.startswith('com') == False and aus.startswith('COM') == False or (len(aus) != 4 and len(aus) != 5) or aus[-1].isdigit() == False:
            aus = input('The port is not valid. It must be similar to \'COM7\'\n')
        else:
            config['ardData']['serialPort'] = aus
            break

    aus = input('Insert the baudrate (e.g.:9600)\n')
    while True:
        if aus.isdigit() == False or int(aus) <= 0:
            aus = input('The baudrate value is not valid.\nInsert a valid baudrate, like \'9600\':\n')
        else:
            config['ardData']['baudrate'] = aus
            break

    aus = input('Insert the number of data to be read at a time, for example 3\n')
    while True:
        if aus.isdigit() == False or int(aus) <= 0:
            aus = input('The number of data is not a valid number.\nInsert a valid number, like \'2\':\n')
        else:
            config['dataNumber'] = aus
            break
    if int(config['dataNumber']) > 1:
        aus = input('Insert the separator between every type of data\n')
        while True:
            if aus == '-':
                aus = input('The separator cant be \'-\' because it could be confused whith minus\n')
            else:
                config['separator'] = aus
                break
    else:
        config['separator'] = 'not needed'

    if int(config['dataNumber']) == 1:
        aus = input('Insert the name of the data to read (e.g.: pression)\n')
        config['dataNames'] = aus
    else:
        names = []
        for i in range(int(config['dataNumber'])):
            aus = input(f'Insert data name for data number {i+1}\n')
            names.append(aus)
        config['dataNames'] = names

    aus = input('Choose the number format, 1 for English format (dot at decimals) or 2 for Italian format (comma at decimals)\n')
    while True:
        if aus.isdigit() == False or (int(aus) != 1 and int(aus) != 2):
            aus = input('The option is not valid.\nInsert a valid number, 1 for EN or 2 for IT\n')
        elif int(aus) == 1:
            config['numberFormat'] = 'EN'
            break
        elif int(aus) == 2:
            config['numberFormat'] = 'IT'
            break

    updateJson()

def changeNumFormat(array, Split, Join):
    final = []
    for i in range(len(array)):
        aus = str(array[i]).split(Split)
        aus = Join.join(aus)
        final.append(aus)
    return final

def correctValues(array):
    final = []
    for i in range(len(array[0])):
        aus = []
        for j in range(len(array)):
            aus.append(array[j][i])
        final.append(aus)
    return final

def graph(Time, values, y, single):
    global config
    if y == 1:
        plt.plot(Time, values)
        plt.xlabel('Time (s)')
        plt.xlabel(config['dataNames'])
        plt.title('Time (s) / ' + config['dataNames'])
        plt.show()
    else:
        if single == 'yes':
            for i in range(0, len(y), 1):
                plt.plot(Time, values[y[i]])
                plt.xlabel('Time (s)')
                plt.xlabel(config['dataNames'][y[i]])
                plt.title('Time (s) / ' + config['dataNames'][y[i]])
                plt.show()
        else:
            for i in range(0, len(y), 1):
                plt.plot(Time, values[y[i]], label = config['dataNames'][y[i]])
            plt.legend()
            plt.show()
    

def main():
    global config
    nullExample = []
    stop = loadJson()
    if stop == False:
        std = {'ardData': {'serialPort': 'e.g.: COM7', 'baudrate': 'e.g.:9600'}, 'dataNumber': 'number of individual data sent by arduino every time', 'separator': "the separator between the different types of data sent by arduino at a time (e.g.: '*')", 'dataNames': ['name1', 'name2', 'etc'], 'numberFormat': 'EN for number format whith decimal dot like 1.15 or IT for number format with decimal comma like 1,15. If you want to paste the data in excel make sure to use the correct format.'}
        if config == std:
            autoConfigFirstTime()
        else:
            validData()
        while True:
            try:
                arduino = serial.Serial(config['ardData']['serialPort'], int(config['ardData']['baudrate']), timeout = 0.01)
                break
            except:
                print('The port is probably wrong\nTry reading from another port')
                aus = input('Insert another port:\n')
                while True:
                    if aus.startswith('com') == False and aus.startswith('COM') == False or (len(aus) != 4 and len(aus) != 5) or aus[-1].isdigit() == False:
                        aus = input('The port is not valid. It must be similar to \'COM7\'\n')
                    else:
                        config['ardData']['serialPort'] = aus
                        break
                updateJson()
        initialTime = time.time()
        date = str(datetime.now()).split('.')[0]
        firstData = False
        try:
            os.mkdir(path + '\\dataFiles\\')
        except FileExistsError:
            pass
        file = open((path + '\\dataFiles\\allData.txt'), 'a')
        file.write('\n' + str(date) + '\n')
        file.close()
        print('Started reading data\nCtrl+c to stop')
        try:
            values = []
            Time = []
            while True:
                val = arduino.readline()
                try:
                    decodedVal = str(val[0:len(val)].decode("utf-8"))
                except UnicodeDecodeError:
                    decodedVal = val
                spltVal = decodedVal.split(config['separator'])
                pureData = []
                try:
                    if firstData == False:
                        initialTime = time.time()
                    for i in range(1, len(spltVal)-1, 1):
                        try:
                            pureData.append(float(spltVal[i]))
                        except ValueError:
                            aus = spltVal[i].split('\'')
                            pureData.append(float(aus[1]))
                    if pureData != nullExample:
                        aus = time.time() - initialTime
                        aus = "{:.3f}".format(aus)
                        Time.append(float(aus))
                        values.append(pureData)
                        if firstData == False:
                            firstData = True
                except IndexError:
                    pass
        except KeyboardInterrupt:
            file = open((path + '\\dataFiles\\allData.txt'), 'a')
            file.write('\nList of timestamps: \t\t\tList of data:\n')
            for i in range(0, len(Time), 1):
                file.write(str(i+1) + '. ' + str(Time[i]) + '  \t\t\t\t' + str(values[i]) + '\n')
            file.close()

            if config['numberFormat'] == 'IT':
                Time = changeNumFormat(Time, '.', ',')
                values = correctValues(values)
                for i in range(len(values)):
                    values[i] = changeNumFormat(values[i], '.', ',')

            file = open((path + '\\dataFiles\\time.txt'), 'a')
            file.write('\n' + str(date) + '\n\n')
            for i in range(0, len(Time), 1):
                file.write(str(Time[i]) + ' \n')
            file.close()

            for i in range(0, int(config['dataNumber']), 1):
                file = open((path + '\\dataFiles\\' + config['dataNames'][i] + '.txt'), 'a')
                file.write('\n' + str(date) + '\n\n')
                for j in range(len(values[i])):
                    file.write(values[i][j] + '\n')
                file.close()

            aus = input('Do you want to see the graph?\n(Y/N)\n')
            while True:
                if aus != 'Y' and aus != 'N' and aus != 'y' and aus != 'n' and aus != 'yes' and aus != 'no' and aus != 'Yes' and aus != 'No' and aus != 'YES' and aus != 'NO':
                    aus = input('That is not a valid answer\nDo you want to see the graph?\n(Y/N)\n')
                else:
                    break
            if aus == 'Y' or aus == 'y' or aus == 'yes' or aus == 'Yes' or aus == 'YES':
                
                if int(config['dataNumber']) == 1:
                    if config['numberFormat'] == 'IT':
                        values = changeNumFormat(values, ',', '.')
                        for i in range(0, len(values), 1):
                            values[i] = float(values[i])
                    graph(Time, values, 1, '-')
                else:
                    print('Select the number of the values you want to show in the graph, then type x to see the graph.\nType \'all\' to see everything in the graph.')
                    vals = []
                    for i in range(0, int(config['dataNumber']), 1):
                        print(str(i+1) + '. ' + config['dataNames'][i])
                    while aus != 'x' and len(vals) < int(config['dataNumber']):
                        aus = input()
                        while True:
                            if aus == 'all':
                                for i in range(0, int(config['dataNumber']), 1):
                                    vals.append(i)
                                aus = 'x'
                                break
                            elif aus == 'x':
                                break
                            elif aus.isdigit() == False or int(aus) > int(config['dataNumber']) or int(aus) < 1:
                                print('Not acceptable value.\nSelect the number of the values you want to show in the graph, then type x to see the graph.\nType \'all\' to see everything in the graph.\n')
                                for i in range(0, int(config['dataNumber']), 1):
                                    print(str(i+1) + '. ' + config['dataNames'][i])
                                aus = input()
                            else:
                                vals.append(int(aus)-1)
                                break
                    if config['numberFormat'] == 'IT':
                        for i in range(0, int(config['dataNumber']), 1):
                            values[i] = changeNumFormat(values[i], ',', '.')
                            for j in range(0, len(values[0]), 1):
                                values[i][j] = float(values[i][j])
                    if len(vals) > 1:
                        aus = input('Choose between the options:\n1. Print every line in one graph\n2. Print a graph per data type (close the graph to see the next one)\n')
                        while True:
                            if aus != '1' and aus != '2':
                                print('Value is not acceptable')
                                aus = input('Choose between the options:\n1. Print every line in one graph\n2. Print a graph per data type (close the graph to see the next one)\n')
                            elif aus == '1':
                                graph(Time, values, vals, 'no')
                                break
                            elif aus == '2':
                                graph(Time, values, vals, 'yes')
                                break
                    else:
                        graph(Time, values[vals[0]], 1, '-')
                        
            else:
                pass
            print('Thanks for using this program.\nVisit https://www.github.com/claristorio for more.')
            aus = input()
main()