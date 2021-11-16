import analizador

while True:
    print("Proyecto 2 - Estructuras de datos - II Ciclo 2021")
    print("Deiner Rodriguez Villalobos - Christofer Vargas Saldaña - Manfred Zamora Robles")
    print("\n")
    print("\n")
    print("--Ingrese la opción que desea probar--")
    print("1.Analizar el codigo correcto")
    print("2.Analizar el codigo incorrecto)")
    print("3.Salir")
    opcion = input()
    if opcion == "1":
        analisisA = analizador.Analizador()
        analisisA.LectorCodigo("C:/Users/deine/Desktop/P2ED/Proyecto_Datos_2/CodigoCorrecto.txt")
        print("\n")
        analisisA.AnalizadorCodigo("C:/Users/deine/Desktop/P2ED/Proyecto_Datos_2/CodigoCorrecto.txt")
    elif opcion == "2":
        analisisB = analizador.Analizador()
        analisisB.LectorCodigo("C:/Users/deine/Desktop/P2ED/Proyecto_Datos_2/CodigoIncorrecto.txt")
        print("\n")
        analisisB.AnalizadorCodigo("C:/Users/deine/Desktop/P2ED/Proyecto_Datos_2/CodigoIncorrecto.txt")
    elif opcion == "3":
        break




