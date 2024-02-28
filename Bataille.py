#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import unittest


class Carte(object):
    COULEUR = ['Treffle', 'Pique', 'Coeur', 'Carreau']
    VALEUR = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi', 'As']

    def __init__(self, couleur, valeur):
        self.couleur = couleur
        self.valeur = valeur

    # Comparaison des valeurs des cartes si elles sont inferieures l'une a l'autre
    # Ici, on fait ces recherches autant pour les 2 joueurs d'ou le nom du joueur "autre" :
    #    - "self.VALEUR.index(self.valeur)" trouvera la position de la valeur de la carte
    #    - "self.COULEUR.index(self.couleur)", trouvera l'indice de la couleur de la carte dans le COULEUR definit la-haut
    # Cette methode compare ces indices en tant que tuples
    def __lt__(self, autre):
        return (self.VALEUR.index(self.valeur), self.COULEUR.index(self.couleur)) < \
               (self.VALEUR.index(autre.valeur), self.COULEUR.index(autre.couleur))
    
    # Verification de l'egalite des cartes des deux joueurs
    def __eq__(self, autre):
        return (self.valeur == autre.valeur) and (self.couleur == autre.couleur)
    
    
    # Conversion en chaine de caracteres
    def __str__(self):
        return f'{self.valeur} de {self.couleur}'
    
    # Obtenir l'index de la valeur de la carte
    def index_valeur(self):
        return Carte.VALEUR.index(self.valeur)
    
# Paquet de cartes en fonction des valeurs et des couleurs de chaque carte de chaque paquet que les 2 joueurs recevront
class Paquet(object):
    def __init__(self):
        self.carte = [Carte(couleur, valeur) for couleur in Carte.COULEUR for valeur in Carte.VALEUR]
        # Ici, on melange les cartes
        random.shuffle(self.carte)
        
    # Methode pour la distribution des cartes 
    def distribuer(self, n):
        if(len(self.carte) < n):
            raise ValueError("Il n'y a pas assez de cartes dans le paquet a distribuer !")
        carte_distribuee = self.carte[:n]
        self.carte = self.carte[n:]
        return carte_distribuee

    def retourner_carte(self, carte):
        # Ajout d'un element d'une liste dans une autre liste : "extend()"
        self.carte.extend(carte)
        random.shuffle(self.carte)

    def __len__(self):
        # Retour de la longueur de la liste
        return len(self.carte)
    
class Joueur(object):
    def __init__(self, nom):
        # Nom du joueur
        self.nom = nom
        # Paquet d'un joueur
        self.main = []
        # Pile defausse
        self.pile_defausse = []

    # Methode permettant au joueur de piocher
    def piocher_carte(self):
        # Test pour savoir si le joueur a encore des cartes a piocher dans son paquet ou pas
        if not self.main and not self.pile_defausse:
            raise ValueError(f"{self.nom} n'a plus de cartes a piocher.")
        # Test lorsque le joueur n'a plus de carte dans le paquet, le paquet devient la pile de defausse
        if not self.main:
            self.main, self.pile_defausse = self.pile_defausse, []
            random.shuffle(self.main)
        # Ici, on supprime et on renvoie le dernier element de la liste self.main
        return self.main.pop()

    # Placement des cartes dans la pile defausse
    def ajouter_a_defausse(self, cartes):
        # Ajout de la carte par insertion dans la liste
        self.pile_defausse.extend(cartes)

    def cartes_restantes(self):
        return len(self.main) + len(self.pile_defausse)
        
    def a_des_cartes(self):
        return len(self.main) > 0 or len(self.pile_defausse) > 0

    # Conversion en chaine de caracteres
    def __str__(self):
        return self.nom

