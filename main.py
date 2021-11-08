import analizador

while True:
    print("Selecciona una opción")
    print("\t1 - Codigo Correcto (correcto.txt)")
    print("\t2 - Codigo Incorrecto (inorrecto.txt))")
    print("\t3 - Salir")
    opcionMenu = input()
    if opcionMenu == "1":
        analizar = AnalizadorSemantico.AnalizadorSemantico()
        analizar.leyendoCodigo("correcto.txt")
        print("\n")
        print("\n")
        analizar.AnalizarCodigoFuente("correcto.txt")
    elif opcionMenu == "2":
        analizar2 = AnalizadorSemantico.AnalizadorSemantico()
        analizar2.leyendoCodigo("incorrecto.txt")
        print("\n")
        print("\n")
        analizar2.AnalizarCodigoFuente("incorrecto.txt")
    elif opcionMenu == "3":
        break




