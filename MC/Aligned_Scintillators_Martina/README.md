# MonteCarlo

## PROGRAMMI E LORO FUNZIONALITA'

### mcm.c 

* COSA FA: genera 25000 muoni per 500 volte 
* OUTPUT: 3 file txt contenenti il numero di conteggi registrati nelle varie zone degli scintillatori ( _scintillatore1m.txt_ - _scintillatore2m.txt_ - _scintillatore3m.txt_ )
* COME SI LANCIA: prima compilare tramite Makefile (lanciando comando _make_ )

---

### sci1.cpp 

* INPUT: file txt creati da **mcm.c**
* COSA FA: crea i grafici 3d delle distribuzioni spaziali dei muoni sugli scintillatori

---

### Gaussiana.c

* OUTPUT: file gauss.txt contenente l'occorrenza di una certa efficienza, organizzato in due colonne: efficienza e numero di volte che occorre nella simulazione

---

### histo.cpp

* INPUT: file gauss.txt
* COSA FA: genera l'istogramma ed esegue il fit con la Gaussiana

---
