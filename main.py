import analizador

while True:
    print("\n")
    print("Ingrese la opción que desea probar")
    print("1.Analizar el codigo correcto")
    print("2.Analizar el codigo incorrecto)")
    print("3.Salir")
    opcion = input()
    if opcion == "1":
        analizar = AnalizadorSemantico.AnalizadorSemantico()
        analizar.leyendoCodigo("correcto.txt")
        print("\n")
        analizar.AnalizarCodigoFuente("correcto.txt")
    elif opcion == "2":
        analizar2 = AnalizadorSemantico.AnalizadorSemantico()
        analizar2.leyendoCodigo("incorrecto.txt")
        print("\n")
        analizar2.AnalizarCodigoFuente("incorrecto.txt")
    elif opcion == "3":
        break




