#Graoupe : TACHRIFT karim , LORIENTE lucas , YABA-NGO charlotte // 


# Importer les modules nécessaires
import json
import random
from collections import Counter

# Définir le seuil de filtrage
seuil_filtre = 50

# Fonction pour charger les mots à partir d'un fichier
def charger_mots(fichier):
    with open(fichier, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

# Fonction pour créer les occurrences de bigrammes, trigrammes, tetragrammes et terminaisons
# On a trouver des explications supplémentaires sur les fréquences des séquences dans le français ici : https://www.apprendre-en-ligne.net/crypto/stat/francais.html 
def creer_occurrences(mots, seuil_filtre):
    trigrammes = Counter()
    tetragrammes = Counter()
    terminaisons = Counter()

    for mot in mots:
        for i in range(len(mot) - 2):
            trigramme = mot[i:i+3]  # On extrait les trigrammes
            trigrammes[trigramme] += 1
        for i in range(len(mot) - 3):
            tetragramme = mot[i:i+4]  # On extrait les tétragrames
            tetragrammes[tetragramme] += 1
        if len(mot) > 3:
            terminaisons[mot[-3:]] += 1  # On extrait les terminaisons

    # Filtrer les occurrences pour ne garder que celles qui se répètent
    trigrammes_filtres = {seq: count for seq, count in trigrammes.items() if count > seuil_filtre}
    tetragrammes_filtres = {seq: count for seq, count in tetragrammes.items() if count > seuil_filtre}
    terminaisons_filtrees = {ter: count for ter, count in terminaisons.items() if count > seuil_filtre}
    
    return trigrammes_filtres, tetragrammes_filtres, terminaisons_filtrees

# Fonction pour calculer les probabilités à partir des occurrences
def calculer_probabilites(occurrence):
    probabilites = {}
    total_occurrences = sum(occurrence.values())
    for sequence_lettres, count in occurrence.items():
        probabilites[sequence_lettres] = count / total_occurrences
    return probabilites

# Fonction pour sauvegarder les données dans un fichier JSON
def sauvegarder_donnees(occurrence, probabilites, fichier):
    with open(fichier, 'w') as json_file:
        json.dump({
            'occurrences': occurrence,
            'probabilites': probabilites
        }, json_file, indent=4)

# Fonction pour générer un mot aléatoire à partir des trigrammes, tetragrammes et terminaisons
def generer_mot(trigrammes, tetragrammes, terminaisons):
    longueur_mot = random.randint(5, 12)  # Longueur aléatoire entre 5 et 12 lettres
    mot = ''
    sequence_precedente = choisir_sequence_initiale(trigrammes, tetragrammes)
    mot += sequence_precedente
    while len(mot) < longueur_mot:
        sequence_suivante = choisir_sequence_suivante(sequence_precedente, trigrammes, tetragrammes)
        mot += sequence_suivante[-1]
        sequence_precedente = mot[-len(sequence_precedente):]
        if len(mot) >= longueur_mot:
            break
    # Choisir une terminaison aléatoire parmi les terminaisons fréquentes et ajouter au mot généré
    terminaison = random.choice(list(terminaisons.keys()))
    mot += terminaison
    return mot

# Fonction pour choisir une séquence initiale aléatoire
def choisir_sequence_initiale(trigrammes, tetragrammes):
    sequences = list(trigrammes.keys()) + list(tetragrammes.keys())
    return random.choice(sequences)

# Fonction pour choisir la séquence suivante à partir de la séquence précédente
def choisir_sequence_suivante(sequence_precedente, trigrammes, tetragrammes):
    sequences = []
    for seq in [trigrammes, tetragrammes]:
        for key in seq:
            if key.startswith(sequence_precedente[-len(key) + 1:]):
                sequences.append(key)
    if sequences:
        return random.choice(sequences)
    else:
        # Si la liste sequences est vide, retourner une séquence aléatoire parmi toutes les clés des compteurs
        return random.choice(list(trigrammes.keys()) + list(tetragrammes.keys()))

# Charger les mots à partir du fichier
mots = charger_mots('mots.txt')

# Créer les occurrences de trigrammes, tetragrammes et terminaisons
trigrammes, tetragrammes, terminaisons = creer_occurrences(mots, seuil_filtre)

# Calculer les probabilités à partir des occurrences
probabilites = {
    'trigrammes': calculer_probabilites(trigrammes),
    'tetragrammes': calculer_probabilites(tetragrammes),
    'terminaisons': calculer_probabilites(terminaisons)
}

# Sauvegarder les données dans un fichier JSON
sauvegarder_donnees(
    {
        'trigrammes': trigrammes,
        'tetragrammes': tetragrammes,
        'terminaisons': terminaisons
    },
    probabilites,
    'doc.json'
)

# Demander à l'utilisateur le nombre de mots à générer
nombre_mots_a_generer = int(input("Entrez le nombre de mots à générer : "))

# Générer les mots
for _ in range(nombre_mots_a_generer):
    mot_genere = generer_mot(trigrammes, tetragrammes, terminaisons)
    print("Mot généré :", mot_genere)
