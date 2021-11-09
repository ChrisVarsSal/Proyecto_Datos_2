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
        self.palabraReservada = {
            'void': "void", 'int': "int", 'float': "float", 'string': "string",'if': "if", 
            'while': "while", 'return': "return"
                          }
        self.caratecterEspecial = {
            '+': "+", '-': "-", ';': ";", '*': "*", ',': ",", '/': "/", '=': "=", '==': "==", '!=':"!=",
            '<': "<", '>': ">", ')': ")", '{': "{", '}': "}", '(': "("
                }

    def guardarEnHashGlobal(self,var):
        self.hashGlobal[var.nombre] = var
    def varString(self, s):
        if s =='':
            return False
        return s[0] == -30 and s[s.size() - 1] == -99 or \
               s[0] == 34 and s[s.size() - 1] == 34 or \
               s[0] == 39 and s[s.size() - 1] == 39
    def varInt(self,n):
        return (n.replace('.', '', 1).isdigit())
    def varFloat(self, variable):
        try:
            float(variable)
            return True
        except:
            return False

    #WRAPPERS
    def AnalizadorCodigo(self,string):
        self._AnalizadorCodigo(string)

    def LectorCodigo(self,codigo):
        self._LectorCodigo(codigo)

    #Desarrollo de funciones
    def _AnalizadorCodigo(self,n):
        nombreArchivo=n
        contador = 1  # para ir contanto las lineas
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
                        if self.varInt(despues):
                            if antes2.tipo == "int":
                                EsIgual = False
                                continue
                            elif antes2.tipo == "float":
                                print("Error linea", contador,": Asignacion incorrecta '" + 
                                      antes + "' (" + antes2.tipo + ") a 'int')\n")
                                EsIgual = False
                                continue
                            elif antes2.tipo == "string":
                                print("Error linea", contador,": Asignacion incorrecta '" + 
                                      antes + "' (" + antes2.tipo + ") a 'int')\n")
                                EsIgual = False
                                continue
                        elif self.varFloat(despues):
                            if antes2.tipo == "float":
                                EsIgual = False
                                continue
                            elif antes2.tipo == "int":
                                print("Error linea", contador,": Asignacion incorrecta '" + 
                                      antes + "' (" + antes2.tipo + ") a 'float')\n")
                                EsIgual = False
                                continue
                            elif antes2.tipo == "string":
                                print("Error linea", contador,": Asignacion incorrecta '" + 
                                      antes + "' (" + antes2.tipo + ") a 'float')\n")
                                EsIgual = False
                                continue
                        elif y[0] == '"' and y[len(y)-1] == '"':
                            if antes2.tipo == "string":
                                EsIgual = False
                                continue
                            elif antes2.tipo == "int":
                                print("Error linea", contador,": Asignacion incorrecta '" + 
                                      antes + "' (" + antes2.tipo + ") a 'string')\n")
                                EsIgual = False
                                continue
                            elif antes2.tipo == "float":
                                print("Error linea", contador,": Asignacion incorrecta '" + 
                                      antes + "' (" + antes2.tipo + ") a 'string')\n")
                                EsIgual = False
                                continue
                        elif despues in self.hashGlobal:
                            despues2 = self.hashGlobal.get(despues)
                            if antes2.tipo == despues2.tipo:
                                EsIgual = False
                                continue
                            else:
                                print("Error linea", contador, ": Asignacion incorrecta '"+ 
                                      antes +"' ("+antes2.tipo+") a '"+ despues+"' ("+despues2.tipo+")\n")
                                EsIgual = False
                                continue
                    if EsReturn:
                        if y in self.hashGlobal:
                            varAux2 = self.hashGlobal.get(y)
                            if varAux2.tipo == funciones[len(funciones)-1].tipo:
                                continue
                            else:
                                print("Error linea", contador, ": '" + y + 
                                      "' el tipo de retorno no coincide con el tipo de la funcion\n")
                        EsReturn = False
                    if y == self.palabraReservada.get(y):
                        if y == self.palabraReservada.get("return"):
                            EsReturn = True
                            continue
                        else:
                            tipoVariable = y
                            continue
                    if (not self.varInt(y) or not self.varFloat(y) or self.varString(y)) and  y not in self.caratecterEspecial:
                        if tipoVariable != "":
                            var = Variable(tipoVariable,y)
                            var.alcance = alcance
                            var.id = "variable"
                            var.linea = contador
                            self.guardarEnHashGlobal(var)
                        else:
                            if y[0] == '"' and y[len(y)-1] == '"':
                                continue
                            if y != self.caratecterEspecial.get(y) and y not in self.hashGlobal:
                                print("Error linea", contador, ": " + y + " no esta declarada\n")
                    elif y == self.caratecterEspecial.get("}"):
                            abreCorchetes = False
                            alcance -= 1
                            continue
                    elif y == self.caratecterEspecial.get("="):
                        EsIgual = True
                        continue

            else:
                tipoVariable = ""
                for y in word:
                    tokens.append(y)
                    if y == self.palabraReservada.get(y):
                        if abreParentesis:
                            tipoVariable = y
                            continue
                        tipoFuncion = y
                        continue
                    if not self.varInt(y) or not self.varFloat(y) or self.varString(y):
                        if abreParentesis and y in self.hashGlobal and not self.varInt(y) and not self.varFloat(y):
                            varAux = self.hashGlobal.get(y)
                            if varAux.alcance <= alcance-1:
                                continue
                            else:
                                print("Error linea", contador, ": '" + y + "' parametro no definido\n")
                        if abreParentesis and y not in self.hashGlobal and not self.varInt(y) and not self.varFloat(y) and y not in self.caratecterEspecial:
                            if tokens[len(tokens)-2] in self.palabraReservada:
                                #tipoVariable= tokens[len(tokens)-1]
                                var = Variable(tipoVariable, y)
                                var.alcance = alcance
                                var.id = "variable"
                                var.linea = contador
                                self.guardarEnHashGlobal(var)
                            else:
                                print("Error linea", contador, ": '" + y + "' parametro no definido\n")
                        if tipoFuncion != "" and y not in self.caratecterEspecial and y not in self.hashGlobal:
                            fun = Variable(tipoFuncion,y)
                            fun.alcance = alcance
                            fun.id = "funcion"
                            fun.linea = contador
                            self.guardarEnHashGlobal(fun)
                            funciones.append(fun)
                            continue
                    if y == self.caratecterEspecial.get("("):
                        abreParentesis = True
                        alcance += 1
                        continue
                    if y == self.caratecterEspecial.get(")"):
                        abreParentesis = False
                        alcance -= 1
                        continue
                    if y == self.caratecterEspecial.get("{"):
                        abreCorchetes = True
                        alcance += 1
                        continue

            contador += 1

    def _LectorCodigo(self,codigo):
        contadorLector=1
        archivo = open(codigo, "r", encoding="utf=8")
        linea = archivo.readlines()  # una lista de lineas
        archivo.close()
        for i in linea:
            print(contadorLector," "+i)
            contadorLector+=1




