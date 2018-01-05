import pandas as pd
import matplotlib.pyplot as plt
#######################################################################################
# Carga del dataSet que contiene los fallecidos en accidentes aéreos de tráfico civil #
#######################################################################################
#
# Representacion en crudo
#
#######################################################################################

mycrashes = pd.read_csv(
    'C:\\Users\\rodrigo.minguito\\Google Drive\\UOC\\Tipologia y Ciclo de vida de los datos\\Practica2\Airplane_Crashes.csv',
    parse_dates=['Date'], dayfirst=True, index_col='Date'
)

plt.figure()
plt.show(mycrashes['Fatalities'].plot(figsize=(15,10)))