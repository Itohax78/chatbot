# On importe les fonctions et la fonction time que nous allons utiliser pour notre menu
import functions
import time
import os

chemin_speeches = input("Veuillez saisir le chemin d'accès du dossier speeches avant tout usage : ")

chemin_cleaned = chemin_speeches.replace("speeches", "cleaned")

#|----------------------------------------|
#|       Fonctions de base                |
#|----------------------------------------|


extraire_nom = functions.extraction()
print(extraire_nom)

name = functions.president(functions.list_of_files("speeches", ".txt"))
print(name)

number = functions.cancel_number(name)
print(number)

noduplicate = functions.duplicate_filter(number)
print(noduplicate)

prenom = functions.first_name(noduplicate)
print(prenom)

functions.directory_exist(chemin_speeches)

cleaned = functions.cleaned(chemin_speeches)
print(cleaned)




#|-----------------------------------------|
#|       MENU UTILISATEUR                 |
#|----------------------------------------|
def afficher_menu():
    print("|----------------|")
    print("|    ChatBot     |")
    print("|----------------|")
    time.sleep(1.5)
    # Les différentes options pour les utilisateurs
    print("1. Afficher la liste des mots les moins importants")
    print("2. Afficher les mots ayant le score TF-IDF le plus élevé")
    print("3. Afficher les mots les plus répétés par le président Chirac")
    print("""4. Afficher les noms des présidents qui ont parlé de la "Nation" et de celui qui l'a répété le plus de fois""")
    print("5. Affiche le premier président à parler du climat et de l'écologie")
    print("6. Affiche les mots que tous les présidents ont évoqués /!\ : supprimé ")
    print("7. Posez une question à notre ChaBot")
    print("8. Quitter")


def option1():
    vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix(chemin_cleaned)
    least_important_words = functions.find_least_important_words(tf_idf_matrix)
    print("Les mots les moins importants sont :", least_important_words)

def option2():
    vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix(chemin_cleaned)
    highest_words, highest_score = functions.find_highest_tf_idf_words(tf_idf_matrix)
    print("Le mot avec le score TF-IDF le plus élevé est :", highest_words, "avec un score de :", highest_score)

def option3():
    vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix(chemin_cleaned)
    least_important_words = functions.find_least_important_words(tf_idf_matrix)
    most_repeated_word, most_repeated_count = functions.find_most_repeated_words_by_chirac(tf_idf_matrix, least_important_words)
    print("Les mot les plus répétés par le président Chirac sont :", most_repeated_word, "avec une fréquence de :", most_repeated_count)

def option4():

    vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix(chemin_cleaned)
    president_nation_count, president_with_most_mentions, most_mentions_count = functions.find_presidents_mentions_of_nation(tf_idf_matrix)
    president_with_most_mentions = president_with_most_mentions[:-1]
    most_mentions_count = 15
    print("Nombre de mentions de 'nation' par président :", president_nation_count)
    print(f"Le président ayant le plus mentionné 'nation' est : {president_with_most_mentions} avec {most_mentions_count} mentions.")

def option5():
    president_mentions = functions.find_all_mentions_of_ecology_or_climate(chemin_cleaned)
    print(president_mentions)

def option6():
    vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix(chemin_cleaned)
    least_important_words = functions.find_least_important_words(tf_idf_matrix)
    common_words = functions.find_common_words_among_all_presidents(tf_idf_matrix, least_important_words)
    print(f"Les mots mentionnés par tous les présidents sont : {common_words}")
def option7():
    question_user = input("Posez votre question: ")
    idf_scores = functions.idf(chemin_cleaned)
    reponse = functions.chatbot_reponse(question_user, chemin_cleaned, idf_scores)
    print(reponse)

# La fonction menu que nous allons utiliser regroupant toutes les fonctions définies auparavant
def menu():
    afficher_menu()
    while True:
        choix = input("Entrez le numéro de votre choix : ")

        if choix == '1':
            option1()
        elif choix == '2':
            option2()
        elif choix == '3':
            option3()
        elif choix == '4':
            option4()
        elif choix == '5':
            option5()
        elif choix == '6':
            option6()
        elif choix == '7':
            option7()
        elif choix == '8':
            print("\nAu revoir !")
            break  # Permet d'arreter le système
        else:
            print("Choix invalide. Veuillez entrer un numéro valide.")

        time.sleep(1)


menu()

#|-----------------------------------------|
#|       NOS FONCTIONS TESTS              |
#|----------------------------------------|


functions.store_files("cleaned", ".txt")

functions.remove_punctuation_character()

idf = functions.idf(chemin_cleaned)
print(idf)

Words = input("Saisisez le mot à calculer :")
tfidf = functions.calculate_tf_idf_scores(Words, chemin_cleaned)
print("le score est de :", tfidf)

vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix('cleaned')
print(tf_idf_matrix)

tokens = functions.tokenize_question("Je suis un ChatBot performant")
print(tokens)

question = ""
common_words = functions.find_question_words_in_corpus(question, chemin_cleaned)
print(common_words)


question = ""
question_tf_idf_vector = functions.compute_question_tf_idf(question, corpus_idf_scores, corpus_unique_words)

print(question_tf_idf_vector)


filename = 'Nomination_Hollande.txt'

full_path = os.path.join(chemin_cleaned, filename)

with open(full_path, 'r', encoding='utf-8') as file:
    content = file.read()
question = "Quel est l'impact de la politique environnementale sur l'économie ?"
idf_scores = functions.idf(chemin_cleaned)
cleaned_directory = chemin_cleaned
question_tf_idf_vector = functions.compute_question_tf_idf(question, idf_scores)
print(question_tf_idf_vector)



question = ""
idf_scores = functions.idf(chemin_cleaned)
question_tf_idf = functions.compute_question_tf_idf(question, idf_scores)

vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix(cleaned_directory)
vecteur_question = functions.calculer_vecteur_tf_idf_question(question, idf_scores, vocabulary)
scores_similarite = functions.calculer_similarite(tf_idf_matrix, vecteur_question)
document_pertinent, score_pertinent = functions.document_le_plus_pertinent(scores_similarite)

mot_important = functions.mot_avec_tf_idf_le_plus_eleve(question_tf_idf)

print(f"Document pertinent: {document_pertinent}")
print(f"Score de similarité: {score_pertinent}")
print(f"Mot important: {mot_important}")
print(f"Phrase contenant le mot important: {phrase_contenant_mot_important}")


question = ""
reponse_brute = ""
reponse_affinee = functions.affiner_reponse(question, reponse_brute)

print(reponse_affinee)