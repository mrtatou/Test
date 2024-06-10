import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import PIL
import random
import sys


assert(len(sys.argv)==2)
file = np.copy(PIL.Image.open(sys.argv[1], mode='r'))

taille = file.shape
hauteur = taille[0] # nombre de lignes
largeur = taille[1] # nombre de colonnes

def distance(x1:int , x2:int , y1:int , y2:int ): #simple calcul de distance
    return np.sqrt((x1-x2)**2+(y1-y2)**2)


def min_list(l):
    mini = 0
    for k in range(1,len(l)):
        if l[k]<l[mini]:
            mini=k

def init_couleurs(image, nombre_couleurs):
    
    coordonnees_couleurs=np.empty((nombre_couleurs, 2)) #Sera utilisé plus tard pour avoir des clusters éloignés (weight les probabilités de répartition proportionnellement à la distance aux autres clusters)
    #random semble pas pouvoir faire ça très bien, utilisant random.choice(population, weights) et on va éviter de calculer la distance à tous les clusters pour tous les pixels de l'image pour la proba...
    couleurs = np.empty((nombre_couleurs, 3)) #Array contenant nombre_couleurs valeurs (R,G,B)
    
    # Boucle de génération des couleurs initiales
    for i in range(nombre_couleurs):
        ligne_aleatoire = random.randint( 0, hauteur)
        colonne_aleatoire = random.randint(0, largeur)
        coordonnees_couleurs[i] = [ ligne_aleatoire, colonne_aleatoire ]
        couleurs[i] = image[ ligne_aleatoire ] [ colonne_aleatoire ]
        for j in range(i):
            if distance( colonne_aleatoire, coordonnees_couleurs[i][1], ligne_aleatoire, coordonnees_couleurs[i][0] ) <=  np.sqrt(50): #valeur arbitraire de distance pour l'instant vide, pour que les clusters soient éloignés un minimum.
            #Ici sqrt(50) car il s'agit de la diagonale d'un carré de 5 pixels par 5 pixels
                j=i-2 #arrête la boucle actuelle après cette itération
                i=i-1 #redescend i pour générer de nouvelles coordonnees
    
    return [couleurs, coordonnees_couleurs]


def update_couleurs(image, couleurs, coordonnees_couleurs, nb_iter):
    
    for i in range(nb_iter):
        
        for ligne in range(hauteur):
            for colonne in range(largeur): # j'avoue avoir du mal à comprendre le programme de base, dont je comprends qu'il semble faire un calcul de norme sur les couleurs?
                couleurs_proches=[]
                for k in coordonnees_couleurs: #On regarde de quelle couleur le pixel est le plus proche
                    dist= distance(k[0],ligne, k[1], colonne)
                    couleurs_proches.append(dist)
                
                couleur_la_plus_proche=min_list(couleurs_proches) #indice de la couleur la plus proche, dont on pourra alors chercher les valeurs rgb

                
                
                

#couleurs_initiales=init_couleurs(image)
#update_couleurs(image, couleurs_initiales[0], couleurs_initiales[1], 20)
print(init_couleurs(file, 12))
