import bottle
import model
from bottle import template

vislice = model.Vislice()

bottle.TEMPLATE_PATH.insert(0,'C:/code/python/git/vislice/views/')

@bottle.get("/")
def index():
    return bottle.template('index.tpl')


@bottle.post('/igra/')
def nova_igra():

    vislice = model.Vislice.preberi_iz_datoteke(
        model.DATOTEKA_ZA_SHRANJEVANJE
    )

    id_igre = vislice.nova_igra()
    novi_url = f'/igra/{id_igre}/'

    vislice.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)

    bottle.redirect(novi_url)

@bottle.get('/igra/<id_igre:int>/')
def pokazi_igro(id_igre):
    vislice = model.Vislice.preberi_iz_datoteke(
        model.DATOTEKA_ZA_SHRANJEVANJE
    )

    trenutna_igra, trenutno_stanje = vislice.igre[id_igre]

    vislice.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)

    return bottle.template('igra.tpl',
        igra=trenutna_igra, stanje=trenutno_stanje
    )

@bottle.post('/igra/<id_igre:int>/')
def ugibaj_na_igri(id_igre):
    vislice = model.Vislice.preberi_iz_datoteke(
        model.DATOTEKA_ZA_SHRANJEVANJE
    )

    trenutna_igra = vislice.igre[id_igre]
    ugibana = bottle.request.forms['crka']

    vislice.ugibaj(id_igre, ugibana)

    vislice.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    
    return bottle.redirect(f'/igra/{id_igre}/')

bottle.run(reloader=True, debug=True)







