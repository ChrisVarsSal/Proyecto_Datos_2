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


    def esString(self, s):
        if s =='':
            return False
        return s[0] == -30 and s[s.size() - 1] == -99 or \
               s[0] == 34 and s[s.size() - 1] == 34 or \
               s[0] == 39 and s[s.size() - 1] == 39
        #return s.isalpha()

    def esNumero(self,n):
        return (n.replace('.', '', 1).isdigit())

    def es_flotante(self, variable):
        try:
            float(variable)
            return True
        except:
            return False

    #WRAPPERS
    def AnalizarCodigoFuente(self,string):
        self._AnalizarCodigoFuente(string)

    def leyendoCodigo(self,codigo):
        self._leyendoCodigo(codigo)

    #Desarrollo de funciones
    def _AnalizarCodigoFuente(self,n):
        nombreArchivo=n
        contadorLinea = 1  # para ir contanto las lineas
        linea = []
        tokens = []
        funciones = []
        archivo = open(n, "r",encoding="utf=8")
        linea = archivo.readlines()  # una lista de lineas
        archivo.close()
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
                        if self.esNumero(despues):
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
                        elif self.es_flotante(despues):
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
                    if (not self.esNumero(y) or not self.es_flotante(y) or self.esString(y)) and  y not in self.especiales:
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
                    if not self.esNumero(y) or not self.es_flotante(y) or self.esString(y):
                        if abreParentesis and y in self.hashGlobal and not self.esNumero(y) and not self.es_flotante(y):
                            varAux = self.hashGlobal.get(y)
                            if varAux.alcance <= alcance-1:
                                continue
                            else:
                                print("Error linea", contadorLinea, ": '" + y + "' parametro no definido\n")
                        if abreParentesis and y not in self.hashGlobal and not self.esNumero(y) and not self.es_flotante(y) and y not in self.especiales:
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

    def _leyendoCodigo(self,codigo):
        contador=1
        archivo = open(codigo, "r", encoding="utf=8")
        linea = archivo.readlines()  # una lista de lineas
        archivo.close()
        for i in linea:
            print(contador," "+i)
            contador+=1




