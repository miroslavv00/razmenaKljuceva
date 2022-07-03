import socket
import DHKE
from threading import Thread


klijent1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Dodeljuje se IP adresa sa portom soketu
klijent1.bind(('localhost', 20000))
# Zatim se čeka na konekciju
klijent1.listen(1)

klijent2, adresa = klijent1.accept()

# Unos osnove(generatora) i modula
osnovaModuo = input("Uneti osnovu i moduo: ")

# Slanje drugom klijentu gde se u istoj liniji čeka na proveru
klijent2.send(osnovaModuo.encode())

# Osnova i moduo drugog klijenta i ovog klijenta
osnova2, moduo2 = klijent2.recv(4096).decode().split()
osnova, moduo = osnovaModuo.split()

if osnova == osnova2 and moduo == moduo2:
    # Deklaracija i inicijalizacija objekta za vršenje algoritma
    DH = DHKE.DiffieHellman(int(moduo), int(osnova))
    DH.dh_racunaj_javni()
    print("Javni ključ za klijenta 1 je: ",DH.javni)
    # Razmena javnih ključeva
    klijent2.send(str(DH.javni).encode())
    javniKljuc2 = klijent2.recv(4096)
    print("Javni ključ za klijenta 2 je: ",javniKljuc2.decode())
    DH.dh_tajni(int(javniKljuc2.decode()))
    print('Tajni ključ je: : ', DH.tajni)
else:
    print("Osnova i moduo se ne slažu!")
    klijent2.close()

# Funkcija za primanje poruka, pokrenuta u drugom threadu
def primi():
    while True:
        podaci = klijent2.recv(4096)
        print('-' * 60)
        print('Klijent 2 : ', podaci.decode())
        print("-" * 60, '\n')

Thread(target=primi).start()

# Petlja za unos poruka
while True:
    poruka = input()
    klijent2.send(poruka.encode())
    if poruka == 'x':
        klijent2.close()