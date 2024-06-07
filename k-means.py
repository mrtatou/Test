import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import PIL
import random

file = np.copy(PIL.Image.open('Terre rouge.jpg', mode='r'))

def init_couleurs(image, nombre_couleurs):

    taille = file.shape
    hauteur = taille[0] # nombre de lignes
    largeur = taille[1] # nombre de colonnes
    
    coordonnees_couleurs=np.empty((nombre_couleurs, 2)) #Sera utilisé plus tard pour avoir des clusters éloignés (weight les probabilités de répartition proportionnellement à la distance aux autres clusters)
    #random semble pas pouvoir faire ça très bien, utilisant random.choice(population, weights) et on va éviter de calculer la distance à tous les clusters pour tous les pixels de l'image pour la proba...
    couleurs = np.empty((nombre_couleurs, 3)) #Array contenant nombre_couleurs valeurs (R,G,B)
    
    # Boucle de génération des couleurs initiales
    for i in range(nombre_couleurs):
        rand_row = random.randint(0,hauteur)
        rand_col = random.randint(0,largeur)
        coordonnees_couleurs[i] = [rand_row, rand_col]
        for j in range(i):
            if np.sqrt( (rand_row - coordonnees_couleurs[i][0])**2 + (rand_col - coordonnees_couleurs[i][1])**2) <=  0: #valeur arbitraire de distance pour l'instant vide, pour que les clusters soient éloignés un minimum.
                j=i-2 #arrête la boucle actuelle après cette itération
                i=i-1 #redescend i pour générer de nouvelles coordonnees
        
    couleurs[i] =image[rand_row,rand_col]

    return (coordonnees_couleurs, couleurs)
