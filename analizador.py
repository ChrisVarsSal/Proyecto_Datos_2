import queue
class Variable:
    def __init__(self, tipo, nombre):
        self.nombre = nombre
        self.tipo = tipo
        self.id = ""
        self.linea = 0
        self.alcance = 0


class Analizador:
    def __init__(self):
        self.hashGlobal = {}
        self.tokensReservados = {
            'void': "void", 'int': "int", 'float': "float", 'string': "string",'if': "if", 
            'while': "while", 'return': "return"
                          }
        self.tokensEspeciales= {
            '+': "+", '-': "-", ';': ";", '*': "*", ',': ",", '/': "/", '=': "=", '==': "==", '!=':"!=",
            '<': "<", '>': ">", ')': ")", '{': "{", '}': "}", '(': "("
                }

    def saveGlobalHash(self,var):
        self.hashGlobal[var.nombre] = var

    #retorna un valor booleno dependiendo si 'n' es un numero, ya se int o float
    def varInt(self,n):
        return (n.replace('.', '', 1).isdigit())

    #retorna un valor booleno dependiendo si 's' es tipo string
    def varString(self, s):
        if (s[0]=='"' and s[len(s)-1]=='"') or (s[0]=="'" and s[len(s)-1]=="'"):
            return True
        else:
            return False

    #retorna un valor booleno dependiendo si 'variables' es tipo float
    def varFloat(self, variable):
        try:
            float(variable)
            return True
        except:
            return False

    #retorna el contenido de un archivo, en forma de array donde cada elemento es una linea del .txt
    def cargarContArchivo(self,nomArchivo):
        try:
            archivo = open(nomArchivo, "r", encoding="utf=8")
            lineas = archivo.readlines() 
            archivo.close()
            return lineas
        except:
            print("Ocurrio un error con al cargar los datos del archivo")
            return False

    #WRAPPERS
    def AnalizadorCodigo(self,nomArchivo):
        self._AnalizadorCodigo(nomArchivo)

    def LectorCodigo(self,nomArchivo):
        self.printArchivo(nomArchivo)

    #Desarrollo de funciones
    def _AnalizadorCodigo(self,nomArchivo):

        linea = self.cargarContArchivo(nomArchivo)
        #por si hubo algun problema al cargar el contenido del archivo
        if linea == False:
            return
        
        tipoVar = ""
        tipoFuncion = ""
        palabraAnterior = ""
        alcance = 0
        contador = 1  # esta variable sirve para contar las lineas de codigo
        funciones = []
        tokens = []

        parentesis = False
        funIgual = False
        corchetes = False
        funReturn = False
        
        for x in linea:  # ir linea por linea del archivo
            word = x.split()
            if len(word) <= 4:
                tipoVar = ""
                for y in word:  # ir recorriendo los tokens de word
                    tokens.append(y)
                    if funIgual:
                        #ejemplo int x = 2, tokenAnt = x
                        #tokenDes = 2
                        #tokenAnt2 = busca si esa variable(x) ya fue definida
                        tokenAnt = tokens[len(tokens)-3]
                        tokenDes = tokens[len(tokens)-1]
                        tokenAnt2 = self.hashGlobal.get(tokenAnt)
                        if self.esNum(tokenDes):
                            if tokenAnt2.tipo == "int":
                                funIgual = False
                                continue
                            elif tokenAnt2.tipo == "float":
                                print("Error linea", contador,": Asignacion incorrecta '" + tokenAnt + "' (" + tokenAnt2.tipo + ") a 'int')\n")
                                funIgual = False
                                continue
                            elif tokenAnt2.tipo == "string":
                                print("Error linea", contador,": Asignacion incorrecta '" + tokenAnt + "' (" + tokenAnt2.tipo + ") a 'int')\n")
                                funIgual = False
                                continue
                        elif self.esFloat(tokenDes):
                            if tokenAnt2.tipo == "float":
                                funIgual = False
                                continue
                            elif tokenAnt2.tipo == "int":
                                print("Error linea", contador,": Asignacion incorrecta '" + tokenAnt + "' (" + tokenAnt2.tipo + ") a 'float')\n")
                                funIgual = False
                                continue
                            elif tokenAnt2.tipo == "string":
                                print("Error linea", contador,": Asignacion incorrecta '" + tokenAnt + "' (" + tokenAnt2.tipo + ") a 'float')\n")
                                funIgual = False
                                continue
                        elif y[0] == '"' and y[len(y)-1] == '"':
                            if tokenAnt2.tipo == "string":
                                funIgual = False
                                continue
                            elif tokenAnt2.tipo == "int":
                                print("Error linea", contador,": Asignacion incorrecta '" + tokenAnt + "' (" + tokenAnt2.tipo + ") a 'string')\n")
                                funIgual = False
                                continue
                            elif tokenAnt2.tipo == "float":
                                print("Error linea", contador,": Asignacion incorrecta '" + tokenAnt + "' (" + tokenAnt2.tipo + ") a 'string')\n")
                                funIgual = False
                                continue
                        elif tokenDes in self.hashGlobal:
                            tokenDes2 = self.hashGlobal.get(tokenDes)
                            if tokenAnt2.tipo == tokenDes2.tipo:
                                funIgual = False
                                continue
                            else:
                                print("Error linea", contador, ": Asignacion incorrecta '"+tokenAnt+"' ("+tokenAnt2.tipo+") a '"+ tokenDes+"' ("+tokenDes2.tipo+")\n")
                                funIgual = False
                                continue
                    if funReturn:
                        if y in self.hashGlobal:
                            varAux2 = self.hashGlobal.get(y)
                            if varAux2.tipo == funciones[len(funciones)-1].tipo:
                                continue
                            else:
                                print("Error linea", contador, ": '" + y + "' el tipo de retorno no coincide con el tipo de la funcion\n")
                        funReturn = False
                    if y == self.tokensReservados.get(y):
                        if y == self.tokensReservados.get("return"):
                            funReturn = True
                            continue
                        else:
                            tipoVar = y
                            continue
                    if (not self.esNum(y) or not self.esFloat(y) or self.esString(y)) and  y not in self.tokensEspeciales:
                        if tipoVar != "":
                            var = Variable(tipoVar,y)
                            var.alcance = alcance
                            var.id = "variable"
                            var.linea = contador
                            self.guardarEnHashGlobal(var)
                        else:
                            if y[0] == '"' and y[len(y)-1] == '"':
                                continue
                            if y != self.tokensEspeciales.get(y) and y not in self.hashGlobal:
                                print("Error linea", contador, ": " + y + " no esta declarada\n")
                    elif y == self.tokensEspeciales.get("}"):
                            corchetes = False
                            alcance -= 1
                            continue
                    elif y == self.tokensEspeciales.get("="):
                        funIgual = True
                        continue

            else:
                tipoVar = ""
                for y in word:
                    tokens.append(y)
                    if y == self.tokensReservados.get(y):
                        if parentesis:
                            tipoVar = y
                            continue
                        tipoFuncion = y
                        continue
                    if not self.esNum(y) or not self.esFloat(y) or self.esString(y):
                        if parentesis and y in self.hashGlobal and not self.esNum(y) and not self.esFloat(y):
                            varAux = self.hashGlobal.get(y)
                            if varAux.alcance <= alcance-1:
                                continue
                            else:
                                print("Error linea", contador, ": '" + y + "' parametro no definido\n")
                        if parentesis and y not in self.hashGlobal and not self.esNum(y) and not self.esFloat(y) and y not in self.tokensEspeciales:
                            if tokens[len(tokens)-2] in self.tokensReservados:
                                #tipoVar= tokens[len(tokens)-1]
                                var = Variable(tipoVar, y)
                                var.alcance = alcance
                                var.id = "variable"
                                var.linea = contador
                                self.guardarEnHashGlobal(var)
                            else:
                                print("Error linea", contador, ": '" + y + "' parametro no definido\n")
                        if tipoFuncion != "" and y not in self.tokensEspeciales and y not in self.hashGlobal:
                            fun = Variable(tipoFuncion,y)
                            fun.alcance = alcance
                            fun.id = "funcion"
                            fun.linea = contador
                            self.guardarEnHashGlobal(fun)
                            funciones.append(fun)
                            continue
                    if y == self.tokensEspeciales.get("("):
                        parentesis = True
                        alcance += 1
                        continue
                    if y == self.tokensEspeciales.get(")"):
                        parentesis = False
                        alcance -= 1
                        continue
                    if y == self.tokensEspeciales.get("{"):
                        corchetes = True
                        alcance += 1
                        continue

            contador += 1

    def printArchivo(self,nomArchivo):
        archivo = open(nomArchivo, "r", encoding="utf=8")
        linea = archivo.readlines()
        archivo.close()

        contadorLector = 1
        for i in linea:
            print(contadorLector," ",i)
            contadorLector+=1
