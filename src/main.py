# On importe les fonctions et la fonction time que nous allons utiliser pour notre menu
import functions
import time

matrix = functions.m
print(matrix)


# Le menu utilisateur
def afficher_menu():
    print("############")
    print("# ChatBot  #")
    print("############")
    time.sleep(1)
    # Les différentes options pour les utilisateurs
    print("1. Afficher la liste des mots les moins importants")
    print("2. Afficher les mots ayant le score TF-IDF le plus élevé")
    print("3. Afficher les mots les plus répétés par le président Chirac")
    print(
        """4. Afficher les noms des présidents qui ont parlé de la "Nation" et de celui qui l'a répété le plus de fois""")
    print("5. Affiche le premier président à parler du climat et de l'écologie")
    print("6. Affiche les mots que tous les présidents ont évoqués")
    print("7. Quitter")


def option1():
    print("voici les mots avec les plus bas score")
    opt1 = moinsimportant("C:\AppData\chatbot\speeches\cleaned")
    print(opt1)


def option2():
    print("voici le mot avec le plus haut score : ")
    opt2 = highest_score("C:\AppData\chatbot\speeches\cleaned")
    print(opt2)


def option3():
    opt3 = chirac_repetition("CC:\AppData\chatbot\speeches\cleaned")
    print(opt3)


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
            option3()
        elif choix == '5':
            option3()
        elif choix == '6':
            option3()
        elif choix == '7':
            print("\nAu revoir !")
            break  # Permet d'arreter le système
        else:
            print("Choix invalide. Veuillez entrer un numéro valide.")

        time.sleep(1)


menu()

extraire_nom = extraction()
print(extraire_nom)

name = president(list_of_files("speeches", ".txt"))
print(name)

number = cancel_number(name)
print(number)

noduplicate = duplicate_filter(number)
print(noduplicate)

prenom = first_name(noduplicate)
print(prenom)

directory_exist("C:\AppData\chatbot\speeches")

cleaned = cleaned("C:\AppData\chatbot\speeches")
print(cleaned)

store_files("cleaned", ".txt")

remove_punctuation_character()
idf = idf("C:\AppData\chatbot\speeches\cleaned")
print(idf)

Words = input("Saisisez le mot à calculer :")
tfidf = calculate_tf_idf_scores(Words, "C:/users/User\Desktop\chatbot\cleaned")
print("le score est de :", tfidf)

matrix = matrice_tf_idf("C:\AppData\chatbot\speeches\cleaned")
print(matrix)

fnct1 = moinsimportant("C:\AppData\chatbot\speeches\cleaned")
print(fnct1)
