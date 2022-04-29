# Pixel-Golf

Acest joc prezinta diverse nivele prin care jucatorul trebuie sa treaca. Prin-
cipalul scop este de a baga mingea de golf in gaura in cat mai putine lovituri
posibile.

Implementare : Intreg codul este scris in python, utilizand modulul pygame si
utilitatile oferite de acesta.

Versiunea Beta : 29.04.2022
- crearea principalelor obiecte cu care se poate interactiona in acest joc : 
    *minge de golf : utilizatorul poate manevra directia mingii apasand click
stanga pe ecran, iar in functie de distanta unde s-a facut click-ul fata de
minge se calculeaza traiectoria pe care aceasta o va lua si puterea cu care
aceasta va fi lovita. Pentru a informa utilizatorul este dispusa o bara de
putere sugestiva pentru a cunoaste viteza cu care va fi lovita mingea.
    *gaura : este un obiect static care poate doar interactiona cu mingea a-
tunci cand aceasta intra in contact cu gaura. In acest caz jocul se restar-
teaza si se pastreaza scorul final.
    *ziduri : obiecte statice care pot reflecta mingea in directia opusa ca
intr-o oglinda