# payment processor and stock predictor

Proiectul a fost implementat folosind urmatoarele versiuni:  
Tensorflow 1.14.0  
Keras 2.2.5  
Numpy 1.16.0  
  
Pentru restul versiunilor am atastat un output de pip freeze in fisierul requirements.txt

Aveam ceva incompatibilitati cu Tensorflow 2.0 si Keras 2.3.1 in momentul in care am imbunatatit structura proiectului, iar solutia cea mai rapida care sa dea rezultate a fost downgrade-ul la versiunile de mai sus.

# Rularea proiectului  
Proiectul se ruleaza cu "flask run", iar in prealabil se seteaza FLASK_APP cu numele fisierului de server  
  
**set FLASK_APP=server.py**  
  
Se pot modifica la flask parametrii precum adresa sau portul, insa testele mele nu au avut nevoie de asta.  
Am testat cu valorile default: http://127.0.0.1:5000  
Din adresa asta rezulta impartirea pe cele doua taskuri:  
Payment Process - http://127.0.0.1:5000  
Stock Predictor - http://127.0.0.1:5000/predict  

Dupa pornirea serverului, testarea se poate face atat dintr-un browser cat si dintr-un utilitar precum Postman.  
In cazul Postman, nu am reusit sa il fac sa salveze singur tokenul CSRF atunci cand fac GET si sa il foloseasca la POST.
Asadar, prima data vom da un GET, iar din response-ul de html primit, luam valoarea tokenului de CSRF. Pentru o mai buna intelegere voi atasa un screenshot in care se observa exact locul din care trebuia luat tokenul (input id="csrf_token" name="csrf_token" type="hidden" value="...")  

![Raw CSRF](/Images/raw_csrf.png)  
  
**Atentie! In cazul in care testarea dureaza ceva timp, tokenul de CSRF e posibil sa expire, iar procedeul de mai sus cu GET si copierea tokenului trebuie repetat**  
  
  
Vom folosi acest token cand facem POST. POST-ul se face sub forma de formular, astfel, cand construim requestul de POST, mergem la Body si selectam "form-data".  
Formularele ce trebuie completate pentru fiecare dintre taskuri sunt urmatoarele:  
  
Payment Process:  
![FORM_Pay](/Images/form_payment.png)  
  
Stock Predictor:  
![FORM_Pred](/Images/form_predict.png)
  
  
# Rezultate posibile
Incerc sa prezint pe scurt care este functionarea normala a proiectului si voi folosi ca referinta output-urile din Postman.
## Payment Processor
  
**De specificat aici:**  
**Data trebuie introdusa sub formatul afisat ca default in campul de Expiration Date si anume YYYY-mm-dd**
**Numarul cardului trebuie sa fie valid (se valideaza cu algoritmul lui Luhn) si sa fie emis de VISA (sa inceapa cu 4)**
**In rest, validarile sunt cele specificate in cerinta**
  
In cazul completarii corecte a campurilor din formular, output-ul va fi ceva de felul "Payment processed succesfully on the Expensive Gateway" sau "Payment failed on the Cheap Gateway". Payment-ul da fail desi formularul este completat corect in cazul in care gateway-ul/gateway-urile pe care trebuia sa fie procesat, nu este disponibil. In acest caz, pe langa mesajul afisat, Postman va afisa ca status 400 Bad Request. In cazul contrar, acela al procesarii cu succes, statusul va fi 200 OK.  
  
Daca formularul nu a fost completat conform cerintelor, response-ul va avea ca status 400 Bad Request, si va fi primit un HTML, care odata afisat in Preview, sau citit in Raw si urmarit tag-ul cu class="errors", se vor putea vedea ce probleme au aparut la validare.

## Stock Predictor
  
**De specificat aici:**  
**Modelul este antrenat folosind date saptamanale din 25 de saptamani, iar acest model poate realiza predictii pe date care sunt dupa acest interval. Predictia se realizeaza din aproape in aproape, ultima data din setul de date este 24/06/2011, asadar, predictia ce poate fi facuta incepe cu 01/07/2011. Pentru o data mai indepartata de atat, modelul realizeaza predictii succesive, iar fiecare predictie intermediara este adaugata ca data la setul de date, avansand astfel saptamana cu saptamana pana la data dorita.**  
**Pentru rezultate ok si un timp de rulare care sa nu dureze prea mult, ar fi de preferat sa fie testat cu niste date care sa fie la maxim 5-6 saptamani distanta**
  
Singura validare a formularului este cea spusa si mai sus, data introdusa trebuie sa fie mai mare decat 01/07/2011, ca predictia sa aiba sens. Pentru ca diferenta de zile intre ultima data cunoscuta si data introdusa este impartita la 7 si apoi se face floor pe ea, practic se ia parte intreaga. In cazul introducerii unei date valide rezultatul obtinut va fi de forma : "Predicted closing price: 162.31044006347656"  
  
**Din pacate aici exista o problema careia nu i-am putut da de cap, deoarece am observat-o foarte tarziu**  
**Daca in formularul de predict, se completeaza data corecta si se da predictia (flow normal), dupa care se modifica data cu una gresita si se incearca rulareaza, da un 400 impreuna un un HTML unde se vede si eroarea de validare (flow normal), insa dupa scenariul asta, daca dau o data corecta se primeste 500 internal server error care ar parea sa fie ceva din tensorflow, insa nu am reusit sa-mi dau seama ce il deranjeaza din scenariul de mai sus**  
**Daca primele incercari pe care le realizez dupa pornirea serverului sunt cu date eronate, iar apoi dau o data corecta, nu are nicio problema si functioneaza normal, problema apare doar in scenariul descris mai sus**

