import csv
import random
import statistics as stats
from scipy import stats as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#######################################################################################
# Carga del dataSet que contiene los fallecidos en accidentes aéreos de tráfico civil #
#######################################################################################
#
# Análisis estadiscico de la evolución del número de accidentes en cada año
#
#######################################################################################

#Generacion de una muestra dentro de una población con un tamaño dado
def muestra(poblacion, tamanno):
    i = 0
    retorno = []
    while (i < tamanno):
        posicion = random.randrange(poblacion.size)
        i = i + 1
        retorno.append(poblacion[posicion])
    return retorno

#Test de Levene
def levene(tamannoMuestras, poblacion):
    results = st.levene(
        muestra(poblacion, tamannoMuestras),
        muestra(poblacion, tamannoMuestras),
        muestra(poblacion, tamannoMuestras),
        muestra(poblacion, tamannoMuestras)
    )
    print("Levene Valor Estadistico %f" % results[0])
    print("Levene Valor p %f" % results[1])

#Test de Bartlett
def bartlett(tamannoMuestras, poblacion):
    results = st.bartlett(
        muestra(poblacion, tamannoMuestras),
        muestra(poblacion, tamannoMuestras),
        muestra(poblacion, tamannoMuestras),
        muestra(poblacion, tamannoMuestras)
    )
    print("Bartlett Valor Estadistico %f" % results[0])
    print("Bartlett Valor p %f" % results[1])


#Abrir fichero
with open(
        'Airplane_Crashes.csv',
        'r') as f:
    reader = csv.reader(f)
    my_list = list(reader)

listaActual = []
anooActual = 0
numVuelos = 0
numFatalities = 0
numAnno = 0
mediaActual = 0
listaMedias = []

idx = range(47)
cols = ['Anno', 'Acumulado', 'NumVuelos', 'Media']
data = pd.DataFrame(index=idx, columns=cols)

# Volcado de los datos. No puedo confiar en que vengan ordenados

# Inicializacion de la matriz
numAnno = 0
while (numAnno < 49):
    data.loc[numAnno, "Anno"] = int(1960 + numAnno)
    data.loc[numAnno, "Acumulado"] = 0
    data.loc[numAnno, "NumVuelos"] = 0
    data.loc[numAnno, "Media"] = 0
    numAnno = numAnno + 1

for linea in my_list:
    if (not linea[0] == "Date"):
        anoo = int((linea[0].partition("/")[2].partition("/")[2]))
        fatalities = int(linea[3])
        acumulado = data.loc[abs(1960 - anoo), "Acumulado"]
        data.loc[abs(1960 - anoo), "Acumulado"] = int(acumulado + fatalities)
        data.loc[abs(1960 - anoo), "NumVuelos"] = int(data.loc[abs(1960 - anoo), "NumVuelos"] + 1)

numAnno = 0
while (numAnno < 49):
    data.loc[numAnno, "Media"] = data.loc[numAnno, "Acumulado"] / data.loc[numAnno, "NumVuelos"]
    listaMedias.append(data.loc[numAnno, "Media"])
    numAnno = numAnno + 1

print(data)

print("****************")
print("Media: %f" % stats.mean(listaMedias))
print("Mediana: %f" % stats.median(listaMedias))
print("Varianza: %f" % stats.variance(listaMedias))
print("Desviación estándar: %f" % stats.stdev(listaMedias))
print("****************")

# https://plot.ly/python/normality-test/
# The Shapiro-Wilk normality test is reputadely more well suited to smaller datasets.

x = data['NumVuelos']

print("")
print("**************************************")
print(" Test de Normalidad")
print("**************************************")
normal_results = st.normaltest(x)
print("Valor Estadistico %f" % normal_results[0])
print("Valor p %f" % normal_results[1])

print("")
print("**************************************")
print(" Test de Normalidad de Shapiro-Wilk")
print("**************************************")
shapiro_results = st.shapiro(x)
print("Valor Estadistico %f" % shapiro_results[0])
print("Valor p %f" % shapiro_results[1])

print("")
print("**************************************")
print(" Test de Normalidad de Kolmogorov-Smirnov")
print("**************************************")
ks_results = st.kstest(x, cdf='norm')
print("Valor Estadistico %f" % ks_results[0])
print("Valor p %f" % ks_results[1])

print("")
print("**************************************")
print(" Homogeneidad de la varianza")
print("**************************************")
# https://stackoverflow.com/questions/36141254/how-to-test-for-homoscedasticity-having-the-same-population-variance-in-python
# https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.bartlett.html
levene(10, x)
levene(10, x)
levene(10, x)
print("")
bartlett(10, x)
bartlett(10, x)
bartlett(10, x)

# https://blog.adrianistan.eu/2017/11/15/estadistica-python-analisis-datos-multidimensionales-regresion-lineal-parte-iv/
# ¿Y la covarianza qué nos dice? Por si mismo, bastante poco. Como mucho, si es positivo nos dice que se relacionarían de forma directa y si es negativa de forma inversa. Pero la covarianza está presente en muchas fórmulas.
print("")
print("**************************************")
print(" Covarianza")
print("**************************************")
covarianza = data.cov()["Anno"]["NumVuelos"]
print("Covarianza %f" % covarianza)

print("")
print("**************************************")
print(" Coeficiente de Correlacion de Pearson")
print("**************************************")
pearson = data.corr(method="pearson")["Anno"]["NumVuelos"]
print("Coeficiente de Correlacion de Pearson %f" % pearson)

m, b = np.polyfit(data["Anno"], data["NumVuelos"], 1)
plt.scatter(data["Anno"], data["NumVuelos"])
plt.xlabel("Fecha")
plt.ylabel("Media")
plt.plot(data["Anno"], m * data["Anno"] + b, '-')
plt.show()
