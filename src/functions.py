#Les importations que nous allons utiliser durant le programme
import os
import shutil
import math
import string
import collections

#|-----------------------------------------|
#|       PARTIE 1                         |
#|----------------------------------------|

#Parcourir le dossier pour trouver les noms
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

#|-----------------------------------------|
#|       QUESTIONS PARTIE 1               |
#|----------------------------------------|

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

    # Parcourir les documents et compter la fréquence des mots pour les discours de Chirac
    for filename, doc_scores in tf_idf_matrix.items():
        if 'Chirac' in filename:  # Simplification pour l'exemple
            for word, score in doc_scores.items():
                if word not in least_important_words:
                    word_frequency[word] = word_frequency.get(word, 0) + 1

    # Trouver la fréquence la plus élevée
    max_frequency = max(word_frequency.values(), default=0)

    # Trouver tous les mots qui ont la fréquence la plus élevée
    most_repeated_words = [word for word, frequency in word_frequency.items() if frequency == max_frequency]

    return most_repeated_words, max_frequency


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



def find_all_mentions_of_ecology_or_climate(cleaned_directory):
    # Liste des mots à rechercher
    keywords = ['climat', 'écologie']

    # Dictionnaire pour stocker les présidents et les fichiers correspondants
    president_mentions = {}

    # Parcourir les fichiers
    for filename in os.listdir(cleaned_directory):
        if filename.endswith('.txt'):
            with open(os.path.join(cleaned_directory, filename), 'r', encoding='utf-8') as file:
                content = file.read().lower()

                # Vérifier si l'un des mots-clés est mentionné dans le discours
                if any(keyword in content for keyword in keywords):
                    # Extraire le nom du président du nom du fichier
                    president_name = filename.replace('Nomination_', '').replace('.txt', '').split('_')[0]

                    # Ajouter le nom du président et le fichier à la liste
                    if president_name not in president_mentions:
                        president_mentions[president_name] = []
                    president_mentions[president_name].append(filename)

    return president_mentions


def find_common_words_among_all_presidents(tf_idf_matrix, least_important_words):
    # Initialiser un ensemble avec tous les mots du premier document
    common_words = set(tf_idf_matrix[next(iter(tf_idf_matrix))].keys()) - set(least_important_words)

    # Intersecter les ensembles de mots de tous les documents pour trouver les mots communs
    for doc_scores in tf_idf_matrix.values():
        current_doc_words = set(doc_scores.keys()) - set(least_important_words)
        common_words = common_words.intersection(current_doc_words)

    return common_words




#|-----------------------------------------|
#|                PARTIE 2                |
#|----------------------------------------|
def tokenize_question(question_text):
    # Liste des mots vides
    stop_words = ['le', 'la', 'les', 'un', 'une', 'de', 'du', 'des', 'et', 'en', 'à', 'pour', 'que', 'qui', 'dans',
                  'avec',
                  'sur', 'au', 'par', 'il', 'elle', 'ils', 'elles', 'ce', 'cette', 'ces', 'sa', 'son', 'ses', 'lui',
                  'leur',
                  'leurs', 'mais', 'ou', 'où', 'si', 'comme', 'ne', 'se', 'pas', 'plus', 'moins', 'sont', 'être',
                  'avoir',
                  'tout', 'très', 'peut', 'aussi', 'faire', 'où', 'quand']
    # Supprimer la ponctuation et convertir en minuscules
    question_text = question_text.translate(str.maketrans('', '', string.punctuation)).lower()

    # Tokeniser le texte
    tokens = question_text.split()

    # Supprimer les mots vides
    tokens = [word for word in tokens if word not in stop_words]

    return tokens


def get_unique_corpus_words(cleaned_dir):
    unique_words = set()  #Création d'un ensemble vide pour stocker les mots uniques du corpus

    # Parcours de tous les fichiers dans le répertoire cleaned_dir
    for filename in os.listdir(cleaned_dir):
        filepath = os.path.join(cleaned_dir, filename)

        # Lecture du contenu du fichier et tokenisation des mots avec la fonction tokenize_question()
        with open(filepath, 'r', encoding='utf-8') as file:
            unique_words.update(tokenize_question(file.read()))
    return unique_words

