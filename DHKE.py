import gmpy2
import random


class DiffieHellman:

    # Konstruktor
    def __init__(self, moduo=0, gen=0):
        if (moduo == 0) and (gen == 0):
            self.moduo, self.gen = self.dh_predefined_1536()
        elif (moduo != 0) and (gen != 0):
            self.moduo = moduo
            self.gen = gen
        else:
            raise Exception()
        
        # Generisanje privatnog ključa
        
        self.dh_gen_privatni()
        print(self.privatni)

    # Predefinisan moduo i generator za dimenzije 1536 bita, definisan po RFC 3526

    def dh_predefined_1536(self):
        predefined_p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
        predefined_g = 2

        return (predefined_p, predefined_g)

    # Broj za privatni ključ, dimenzija 16

    def dh_gen_privatni(self):
        seed = random.randrange(5000, 50000)
        self.privatni = int(gmpy2.mpz_rrandomb(gmpy2.random_state(seed), 16))

    # Računanje javnog ključa po formuli osnov

    def dh_racunaj_javni(self):
        self.javni = pow(self.gen, self.privatni) % self.moduo

    # Računanje tajnog, deljenog ključa

    def dh_tajni(self, straniJavni):
        self.tajni = pow(straniJavni, self.privatni, self.moduo)