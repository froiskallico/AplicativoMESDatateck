from datetime import datetime

def logError(msg):
    with open("errors.log", 'a', encoding='CP1252') as file:
        string = "Time: {}    -    {};\n".format(datetime.now(), msg)
        print(string)

        file.write(string)
