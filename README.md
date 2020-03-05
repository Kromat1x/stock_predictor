# stock_predictor

Proiectul a fost implementat folosind urmatoarele versiuni:  
Tensorflow 1.14.0  
Keras 2.2.5  
Numpy 1.16.0  

Aveam ceva incompatibilitati cu Tensorflow 2.0 si Keras 2.3.1 in momentul in care am imbunatatit structura proiectului, iar solutia cea mai rapida care sa dea rezultate a fost downgrade-ul la versiunile de mai sus.

# Rularea proiectului  
Proiectul se ruleaza cu "flask run", iar in prealabil se seteaza FLASK_APP cu numele fisierului de server  
  
set FLASK_APP=server.py  
  
Se pot modifica la flask parametrii precum adresa sau portul, insa testele mele nu au avut nevoie de asta.  
Am testat cu valorile default: http://127.0.0.1:5000

Dupa pornirea serverului, testarea se poate face atat dintr-un browser cat si dintr-un utilitar precum Postman.  
In cazul Postman, 
