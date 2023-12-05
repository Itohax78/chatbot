#Les importations que nous allons utiliser durant le programme
import os
import shutil
import math
import string
import collections



def list_of_files(directory, extension):
   files_names = []
   for filename in os.listdir(directory):
       if filename.endswith(extension):
           files_names.append(filename)
   return files_names


#Extraire les noms de présidents
def extraction():
    Extract = list_of_files("speeches",".txt")
    return(Extract)

#Afficher la liste des noms des présidents
def president(name_presidents=[]):
    names = []
    for filename in name_presidents:
        names.append(filename[11:-4])
    return names

#Supprimer les chiffres
def cancel_number(name_presidents):
    nonumber = []
    for val in name_presidents:
        if val[-1] in "123456789":
            nonumber.append(val[:-1])
        else:
            nonumber.append(val)
    return nonumber

#Enlever les doublons
def duplicate_filter(name_presidents):
    noduplicate = []
    for dup in name_presidents:
        if dup not in noduplicate:
            noduplicate.append(dup)
    return (noduplicate)


#Associer à chaque président un prénom
def first_name(name_presidents):
    prenom = [ ]
    prenom_nom = []
    for i in range(len(name_presidents)):
        if name_presidents[i] == 'Macron':
            prenom.append('Emmanuel')
        elif name_presidents[i] == 'Giscard dEstaing':
            prenom.append('Valéry')
        elif name_presidents[i] == 'Hollande':
            prenom.append('François')
        elif name_presidents[i] == 'Mitterrand':
            prenom.append('François')
        elif name_presidents[i] == 'Chirac':
            prenom.append('Jacques')
        elif name_presidents[i] == 'Sarkozy':
            prenom.append('Nicolas')
    for i in range(len(name_presidents)):
        prenom_nom.append(prenom[i] + " " + name_presidents[i])
    return (prenom_nom)

#Vérifie si e répertoire existe déja
def directory_exist(directory_path):
    return os.path.exists(directory_path) and os.path.isdir(directory_path)

#Permet de créer un nouveau répertoire de documents dit "nettoyé" (lettres en minuscule)
def cleaned(directory):
    name_file = "cleaned"
    if not directory_exist(name_file):
        shutil.copytree(directory, name_file)
        for filename in os.listdir(name_file):
            if filename.endswith("txt"):
                file_path = os.path.join(name_file, filename)
                with open(file_path, 'r') as file:
                    content = file.read()
                content_lower = content.lower()
                with open(file_path, 'w') as cleaned_file:
                    cleaned_file.write(content_lower)

#Permet de créer une liste qui stocke tous les noms des fichiers présents dans le répertoire "cleaned"
def store_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

#Permet d'enlever toutes les ponctuations/accents
def remove_punctuation_character():
    name_file = "cleaned"
    if directory_exist(name_file):
        files_names = store_files(name_file, ".txt")
        for files in files_names:
            file_path = os.path.join(name_file, files)
            with open(file_path, "r") as text:
                content = text.read()
                for char in string.punctuation:
                    content = content.replace(char, ' ')
            with open(file_path, 'w') as cleaned_text:
                cleaned_text.write(content)

#Permet de calculer le score TF d'un mot/phrase choisis
def tf(content):
    word_frequency = {}
    words = content.split()  # Sépare le contenu en mots
    total_words = len(words)  # Compte le nombre total de mots dans le document

    # Calcul de la fréquence de chaque mot dans le document
    for word in words:
        if word in word_frequency:
            word_frequency[word] += 1  # Si le mot existe déjà, incrémente la fréquence
        else:
            word_frequency[word] = 1  # Si le mot n'existe pas, initialise la fréquence à 1

    # Normalisation des fréquences par rapport au nombre total de mots
    for word in word_frequency:
        word_frequency[word] /= total_words

    return word_frequency

#Permet de calculer le score IDF de chaque mots dans chaque document du répertoire "cleaned"
def idf(directory):
    word_documents_count = collections.defaultdict(int)
    total_documents = 0

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            total_documents += 1
            words_in_file = set()

            #Permet de compter les mots uniques dans chaque fichier
            with open(file_path, 'r') as file:
                content = file.read().lower().split()
                words_in_file.update(content)

            #Permet de mettre à jour le compteur du nombre de documents contenant chaque mot
            for word in words_in_file:
                word_documents_count[word] += 1

    #Permet de calculer le score IDF pour chaque mot
    idf_scores = {}
    for word, doc_count in word_documents_count.items():
        idf = math.log(total_documents / doc_count)
        idf_scores[word] = idf

    return idf_scores

#Permet de calculer le score TF-IDF
def calculate_tf_idf_scores(content, directory):
    tf_scores = tf(content)
    idf_scores = idf(directory)
    tf_idf_scores = {}
    for word, tf_value in tf_scores.items():
        tf_idf_scores[word] = tf_value * idf_scores.get(word, 0)

    return tf_idf_scores

