### OpenPickle.py 

* REQUISITI: Il programma è basato su python3 
* NOTE: Nella stessa cartella del programma deve essere presente la cartella 'Pickle' (Vedi programmi sotto) in cui sono presenti i file .pickle 
* COSA FA: Permette di aprire i grafici, con diverse opzioni, salvati (Vedi programmi sotto) in formato .pickle e quindi editabili. 
Si veda il comando -h per sapere tutte le funzionalita' del programma. 
* COME SI LANCIA: Sul terminale --> python3 OpenPickle.py [options]

---

### Plot3D.py 

* REQUISITI: Il programma è basato su python3 
* NOTE: Nella stessa cartella del programma deve essere presente la cartella 'RateVsVoltage', 'RateVsThreshold' e 'Pickle'. 
* COSA FA: Fa due grafici (uno in 3D e l'altro la heatmap corrispondente) per ciascun scintillatore, in cui si ha sugli assi X e Y la soglia (mV) e i voltaggi (V), mentre sull'asse Z si ha il rate di eventi di singola e li salva nella cartella Pickle. Questo programma semplicemente mette insieme tutte le informazioni ricavate dalla caratterizzazione nella prima parte dell'esperimento.
* COME SI LANCIA: Sul terminale --> python3 Plot3D.py

---

### PlotAll.py 

* REQUISITI: Il programma è basato su python3 
* NOTE: Nella stessa cartella del programma deve essere presente la cartella 'RateVsVoltage', 'RateVsThreshold', 'Efficiency' e 'Pickle'. 
* COSA FA: Questo programma fa il grafico dei Rate vs Voltage e Threshold e delle efficienze al variare della tensione per tre soglie fissate. 
Inoltre salva tutti i grafici nella cartella Pickle. 
* COME SI LANCIA: Sul terminale --> python3 PlotAll.py 

---

### PyEfficiency.py

**!!! DEPRECATED !!!**

---

### Uniformity.py 

* REQUISITI: Il programma è basato su python3 
* NOTE: Nella stessa cartella del programma deve essere presente la cartella 'Uniformity' (con la relativa sottocartella 'Fine') e 'Pickle'. 
* COSA FA: Questo programma fa il grafico delle uniformita' dei tre scintillatori, riportando l'efficienza di ciascuna zona. Inoltre effettua anche la 'fine uniformity' (uniformita' di fino) per il rivelatore Minosse. Ovviamente anche questo programma salva tutti i grafici nella cartella Pickle. 
* COME SI LANCIA: Sul terminale --> python3 Uniformity.py

---

### Linearity.py

* REQUISITI: Il programma è basato su python3 
* NOTE: Nella stessa cartella del programma deve essere presente la cartella 'Digitizer'. 
* COSA FA: Questo programma fa il grafico della linearita' del Digitizer e salva i dati in un file esterno chiamato Linearity_oitput.txt 
* COME SI LANCIA: Sul terminale --> python3 Linearity.py
