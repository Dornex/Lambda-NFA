graf = {}
vizitat = []
stack = []
lambda_enc = set()

input = open('input.txt', 'r')
output = open('output.txt', 'w')

def lambda_inchidere(stare):
    stack.clear()
    vizitat.clear()
    lambda_enc.clear()

    # Aplic DFS pentru fiecare stare catre care am
    # muchie de tipul (stare_curenta, '.')
    # Daca nu am muchie de acest tip, adaug intr-un set care
    # Reprezinta lambda inchiderea starii apelate de catre subprogram
    stack.append(stare)
    while stack:
        element = stack.pop()
        if (element, '.') in graf:
            vizitat.append(stare)
            for i in delta(element, '.'):
                if i not in vizitat:
                    stack.append(i)
                    vizitat.append(i)
        else:
             lambda_enc.add(element)
    return lambda_enc


def delta(stare, litera):
    # Incerc sa vad daca exista (stare, litera) in graf
    # Daca nu exista, returnez un set() nul
    try:
        return graf[(stare, litera)]
    except:
        return set()


def delta_tilda(stare, cuvant):
    stari_viitoare_aux = set()
    rezultat = set()
    stari_viitoare = delta(stare, cuvant[0])

    # Pentru fiecare stare din lambda inchiderea starii curente,
    # Verific daca pot sa merg cu litera curenta in starea respectiva
    for stare_aux in lambda_inchidere(stare):
        stari_viitoare = stari_viitoare | delta(stare_aux, cuvant[0])

    # Verific daca pentru starile optinute din opertia anterioara,
    # pot sa mai merg inca odata cu lambda inchidere
    for element in stari_viitoare:
        stari_viitoare_aux = stari_viitoare_aux | lambda_inchidere(element)
    stari_viitoare = stari_viitoare | stari_viitoare_aux

    if len(cuvant) == 1:
        return stari_viitoare


    for stare_viitoare in stari_viitoare:
        rezultat = rezultat | delta_tilda(stare_viitoare, cuvant[1:])

    return rezultat


# Citirea datelor dintr-un fisier
numar_stari = int(input.readline().split()[0])
stari = set(input.readline().split())

numar_litere = int(input.readline().split()[0])
litere = set(input.readline().split())

stare_initiala = input.readline().split()[0]

numar_stari_finale = int(input.readline().split()[0])
stari_finale = set(input.readline().split())

numar_tranzitii = int(input.readline().split()[0])

# Initializarea grafului cu urmatoarea notatie: [stare, litera] -> [stari]
for i in range(numar_tranzitii):
    tranzitie = input.readline().split()

    try:
        graf[(tranzitie[0], tranzitie[1])].add(tranzitie[2])
    except:
        graf[(tranzitie[0], tranzitie[1])] = set([tranzitie[2]])

# Citesc cuvintele ce trebuiesc verificate, si apelez pentru fiecare in parte
# functia delta_tilda, dupa care fac intersectia setului returnat de delta_tilda
# cu setul starilor finale
numar_cuvinte = int(input.readline().split()[0])

for i in range(numar_cuvinte):
    cuvant = input.readline().split()[0]
    if delta_tilda(stare_initiala, cuvant) & stari_finale:
        output.write("DA\n")
    else:
        output.write("NU\n")
