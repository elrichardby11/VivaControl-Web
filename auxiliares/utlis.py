def verify_rut(rut):
    ### Verificar DV de RUT

    rut_listo = len(str(rut))

    #Verificar si RUT tiene 8 digitos
    if (rut_listo) != 8:
        print("Rut invalido (8 digitos)... ")

    #Inicializa las variables necesarias
    rut_str = str(rut)
    numeros_a_multiplicar = [3,2,7,6,5,4,3,2]
    resultados = []
    suma = 0

    #Multiplica cada uno de los digitos del rut
    for i, digito in enumerate(rut_str):
        resultado_individual = int(digito) * numeros_a_multiplicar[i]
        resultados.append(resultado_individual)
    
    #Suma cada uno de los resultados de la multiplicacion
    for digito in resultados:
        suma += digito
    
    #Obtener Digito Verificador
    dv = 11-(suma%11)

    #Excepciones para el usuario
    if dv == 11:
        dv = 0
    elif dv == 10:
        dv = "k"

    return str(dv)