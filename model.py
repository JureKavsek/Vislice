import random
import json

STEVILO_DOVOLJENIH_NAPAK = 10
PRAVILNA_CRKA, PONOVLJENA_CRKA, NAPACNA_CRKA = '+', 'o', '-'
ZMAGA, PORAZ = 'W', 'X'
ZACETEK = 'S'

DATOTEKA_ZA_SHRANJEVANJE = 'C:/code/python/git/vislice/podatki.json'

class Vislice:
    def __init__(self, zacetne_igre=None, zacetni_id=0):
        self.igre = zacetne_igre or {}
        self.max_id = zacetni_id

    def pretvori_v_json_slovar(self):
        slovar_iger = {}

        for id_igre, (igra, stanje) in self.igre.items():
            slovar_iger[id_igre] = {
                Igra.pretvori_v_json_slovar(),
                stanje
            }

        return {
            "max_id": self.max_id,
            "igre": slovar_iger
        }

    def zapisi_v_datoteko(self, datoteka):
        with open(datoteka, 'w') as out_file:
            json_slovar = self.pretvori_v_json_slovar()
            json.dump(json_slovar, out_file, indent=2)

    @classmethod
    def dobi_iz_json_slovarja(cls, slovar):
        slovar_iger = {}
        for id_igre, (igra_slovar, stanje) in slovar['igre'].items():
            slovar_iger[int(id_igre)] = (
                Igra.dobi_iz_json_slovarja(igra, slovar), 
                stanje
            )

        return Vislice(slovar_iger, slovar['max_id'])

    @staticmethod
    def preberi_iz_datoteke(datoteka):
        with open(datoteka, 'r') as in_file:
            json_slovar = json.load(in_file)
        
        return Vislice.dobi_iz_json_slovarja(json_slovar)


    def prost_id_igre(self):
        self.max_id += 1
        return self.max_id

    def nova_igra(self):
        nov_id = self.prost_id_igre()
        sveza_igra = nova_igra()

        self.igre[nov_id] = (sveza_igra, ZACETEK)

        return nov_id

    def ugibaj(self, id_igre, crka):
        #Najdi
        igra, _ = self.igre[id_igre]

        #Posodobi z delegiranjem
        novo_stanje = igra.ugibaj(crka)
        
        #Popravi v slovarju
        self.igre[id_igre] = (igra, novo_stanje)

        return novo_stanje



class Igra:
    def __init__(self, geslo, crke=[]):
        self.geslo = geslo
        self.crke = crke

    def napacne_crke(self):
        return [c for c in self.crke if c.upper() not in self.geslo.upper()]

    def pravilne_crke(self):
        return [c for c in self.crke if c.upper() in self.geslo.upper()]

    def stevilo_napak(self):
        return len(self.napacne_crke())
    
    def poraz(self):
        return self.stevilo_napak() > STEVILO_DOVOLJENIH_NAPAK
    
    def zmaga(self):
        return not self.poraz() and len(self.pravilne_crke()) == len(set(self.geslo))
        

    def pravilni_del_gesla(self):
        pravilno = ''
        for crka in self.geslo.upper():
            if crka in self.crke:
                pravilno += crka
            else:
                pravilno += '_'
        return pravilno
        #return ''.join[c if c in self.crke else '_' for c in self.geslo.upper()]

    def nepravilni_ugibi(self):
        return ' '.join(self.napacne_crke())

    def ugibaj(self, crka):
        crka = crka.upper()
        if crka in self.crke:
            return PONOVLJENA_CRKA
        elif crka in self.geslo.upper():
            self.crke.append(crka)
            if self.zmaga():
                return ZMAGA
            else:
                return PRAVILNA_CRKA
        else:
            self.crke.append(crka)
            if self.poraz():
                return PORAZ
            else:
                return NAPACNA_CRKA
    
    def pretvori_v_json_slovar(self):
        return {
            "geslo": self.geslo,
            "crke": self.crke
        }

    @staticmethod
    def dobi_iz_json_slovarja(slovar):
        return Igra(slovar['geslo'], slovar['crke'])

with open('C:/code/python/git/vislice/besede.txt', encoding="utf8") as f:
    bazen_besed = f.read().split()



def nova_igra():
    geslo = random.choice(bazen_besed)
    return Igra(geslo)

