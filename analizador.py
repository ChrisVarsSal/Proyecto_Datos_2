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

    def saveGlobalHash(self,var):
        self.hashGlobal[var.nombre] = var

    def varInt(self,n):
        return (n.replace('.', '', 1).isdigit())

    def varString(self, s):
        if s =='':
            return False
        return s[0] == -30 and s[s.size() - 1] == -99 or \
               s[0] == 34 and s[s.size() - 1] == 34 or \
               s[0] == 39 and s[s.size() - 1] == 39
               
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
        tipoVar = " "
        tipoFuncion = " "
        palabraAnterior = " "
        alcance = 0
        contador = 1  # esta variable sirve para contar las lineas de codigo
        linea = []
        funciones = []
        tokens = []
        parentesis = False
        funIgual = False
        corchetes = False
        funReturn = False
        archivo = open(n, "r",encoding="utf=8")
        linea = archivo.readlines()  # una lista de lineas
        archivo.close()
        for x in linea:  #recorre linea por linea del archivo .txt
            word = x.split()
            if len(word) <= 4:
                tipoVar = ""
                for y in word:  # ir recorriendo los tokens de word
                    tokens.append(y)
                    if funIgual:
                        a = tokens[len(tokens)-3]
                        x = tokens[len(tokens)-1]
                        b = self.hashGlobal.get(a)
                        if self.varInt(x):
                            if b.tipo == "int":
                                funIgual = False
                                continue
                            elif b.tipo == "float":
                                print("Error en la linea", contador,": Asignacion incorrecta '" + 
                                      a + "' (" + b.tipo + ") a 'int')\n")
                                funIgual = False
                                continue
                            elif b.tipo == "string":
                                print("Error en la linea", contador,": Asignacion incorrecta '" + 
                                      a + "' (" + b.tipo + ") a 'int')\n")
                                funIgual = False
                                continue
                        elif self.varFloat(x):
                            if b.tipo == "float":
                                funIgual = False
                                continue
                            elif b.tipo == "int":
                                print("Error en la linea", contador,": Asignacion incorrecta '" + 
                                      a + "' (" + b.tipo + ") a 'float')\n")
                                funIgual = False
                                continue
                            elif b.tipo == "string":
                                print("Error en la linea", contador,": Asignacion incorrecta '" + 
                                      a + "' (" + b.tipo + ") a 'float')\n")
                                funIgual = False
                                continue
                        elif y[0] == '"' and y[len(y)-1] == '"':
                            if b.tipo == "string":
                                funIgual = False
                                continue
                            elif b.tipo == "int":
                                print("Error en la linea", contador,": Asignacion incorrecta '" + 
                                      a + "' (" + b.tipo + ") a 'string')\n")
                                funIgual = False
                                continue
                            elif b.tipo == "float":
                                print("Error en la linea", contador,": Asignacion incorrecta '" + 
                                      a + "' (" + b.tipo + ") a 'string')\n")
                                funIgual = False
                                continue
                        elif w in self.hashGlobal:
                            z = self.hashGlobal.get(w)
                            if b.tipo == z.tipo:
                                funIgual = False
                                continue
                            else:
                                print("Error en la linea", contador, ": Asignacion incorrecta '"+ 
                                      a +"' ("+b.tipo+") a '"+ w+"' ("+z.tipo+")\n")
                                funIgual = False
                                continue
                    if funReturn:
                        if y in self.hashGlobal:
                            varAux2 = self.hashGlobal.get(y)
                            if varAux2.tipo == funciones[len(funciones)-1].tipo:
                                continue
                            else:
                                print("Error en la linea", contador, ": '" + y + 
                                      "' el tipo de retorno no coincide con el tipo de la funcion\n")
                        funReturn = False
                    if y == self.palabraReservada.get(y):
                        if y == self.palabraReservada.get("return"):
                            funReturn = True
                            continue
                        else:
                            tipoVar = y
                            continue
                    if (not self.varInt(y) or not self.varFloat(y) or self.varString(y)) and  y not in self.caratecterEspecial:
                        if tipoVar != "":
                            var = Variable(tipoVar,y)
                            var.alcance = alcance
                            var.id = "variable"
                            var.linea = contador
                            self.saveGlobalHash(var)
                        else:
                            if y[0] == '"' and y[len(y)-1] == '"':
                                continue
                            if y != self.caratecterEspecial.get(y) and y not in self.hashGlobal:
                                print("Error en la linea", contador, ": " + y + " no esta declarada\n")
                    elif y == self.caratecterEspecial.get("}"):
                            corchetes = False
                            alcance -= 1
                            continue
                    elif y == self.caratecterEspecial.get("="):
                        funIgual = True
                        continue
            else:
                tipoVar = ""
                for y in word:
                    tokens.append(y)
                    if y == self.palabraReservada.get(y):
                        if parentesis:
                            tipoVar = y
                            continue
                        tipoFuncion = y
                        continue
                    if not self.varInt(y) or not self.varFloat(y) or self.varString(y):
                        if parentesis and y in self.hashGlobal and not self.varInt(y) and not self.varFloat(y):
                            varAux = self.hashGlobal.get(y)
                            if varAux.alcance <= alcance-1:
                                continue
                            else:
                                print("Error en la linea", contador, ": '" + y + 
                                      "' parametro no definido\n")
                        if parentesis and y not in self.hashGlobal and not self.varInt(y) and not self.varFloat(y) and y not in self.caratecterEspecial:
                            if tokens[len(tokens)-2] in self.palabraReservada:
                                #tipoVar= tokens[len(tokens)-1]
                                var = Variable(tipoVar, y)
                                var.alcance = alcance
                                var.id = "variable"
                                var.linea = contador
                                self.saveGlobalHash(var)
                            else:
                                print("Error en la linea", contador, ": '" + y + 
                                      "' parametro no definido\n")
                        if tipoFuncion != "" and y not in self.caratecterEspecial and y not in self.hashGlobal:
                            fun = Variable(tipoFuncion,y)
                            fun.alcance = alcance
                            fun.id = "funcion"
                            fun.linea = contador
                            self.saveGlobalHash(fun)
                            funciones.append(fun)
                            continue
                    if y == self.caratecterEspecial.get("("):
                        parentesis = True
                        alcance += 1
                        continue
                    if y == self.caratecterEspecial.get(")"):
                        parentesis = False
                        alcance -= 1
                        continue
                    if y == self.caratecterEspecial.get("{"):
                        corchetes = True
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
