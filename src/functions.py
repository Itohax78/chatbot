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
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                content_lower = content.lower()
                with open(file_path, 'w', encoding='utf-8') as cleaned_file:
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
            with open(file_path, "r", encoding='utf-8') as text:
                content = text.read()
                for char in string.punctuation:
                    content = content.replace(char, ' ')
            with open(file_path, 'w', encoding='utf-8') as cleaned_text:
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
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().lower().split()
                words_in_file.update(content)

            #Permet de mettre à jour le compteur du nombre de documents contenant chaque mot
            for word in words_in_file:
                word_documents_count[word] += 1

    #Permet de calculer le score IDF pour chaque mot
    idf_scores = {}
    for word, doc_count in word_documents_count.items():
        idf = math.log10(total_documents / doc_count)
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
def build_tf_idf_matrix(directory):
    idf_scores = idf(directory)
    vocabulary = list(idf_scores.keys())
    tf_idf_matrix = {}

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().lower()

            # Calculer les scores TF pour le document courant
            tf_scores = tf(content)

            # Construire le vecteur TF-IDF pour le document courant
            tf_idf_vector = {word: tf_scores.get(word, 0) * idf_scores.get(word, 0) for word in vocabulary}
            tf_idf_matrix[filename] = tf_idf_vector

    return vocabulary, tf_idf_matrix


def find_least_important_words(tf_idf_matrix):
    least_important_words = set()  # Utiliser un ensemble pour éviter les doublons

    # Initialiser l'ensemble avec tous les mots du premier document
    first_doc_scores = next(iter(tf_idf_matrix.values()))
    for word in first_doc_scores:
        least_important_words.add(word)

    # Parcourir la matrice TF-IDF pour chaque document
    for doc_scores in tf_idf_matrix.values():
        for word in least_important_words.copy():  # Créer une copie pour modifier l'ensemble pendant l'itération
            # Si un mot a un score TF-IDF > 0 dans ce document, le retirer de l'ensemble
            if doc_scores.get(word, 0) > 0:
                least_important_words.discard(word)

    return list(least_important_words)  # Convertir l'ensemble en liste avant de retourner

def find_highest_tf_idf_words(tf_idf_matrix):
    highest_score = 0
    highest_words = []

    # Parcourir tous les documents
    for doc_scores in tf_idf_matrix.values():
        # Parcourir tous les mots et leurs scores TF-IDF
        for word, score in doc_scores.items():
            # Si le score actuel est plus élevé que le score le plus élevé enregistré
            if score > highest_score:
                highest_score = score
                highest_words = [word]
            # Si le score actuel est égal au score le plus élevé, ajouter le mot à la liste
            elif score == highest_score:
                highest_words.append(word)

    return highest_words, highest_score

def find_most_repeated_words_by_chirac(tf_idf_matrix, least_important_words):
    word_frequency = {}

    for filename, doc_scores in tf_idf_matrix.items():
        # Vérifiez si le fichier est l'un des discours de Chirac
        if 'Nomination_Chirac1.txt' in filename or 'Nomination_Chirac2.txt' in filename:
            for word, score in doc_scores.items():
                if word not in least_important_words:
                    if word not in word_frequency:
                        word_frequency[word] = 0
                    word_frequency[word] += 1  # Incrementer la fréquence du mot

    # Trouver le mot le plus répété
    most_repeated_word = max(word_frequency, key=word_frequency.get, default=None)
    most_repeated_count = word_frequency.get(most_repeated_word, 0)

    return most_repeated_word, most_repeated_count



def find_presidents_mentions_of_nation(tf_idf_matrix):
    # Initialiser un dictionnaire pour compter les mentions de "nation" pour chaque président
    president_nation_mentions = {}

    # Parcourir tous les documents pour compter les mentions pour chaque président
    for filename, doc_scores in tf_idf_matrix.items():
        # Extraire le nom du président du nom du fichier
        president_name = filename.replace('Nomination_', '').replace('.txt', '')

        # Compter les mentions de "nation"
        president_nation_mentions[president_name] = president_nation_mentions.get(president_name, 0) + doc_scores.get(
            'nation', 0)

    # Trouver le président qui a mentionné "nation" le plus de fois
    most_mentions = max(president_nation_mentions, key=president_nation_mentions.get)
    most_mentions_count = president_nation_mentions[most_mentions]

    return president_nation_mentions, most_mentions, most_mentions_count

def find_first_mention_of_ecology_or_climate(cleaned_directory):
    # Liste des mots à rechercher
    keywords = ['climat', 'écologie', 'environnement']

    # Parcourir les fichiers dans l'ordre alphabétique, qui peut correspondre à l'ordre chronologique
    for filename in sorted(os.listdir(cleaned_directory)):
        if filename.endswith('.txt'):
            with open(os.path.join(cleaned_directory, filename), 'r', encoding='utf-8') as file:
                content = file.read().lower()
                # Vérifier si l'un des mots-clés est mentionné dans le discours
                if any(keyword in content for keyword in keywords):
                    # Extraire le nom du président du nom du fichier
                    president_name = filename.replace('Nomination_', '').replace('.txt', '').split('_')[0]
                    return president_name, filename

    return None, None

def find_common_words_among_all_presidents(tf_idf_matrix, least_important_words):
    # Initialiser un ensemble avec tous les mots du premier document
    common_words = set(tf_idf_matrix[next(iter(tf_idf_matrix))].keys()) - set(least_important_words)

    # Intersecter les ensembles de mots de tous les documents pour trouver les mots communs
    for doc_scores in tf_idf_matrix.values():
        current_doc_words = set(doc_scores.keys()) - set(least_important_words)
        common_words = common_words.intersection(current_doc_words)

    return common_words