#Permet de créer la matrice TF-IDF avec en colonne les documents et en ligne les mots avec leur score TF-IDF associé
'''def calculate_tf_idf_matrix(directory):
    word_index = {}  #Dictionnaire pour stocker les index des mots uniques
    index = 0
    tf_idf_matrix = []  #Matrice pour stocker les valeurs TF-IDF

    idf_scores = idf(directory)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r') as file:
                content = file.read()
                tf_scores = tf(content)

                for word, tf_value in tf_scores.items():
                    if word not in word_index:
                        word_index[word] = index
                        index += 1

    #Permet d'initialiser la matrice TF-IDF avec des zéros
    for j in range(len(word_index)):
        tf_idf_matrix.append([0] * len(os.listdir(directory)))

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r') as file:
                content = file.read()
                tf_scores = tf(content)

                for word, tf_value in tf_scores.items():
                    word_idx = word_index[word]
                    tf_idf_matrix[word_idx][index] = tf_value * idf_scores.get(word, 0)

    #Permet de calculer la transposée de la matrice (échange des lignes et colonnes)
    tf_idf_transpose = []
    for col in range(len(tf_idf_matrix[0])):
        tf_idf_transpose.append([tf_idf_matrix[row][col] for row in range(len(tf_idf_matrix))])

    return tf_idf_transpose'''

'''def recover_string_file(directory, file):
    file_path = os.path.join(directory, file)
    with open(file_path, 'r') as file:
        content = file.read()
def matrice_tf_idf(directory):
    """
     calcule la matrice TF-IDF pour tous les fichiers d'un répertoire.
    """
    # Dictionnaire pour la matrice TF-IDF.
    tf_idf_matrice = {}
    # Calcul des scores IDF.
    idf_scores = idf(directory)
    # Liste des fichiers.
    files = os.listdir(directory)
    for filename in files:
        if filename.endswith('.txt'):
            # Calcul des scores TF pour le fichier actuel.
            tf_scores = tf(recover_string_file(directory, filename))
            for mot, tf in tf_scores.items():
                # Calcul du score TF-IDF.
                tf_idf = tf * idf_scores[mot]
                if mot in tf_idf_matrice:
                    tf_idf_matrice[mot].append(tf_idf)
                else:
                    tf_idf_matrice[mot] = [tf_idf]

    return tf_idf_matrice'''

#fonctionnalité de base à développer

def moinsimportant(directory, num_lowest_scores=10):
    all_tf_idf_scores = {}
    words_with_zero_tf_idf = {}

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r') as file:
                content = file.read()
                tf_idf_scores = calculate_tf_idf_scores(content, directory)

                # Mettre à jour tous les scores TF-IDF calculés
                all_tf_idf_scores.update(tf_idf_scores)

    # Filtrer les mots avec un score TF-IDF égal à zéro
    words_with_zero_tf_idf = {word: score for word, score in all_tf_idf_scores.items() if score == 0}

    return words_with_zero_tf_idf
def highest_score(directory):
    all_tf_idf_scores = {}
    max_tf_idf_score = float('-inf')
    words_with_max_tf_idf = {}

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r') as file:
                content = file.read()
                tf_idf_scores = calculate_tf_idf_scores(content, directory)

                # Mettre à jour tous les scores TF-IDF calculés
                all_tf_idf_scores.update(tf_idf_scores)

    # Trouver le score TF-IDF le plus élevé parmi tous les mots
    max_tf_idf_score = max(all_tf_idf_scores.values())

    # Filtrer les mots avec un score TF-IDF égal au score maximal
    words_with_max_tf_idf = {word: score for word, score in all_tf_idf_scores.items() if score == max_tf_idf_score}

    return words_with_max_tf_idf


def chirac_repetition():
    with open('discours_chirac_1.txt', 'r') as file1, open('discours_chirac_2.txt', 'r') as file2:
        text1 = file1.read()
        text2 = file2.read()

    combined_text = text1 + ' ' + text2
    compteur_mots_combined = (combined_text.split())
    mots_plus_frequents_combined = compteur_mots_combined.most_common(5)
    print("Les mots les plus fréquents dans les discours de Chirac sont :", mots_plus_frequents_combined)



'''discours_presidents = [
    "Nomination_Chirac2.txt",
    "Nomination_Giscard dEstaing.txt",
    "Nomination_Hollande.txt",
    "Nomination_Macron.txt",
    "Nomination_Mitterand1.txt",
    "Nomination_Mitterand2.txt",
    "Nomination_Sarkozy.txt",

]

mots_par_president = []

for discours in discours_presidents:
    with open(discours, 'r') as file:
        text = file.read()
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        mots = text.split()
        mots = [mot for mot in mots if mot not in ["le", "la", "les", "de", "du", "des", "et", "que", "qui", "à", "un", "une", "il", "elle", "nous", "vous"]]
        mots_par_president.append(set(mots))
mots_communs = set.intersection(*mots_par_president)

print("Mots communs à tous les présidents :", mots_communs)
'''