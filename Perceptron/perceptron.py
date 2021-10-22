# Entrenamiento Perceptron

import xlrd
import pandas as pd

# Funcion
def entrenar(theta, fac_ap, w1, w2, epochs, x1, x2, d, n_muestras) :
    errores=True
    while errores : 
        errores=False
        for i in range (n_muestras) :
            # Calculamos z
            z=((x1[i] * w1) + (x2[i] * w2)) - theta

            # Definimos funcion escalon
            if z >= 0 :
                z=1
            else :
                z=0
            
            # Verificamos si z es lo que queremos obtener
            if z != d[i] :
                errores=True
                # Calculamos error
                error=(d[i]-z)
                # Ajustamos theta - umbral
                theta=theta+(-(fac_ap*error))
                # Ajustamos pesos
                w1=w1+(x1[i]*error*fac_ap)
                w2=w2+(x2[i]*error*fac_ap)
                # Los epochs se van incrementando a medida que se van haciendo ajustes
                epochs+=1
    return w1,w2,epochs,theta

# Ciclo Principal
if __name__ == "__main__":
    #Leer Archivo Excel con tabla
    archivo_excel=pd.read_excel("/Users/sinsausti/Develop/Python/preceptron_data.xls")
    theta=0.4
    # Factor de aprendizaje
    fac_ap=0.2
    # Peso 1
    w1=0.3
    # Peso 2
    w2=0.5
    # Iteraciones para ajustar pesos
    epochs=0
    #Muestras - Columnas en excel
    x1=archivo_excel["x1"] 
    x2=archivo_excel["x2"] 
    # Valor deseado - Columna en excel
    d=archivo_excel["d"]
    # Numero de muestras 
    n_muestras=len(d)
    w1,w2,epochs,theta=entrenar(theta,fac_ap,w1,w2,epochs,x1,x2,d,n_muestras)
    print ("w1 = ", w1)
    print ("w2 = ", w2)
    print ("Theta = ", theta)
    print ("Epochs = ", epochs)