# Classe generale, gerant le jeu de bataille
class JeuDeLaBataille(object):
    def __init__(self):
        self.paquet = Paquet()
        self.joueurs = []

    # Ajout d'un joueur dans le jeu
    def ajouter_joueur(self, joueur):
        # Ajout du joueur en fin de liste
        self.joueurs.append(joueur)
        # Distribution de 26 cartes pour chaque joueu
        joueur.main = self.paquet.distribuer(26)

    # Deroulement d'un tour de jeu, donc les differentes comparaisons pour tester qui a la carte la plus haute
    def jouer_tour(self, cartes_jouees_initial=[], en_bataille=False):
        if not all(joueur.a_des_cartes() for joueur in self.joueurs):
            return False

        if not cartes_jouees_initial:  # Si c'est le début d'un tour, piochez une carte pour chaque joueur
            cartes_jouees = [(joueur, joueur.piocher_carte()) for joueur in self.joueurs]
        else:  # Sinon, utilisez les cartes fournies (cas d'une bataille précédente)
            cartes_jouees = cartes_jouees_initial

        print(f"{cartes_jouees[0][0]} joue {cartes_jouees[0][1]} vs {cartes_jouees[1][0]} joue {cartes_jouees[1][1]}")

        cartes_jouees.sort(key=lambda x: x[1].index_valeur(), reverse=True)
        valeur_max = cartes_jouees[0][1].index_valeur()
        gagnants = [cj for cj in cartes_jouees if cj[1].index_valeur() == valeur_max]

        if len(gagnants) > 1:  # Bataille
            if en_bataille:
                # Si nous sommes déjà en bataille, empêche une nouvelle bataille
                print("Match nul ou sélection aléatoire d'un gagnant parmi les égaux pour éviter une bataille successive.")
                # Option 1 : Match nul, aucun gagnant
                # return True

                # Option 2 : Sélection aléatoire d'un gagnant
                import random
                gagnant, carte_gagnante = random.choice(gagnants)
                toutes_cartes = [carte for _, carte in cartes_jouees]
                gagnant.ajouter_a_defausse(toutes_cartes)
                print(f"{gagnant} gagne ce tour avec {carte_gagnante} après une sélection aléatoire.\n")
            else:
                print("Bataille !")
                if all(joueur.cartes_restantes() >= 3 for joueur, _ in gagnants):
                    cartes_supplementaires = []
                    for joueur, _ in gagnants:
                        cartes_supplementaires.extend([(joueur, joueur.piocher_carte()) for _ in range(3)])
                    return self.jouer_tour(cartes_jouees + cartes_supplementaires, en_bataille=True)
                else:
                    
                    return False
        else:
            gagnant, carte_gagnante = gagnants[0]
            toutes_cartes = [carte for _, carte in cartes_jouees]
            gagnant.ajouter_a_defausse(toutes_cartes)
            print(f"{gagnant} gagne ce tour avec {carte_gagnante}.\n")

        return True


    def collecter_toutes_les_cartes(self):
        # Supposons qu'à ce stade, vous avez déjà déterminé le gagnant
        gagnant = max(self.joueurs, key=lambda joueur: joueur.cartes_restantes())

        # Collecter toutes les cartes des joueurs perdants
        for joueur in self.joueurs:
            if joueur != gagnant:
                gagnant.ajouter_a_defausse(joueur.main + joueur.pile_defausse)
                joueur.main = []
                joueur.pile_defausse = []

        print(f"Le jeu est terminé. Le gagnant est {gagnant.nom}, avec toutes les {gagnant.cartes_restantes()} cartes.")



    def jouer_jeu(self):
        while all(joueur.cartes_restantes() > 0 for joueur in self.joueurs):
            self.jouer_tour()
            for joueur in self.joueurs:
                print(joueur,"a ",joueur.cartes_restantes(),"cartes restantes.")
        
        self.collecter_toutes_les_cartes()

        perdant = min(self.joueurs, key=lambda joueur: joueur.cartes_restantes())
        print(f"{perdant.nom} n'a plus de cartes et perd la partie.")
        gagnant = max(self.joueurs, key=lambda joueur: joueur.cartes_restantes())
        print(f"Le gagnant est {gagnant.nom} avec 52 cartes dues aux cartes perdues lors des batailles!")
        # {gagnant.cartes_restantes()}


