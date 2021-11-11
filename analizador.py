import queue
class Variable:
    def __init__(self, tipo, nombre):
        self.nombre = nombre
        self.tipo = tipo
        self.id = ""
        self.linea = 0
        self.alcance = 0


class AnalizadorSemantico:
    def __init__(self):
        self.hashGlobal = {}
        self.reservada = {'void': "void", 'int': "int", 'float': "float", 'string': "string",
                          'if': "if", 'while': "while", 'return': "return"}
        self.especiales = {'+': "+", '-': "-", ';': ";", '*': "*", ',': ",", '/': "/", '=': "=", '==': "==", '!=': "!=",
                           '<': "<", '>': ">", ')': ")", '{': "{", '}': "}", '(': "("}

    def guardarEnHashGlobal(self,var):
        self.hashGlobal[var.nombre] = var

    #true si s es string
    def esString(self, s):
        return s.isalpha()

    #true si n es float
    def esFloat(self, n):
        #si el token n se puede transformar a un float entonce retorne true
        try:
            float(n)
            return True
        except:
            return False
    
    #true si n es un numero(int o float)
    def esNum(self,n):
        return n.isdigit() or esFloat(n)


    def AnalizarCodigoFuente(self,string):
        self._AnalizarCodigoFuente(string)

    #imprime el contenido de un archivo
    def imprimirArchivo(self,nomArchivo):
        try:
            contador=1
            archivo = open(nomArchivo, "r", encoding="utf=8")
            lineas = archivo.readlines() 
            archivo.close()
            for i in lineas:
                print(contador," ",i)
                contador+=1
        except:
            print("Ocurrio un error con el archivo")

    #abre el archivo y retorna el contenido dividido en lineas en forma de array
    def cargarArchivo(self,nomArchivo):
        try:
            archivo = open(nomArchivo, "r", encoding="utf=8")
            lineas = archivo.readlines() 
            archivo.close()
            return lineas
        except:
            print("Ocurrio un error con el archivo")
            return []
        
    #Desarrollo de funciones
    def _AnalizarCodigoFuente(self,nomArchivo):
        contadorLinea = 1 
        linea = cargarArchivo(nomArchivo)

        #reviso si se pudo cargar el archivo
        if( len(linea) == 0):
            return
        
        tokens = []
        funciones = []
        tipoVariable = ""
        palabraAnterior = ""
        tipoFuncion = ""
        alcance = 0
        abreParentesis = False
        abreCorchetes = False
        EsReturn = False
        EsIgual = False
        for x in linea:  # ir linea por linea del archivo
            word = x.split()
            if len(word) <= 4:
                tipoVariable = ""
                for y in word:  # ir recorriendo los tokens de word
                    tokens.append(y)
                    if EsIgual:
                        antes = tokens[len(tokens)-3]
                        despues = tokens[len(tokens)-1]
                        antes2 = self.hashGlobal.get(antes)
                        if self.esNum(despues):
                            if antes2.tipo == "int":
                                EsIgual = False
                                continue
                            elif antes2.tipo == "float":
                                print("Error linea", contadorLinea,": Asignacion incorrecta '" + antes + "' (" + antes2.tipo + ") a 'int')\n")
                                EsIgual = False
                                continue
                            elif antes2.tipo == "string":
                                print("Error linea", contadorLinea,": Asignacion incorrecta '" + antes + "' (" + antes2.tipo + ") a 'int')\n")
                                EsIgual = False
                                continue
                        elif self.esFloat(despues):
                            if antes2.tipo == "float":
                                EsIgual = False
                                continue
                            elif antes2.tipo == "int":
                                print("Error linea", contadorLinea,": Asignacion incorrecta '" + antes + "' (" + antes2.tipo + ") a 'float')\n")
                                EsIgual = False
                                continue
                            elif antes2.tipo == "string":
                                print("Error linea", contadorLinea,": Asignacion incorrecta '" + antes + "' (" + antes2.tipo + ") a 'float')\n")
                                EsIgual = False
                                continue
                        elif y[0] == '"' and y[len(y)-1] == '"':
                            if antes2.tipo == "string":
                                EsIgual = False
                                continue
                            elif antes2.tipo == "int":
                                print("Error linea", contadorLinea,": Asignacion incorrecta '" + antes + "' (" + antes2.tipo + ") a 'string')\n")
                                EsIgual = False
                                continue
                            elif antes2.tipo == "float":
                                print("Error linea", contadorLinea,": Asignacion incorrecta '" + antes + "' (" + antes2.tipo + ") a 'string')\n")
                                EsIgual = False
                                continue
                        elif despues in self.hashGlobal:
                            despues2 = self.hashGlobal.get(despues)
                            if antes2.tipo == despues2.tipo:
                                EsIgual = False
                                continue
                            else:
                                print("Error linea", contadorLinea, ": Asignacion incorrecta '"+antes+"' ("+antes2.tipo+") a '"+ despues+"' ("+despues2.tipo+")\n")
                                EsIgual = False
                                continue
                    if EsReturn:
                        if y in self.hashGlobal:
                            varAux2 = self.hashGlobal.get(y)
                            if varAux2.tipo == funciones[len(funciones)-1].tipo:
                                continue
                            else:
                                print("Error linea", contadorLinea, ": '" + y + "' el tipo de retorno no coincide con el tipo de la funcion\n")
                        EsReturn = False
                    if y == self.reservada.get(y):
                        if y == self.reservada.get("return"):
                            EsReturn = True
                            continue
                        else:
                            tipoVariable = y
                            continue
                    if (not self.esNum(y) or not self.esFloat(y) or self.esString(y)) and  y not in self.especiales:
                        if tipoVariable != "":
                            var = Variable(tipoVariable,y)
                            var.alcance = alcance
                            var.id = "variable"
                            var.linea = contadorLinea
                            self.guardarEnHashGlobal(var)
                        else:
                            if y[0] == '"' and y[len(y)-1] == '"':
                                continue
                            if y != self.especiales.get(y) and y not in self.hashGlobal:
                                print("Error linea", contadorLinea, ": " + y + " no esta declarada\n")
                    elif y == self.especiales.get("}"):
                            abreCorchetes = False
                            alcance -= 1
                            continue
                    elif y == self.especiales.get("="):
                        EsIgual = True
                        continue

            else:
                tipoVariable = ""
                for y in word:
                    tokens.append(y)
                    if y == self.reservada.get(y):
                        if abreParentesis:
                            tipoVariable = y
                            continue
                        tipoFuncion = y
                        continue
                    if not self.esNum(y) or not self.esFloat(y) or self.esString(y):
                        if abreParentesis and y in self.hashGlobal and not self.esNum(y) and not self.esFloat(y):
                            varAux = self.hashGlobal.get(y)
                            if varAux.alcance <= alcance-1:
                                continue
                            else:
                                print("Error linea", contadorLinea, ": '" + y + "' parametro no definido\n")
                        if abreParentesis and y not in self.hashGlobal and not self.esNum(y) and not self.esFloat(y) and y not in self.especiales:
                            if tokens[len(tokens)-2] in self.reservada:
                                #tipoVariable= tokens[len(tokens)-1]
                                var = Variable(tipoVariable, y)
                                var.alcance = alcance
                                var.id = "variable"
                                var.linea = contadorLinea
                                self.guardarEnHashGlobal(var)
                            else:
                                print("Error linea", contadorLinea, ": '" + y + "' parametro no definido\n")
                        if tipoFuncion != "" and y not in self.especiales and y not in self.hashGlobal:
                            fun = Variable(tipoFuncion,y)
                            fun.alcance = alcance
                            fun.id = "funcion"
                            fun.linea = contadorLinea
                            self.guardarEnHashGlobal(fun)
                            funciones.append(fun)
                            continue
                    if y == self.especiales.get("("):
                        abreParentesis = True
                        alcance += 1
                        continue
                    if y == self.especiales.get(")"):
                        abreParentesis = False
                        alcance -= 1
                        continue
                    if y == self.especiales.get("{"):
                        abreCorchetes = True
                        alcance += 1
                        continue

            contadorLinea += 1

        




