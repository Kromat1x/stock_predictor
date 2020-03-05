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
Din adresa asta rezulta impartirea pe cele doua taskuri:  
Payment Process - http://127.0.0.1:5000  
Stock Predictor - http://127.0.0.1:5000/predict  

Dupa pornirea serverului, testarea se poate face atat dintr-un browser cat si dintr-un utilitar precum Postman.  
In cazul Postman, nu am reusit sa il fac sa salveze singur tokenul CSRF atunci cand fac GET si sa il foloseasca la POST.
Asadar, prima data vom da un GET, iar din response-ul de html primit, luam valoarea tokenului de CSRF. Pentru o mai buna intelegere voi atasa un screenshot in care se observa exact locul din care trebuia luat tokenul (input id="csrf_token" name="csrf_token" type="hidden" value="...")

![Raw CSRF](/Images/raw_csrf.png)
  
Vom folosi acest token cand facem POST. POST-ul se face sub forma de formular, astfel, cand construim requestul de POST, mergem la Body si selectam "form-data".  
Formularele ce trebuie completate pentru fiecare dintre taskuri sunt urmatoarele:  
Payment Process  