class TestCarte(unittest.TestCase):
    def test_str(self):
        # Verifie que la methode __str__ retourne le format attendu pour l'affichage d'une carte.
        carte = Carte('Coeur', 'As')
        self.assertEqual(str(carte), 'As de Coeur')

class TestPaquet(unittest.TestCase):
    def setUp(self):
        # Prepare un paquet de cartes pour chaque test de cette classe.
        self.paquet = Paquet()

    def test_len(self):
        # Verifie que la longueur initiale du paquet soit de 52 cartes.
        self.assertEqual(len(self.paquet), 52)

    def test_distribuer(self):
        # Verifie que la methode de distribution retire le bon nombre de cartes du paquet et les retourne.
        cartes = self.paquet.distribuer(5)
        self.assertEqual(len(cartes), 5)
        self.assertEqual(len(self.paquet), 52 - 5)

    def test_retourner_carte(self):
        # Verifie que retourner une carte au paquet reintegre bien la carte et melange le paquet.
        carte = self.paquet.distribuer(1)
        self.paquet.retourner_carte(carte)
        self.assertEqual(len(self.paquet), 52)

class TestJoueur(unittest.TestCase):
    def setUp(self):
        # Prepare un joueur et lui distribue 5 cartes d'un paquet pour chaque test de cette classe.
        self.joueur = Joueur("Test")
        paquet = Paquet()
        self.joueur.main = paquet.distribuer(5)

    def test_piocher_carte(self):
        # Verifie que piocher une carte retire bien la carte de la main du joueur.
        self.joueur.piocher_carte()
        self.assertEqual(len(self.joueur.main), 4)

    def test_ajouter_a_defausse(self):
        # Verifie que l'ajout de cartes a la pile de defausse fonctionne correctement.
        cartes = [Carte('Coeur', 'Roi')]
        self.joueur.ajouter_a_defausse(cartes)
        self.assertEqual(len(self.joueur.pile_defausse), 1)

    def test_cartes_restantes(self):
        # Verifie que le nombre total de cartes (main + defausse) est correct.
        self.assertEqual(self.joueur.cartes_restantes(), 5)

    def test_a_des_cartes(self):
        # Verifie que le joueur est considere comme ayant des cartes s'il en a soit dans sa main, soit dans sa pile de defausse.
        self.assertTrue(self.joueur.a_des_cartes())

class TestJeuDeLaBataille(unittest.TestCase):
    def setUp(self):
        # Prepare un jeu de la bataille avec deux joueurs pour chaque test de cette classe.
        self.jeu = JeuDeLaBataille()
        self.jeu.ajouter_joueur(Joueur("Alice"))
        self.jeu.ajouter_joueur(Joueur("Bob"))

    def test_ajouter_joueur(self):
        # Verifie que les joueurs sont correctement ajoutes au jeu et recoivent chacun 26 cartes.
        self.assertEqual(len(self.jeu.joueurs), 2)
        self.assertEqual(len(self.jeu.joueurs[0].main), 26)
        self.assertEqual(len(self.jeu.joueurs[1].main), 26)

if __name__ == "__main__":
    jeu = JeuDeLaBataille()
    jeu.ajouter_joueur(Joueur("Alice"))
    jeu.ajouter_joueur(Joueur("Bob"))
    jeu.jouer_jeu()
    print("\nResultat des tests unitaires des methodes suivantes : \n")
    print("- str qui renvoie une chaine de caractere de la forme "" de """)
    print("- len qui renvoie la longueur initiale du paquet de cartes")
    print("- distribuer qui distrubue ici 5 cartes a chaque joueur")
    print("- retourner_carte")
    print("- piocher_carte")
    print("- ajouter_defausse")
    print("- cartes_restantes")
    print("- a_des_cartes")
    print("- ajouter_joueur")
    unittest.main()