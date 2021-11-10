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
        analisisA = analizador.Analizador();
        analisisA.LectorCodigo("CodigoCorrecto.txt")
        print("\n")
        analisisA.AnalizarCodigoFuente("CodigoCorrecto.txt")
    elif opcion == "2":
        analisisB = analizador.Analizador()
        analisisB.LectorCodigo("CodigoIncorrecto.txt")
        print("\n")
        analisisB.AnalizadorCodigo("CodigoIncorrecto.txt")
    elif opcion == "3":
        break




