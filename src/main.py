# On importe les fonctions et la fonction time que nous allons utiliser pour notre menu
import functions
import time

# Le menu utilisateur
def afficher_menu():
    print("|----------------|")
    print("|    ChatBot     |")
    print("|----------------|")
    time.sleep(1)
    # Les différentes options pour les utilisateurs
    print("1. Afficher la liste des mots les moins importants")
    print("2. Afficher les mots ayant le score TF-IDF le plus élevé")
    print("3. Afficher les mots les plus répétés par le président Chirac")
    print("""4. Afficher les noms des présidents qui ont parlé de la "Nation" et de celui qui l'a répété le plus de fois""")
    print("5. Affiche le premier président à parler du climat et de l'écologie")
    print("6. Affiche les mots que tous les présidents ont évoqués")
    print("7. Quitter")


def option1():
    vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix('C:/Users/antpe\OneDrive\Documents\GitHub\chatbot\src\cleaned')
    least_important_words = functions.find_least_important_words(tf_idf_matrix)
    print("Les mots les moins importants sont :", least_important_words)

def option2():
    vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix('C:/Users/antpe\OneDrive\Documents\GitHub\chatbot\src\cleaned')
    highest_words, highest_score = functions.find_highest_tf_idf_words(tf_idf_matrix)
    print("Le mot avec le score TF-IDF le plus élevé est :", highest_words, "avec un score de :", highest_score)

def option3():
    vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix('C:/Users/antpe\OneDrive\Documents\GitHub\chatbot\src\cleaned')
    least_important_words = functions.find_least_important_words(tf_idf_matrix)
    most_repeated_word, most_repeated_count = functions.find_most_repeated_words_by_chirac(tf_idf_matrix, least_important_words)
    print("Le mot le plus répété par le président Chirac est :", most_repeated_word, "avec une fréquence de :", most_repeated_count)

def option4():

    vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix('C:/Users/antpe\OneDrive\Documents\GitHub\chatbot\src\cleaned')
    president_nation_count, president_with_most_mentions, most_mentions_count = functions.find_presidents_mentions_of_nation(tf_idf_matrix)
    print("Nombre de mentions de 'nation' par président :", president_nation_count)
    print(f"Le président ayant le plus mentionné 'nation' est : {president_with_most_mentions} avec {most_mentions_count} mentions.")

def option5():
    cleaned_directory = 'C:/Users/antpe\OneDrive\Documents\GitHub\chatbot\src\cleaned'
    first_president, speech_file = functions.find_first_mention_of_ecology_or_climate(cleaned_directory)
    if first_president:
        print(f"Le premier président à parler du climat ou de l'écologie est {first_president} dans le fichier {speech_file}.")
    else:
        print("Aucune mention du climat ou de l'écologie trouvée dans les discours.")

def option6():
    vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix('C:/Users/antpe\OneDrive\Documents\GitHub\chatbot\src\cleaned')
    least_important_words = functions.find_least_important_words(tf_idf_matrix)
    common_words = functions.find_common_words_among_all_presidents(tf_idf_matrix, least_important_words)
    print(f"Les mots mentionnés par tous les présidents sont : {common_words}")


# Permet d'afficher une animation de chargement
def afficher_animation():
    loading = "..."
    for i in range(10):
        time.sleep(0.5)
        print("\r▂ ▃ ▄ ▅ ▆ ▇", "Chargement", loading[: (i % len(loading)) + 1], "▇ ▆ ▅ ▄ ▂", end='')


# La fonction menu que nous allons utiliser regroupant toutes les fonctions définies auparavant
def menu():
    afficher_menu()
    while True:
        choix = input("Entrez le numéro de votre choix : ")

        if choix == '1':
            # afficher_animation()
            option1()
        elif choix == '2':
            # afficher_animation()
            option2()
        elif choix == '3':
            #  afficher_animation()
            option3()
        elif choix == '4':
            option4()
        elif choix == '5':
            option5()
        elif choix == '6':
            option6()
        elif choix == '7':
            print("\nAu revoir !")
            break  # Permet d'arreter le système
        else:
            print("Choix invalide. Veuillez entrer un numéro valide.")

        time.sleep(1)


menu()

'''extraire_nom = functions.extraction()
print(extraire_nom)

name = functions.president(functions.list_of_files("speeches", ".txt"))
print(name)

number = functions.cancel_number(name)
print(number)

noduplicate = functions.duplicate_filter(number)
print(noduplicate)

prenom = functions.first_name(noduplicate)
print(prenom)

functions.directory_exist("C:/Users/antpe\OneDrive\Documents\GitHub\chatbot\src\speeches")

cleaned = functions.cleaned("C:/Users/antpe\OneDrive\Documents\GitHub\chatbot\src\speeches")
print(cleaned)

functions.store_files("cleaned", ".txt")

functions.remove_punctuation_character()

idf = functions.idf("C:/Users/antpe\OneDrive\Documents\GitHub\chatbot\src\cleaned")
print(idf)

Words = input("Saisisez le mot à calculer :")
tfidf = functions.calculate_tf_idf_scores(Words, "C:/Users/antpe\OneDrive\Documents\GitHub\chatbot\src\cleaned")
print("le score est de :", tfidf)

vocabulary, tf_idf_matrix = functions.build_tf_idf_matrix('cleaned')
print(tf_idf_matrix)
'''