def corpus_unique_words(cleaned_directory):
    unique_words = set() # Création d'un ensemble vide pour stocker les mots uniques du corpus

    # Parcours de tous les fichiers dans le répertoire cleaned_dir
    for filename in os.listdir(cleaned_directory):

        # Vérification si le fichier est un .txt
        if filename.endswith(".txt"):
            # Lecture du contenu du fichier et tokenisation des mots avec la fonction tokenize_question()
            with open(os.path.join(cleaned_directory, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                unique_words.update(tokenize_question(content))
    return unique_words


def compute_question_tf_idf(question, idf_scores):
    # Tokeniser la question
    question_tokens = tokenize_question(question)
    # Calculer la fréquence de chaque mot dans la question (TF)
    tf_scores = {word: question_tokens.count(word) / len(question_tokens) for word in question_tokens}
    # Calculer le vecteur TF-IDF pour la question en utilisant uniquement les mots de la question
    question_tf_idf = {word: tf_scores[word] * idf_scores.get(word, 0) for word in question_tokens if word in idf_scores}
    return question_tf_idf

# Permet de faire un produit scalaire
def produit_scalaire(vecteur_a, vecteur_b):
    return sum(a * b for a, b in zip(vecteur_a, vecteur_b))

# Permet de calculer la norme du vecteyr
def norme_vecteur(vecteur):
    return math.sqrt(sum(a * a for a in vecteur))

# Permet de calculer la similarité entre deux vecteurs
def similarite_cosinus(vecteur_a, vecteur_b):

    # Produit scalaire
    produit = sum(a * b for a, b in zip(vecteur_a, vecteur_b))

    # norme de a et b
    norme_a = math.sqrt(sum(a * a for a in vecteur_a))
    norme_b = math.sqrt(sum(b * b for b in vecteur_b))

    # Permet d'éviter une division par 0
    if norme_a == 0 or norme_b == 0:
        return 0
    return produit / (norme_a * norme_b)

# Permet de calculer le vecteur TF-IDF d'une question
def calculer_vecteur_tf_idf_question(question, scores_idf, mots_uniques_corpus):

    # Permet de tokeniser la question
    mots_question = tokenize_question(question)

    # Calcul TF de chaque mot
    tf_question = {mot: mots_question.count(mot) / len(mots_question) for mot in mots_uniques_corpus}

    # Calcul TF-IDF de chaque mot
    tf_idf_question = {mot: tf_question.get(mot, 0) * scores_idf.get(mot, 0) for mot in mots_uniques_corpus}
    return tf_idf_question

# Permet de calculer les scores de similarité entre un vecteur question et une matrice TF-IDF.
def calculer_similarite(tf_idf_matrix, vecteur_question):

    # Dictionnaire pour stocker les scores de similarité
    scores_similarite = {}

    # Parcours de la matrice TF-IDF contenant les vecteurs pour chaque document
    for doc, vecteur_doc in tf_idf_matrix.items():

        # Création d'une liste de valeurs (vecteur_doc) <=  mots du vecteur_question
        vecteur_doc_list = [vecteur_doc.get(mot, 0) for mot in vecteur_question]

        # Calcul de la similarité entre le vecteur question et le vecteur du document actuel
        scores_similarite[doc] = similarite_cosinus(vecteur_question.values(), vecteur_doc_list)
    return scores_similarite

# Permet de trouver le document le plus pertinent du score
def document_le_plus_pertinent(scores_similarite):

    # Identification du document le plus pertinent
    document_pertinent = max(scores_similarite, key=scores_similarite.get)

    # Récupération du score de similarité
    score_pertinent = scores_similarite[document_pertinent]
    return document_pertinent, score_pertinent

# Permet de trouver le mot avec le TF-IDF le plus élevé
def mot_avec_tf_idf_le_plus_eleve(compute_question_tf_idf):
    mot_max = '' # variable pour stocker le mot avec TF-IDF le plus élevé
    score_max = 0
    for mot, score in compute_question_tf_idf.items():
        if score > score_max:
            score_max = score
            mot_max = mot
    return mot_max


def premiere_occurrence_du_mot(document, mot, cleaned_directory):
    full_path = os.path.join(cleaned_directory, document)
    if os.path.exists(full_path):
        try:
            with open(full_path, 'r', encoding='utf-8') as fichier:
                texte = fichier.read().lower()
                texte = texte.translate(str.maketrans('', '', string.punctuation))
                mots = texte.split()
                if mot in mots:
                    index = mots.index(mot)
                    debut = max(index - 15, 0)
                    fin = min(index + 15, len(mots))
                    return ' '.join(mots[debut:fin])
        except ValueError:
            return "Le mot n'a pas été trouvé dans le document."
    else:
        return "Le fichier n'existe pas."


    # Supprimer la ponctuation
    for char in string.punctuation:
        texte = texte.replace(char, ' ')

    # Trouver la première occurrence du mot
    mots = texte.split()
    index = mots.index(mot) if mot in mots else -1
    if index == -1:
        return ""

    # Reconstituer la phrase contenant le mot
    debut = max(index - 15, 0)
    fin = min(index + 15, len(mots))
    return ' '.join(mots[debut:fin])


def affiner_reponse(question, reponse_brute):
    # Dictionnaire des débuts de réponse possibles selon le type de question
    question_starters = {
        "Comment": "Après analyse, ",
        "Pourquoi": "Car, ",
        "Peux-tu": "Oui, bien sûr! "
    }

    # Identifier le type de question pour choisir le bon début de réponse
    for question_type, starter in question_starters.items():
        if question.startswith(question_type):
            # Ajouter le début de réponse et une majuscule en début de phrase
            reponse_amelioree = starter + reponse_brute[0].upper() + reponse_brute[1:]
            # Ajouter un point final si nécessaire
            if not reponse_amelioree.strip().endswith('.'):
                reponse_amelioree += '.'
            return reponse_amelioree

    # Si aucun type n'est reconnu, retourner la réponse brute avec une majuscule et un point
    reponse_amelioree = reponse_brute[0].upper() + reponse_brute[1:]
    if not reponse_amelioree.strip().endswith('.'):
        reponse_amelioree += '.'
    return reponse_amelioree


def chatbot_reponse(question, cleaned_directory, idf_scores):
    # Tokeniser et calculer le vecteur TF-IDF pour la question
    vecteur_question = compute_question_tf_idf(question, idf_scores)

    # Calculer les similarités de cosinus avec les documents du corpus
    vocabulary, tf_idf_matrix = build_tf_idf_matrix(cleaned_directory)
    scores_similarite = calculer_similarite(tf_idf_matrix, vecteur_question)

    # Trouver le document le plus pertinent
    document_pertinent, score_pertinent = document_le_plus_pertinent(scores_similarite)

    # Trouver le mot avec le score TF-IDF le plus élevé dans la question
    mot_important = mot_avec_tf_idf_le_plus_eleve(vecteur_question)

    # Trouver la phrase contenant le mot important dans le document pertinent
    phrase_contenant_mot_important = premiere_occurrence_du_mot(document_pertinent, mot_important, cleaned_directory)

    # Affiner la réponse
    reponse_affinee = affiner_reponse(question, phrase_contenant_mot_important)

    return reponse_affinee













