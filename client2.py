import socket
import DHKE
from threading import Thread


klijent1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Konekcija na drugi klijent
klijent1.connect(('localhost', 20000))

osnovaModuo = input("Uneti osnovu i moduo: ")

klijent1.send(osnovaModuo.encode())

# Slanje drugom klijentu gde se u istoj liniji čeka na proveru
osnova2, moduo2 = klijent1.recv(4096).decode().split()
osnova, moduo = osnovaModuo.split()

if osnova == osnova2 and moduo == moduo2:
    # Deklaracija i inicijalizacija objekta za vršenje algoritma
    DH = DHKE.DiffieHellman(int(moduo), int(osnova))
    DH.dh_racunaj_javni()
    # Razmena javnih ključeva
    klijent1.send(str(DH.javni).encode())
    javniKljuc2 = klijent1.recv(4096)
    DH.dh_tajni(int(javniKljuc2.decode()))
    print('ISPIS TAJNOG KLJUČA: ', DH.tajni)
else:
    print("Osnova i moduo se ne slažu!")
    klijent1.close()

# Funkcija za primanje poruka, pokrenuta u drugom threadu
def primi():
    while True:
        podaci = klijent1.recv(4096)
        print('-' * 60)
        print('Klijent 1 : ', podaci.decode())
        print("-" * 60, '\n')


Thread(target=primi).start()


while True:
    poruka = input()
    klijent1.send(poruka.encode())
    if poruka == 'x':
        klijent1.close()