import matplotlib.pyplot as plt
import numpy as np
import PIL
import random
import sys

assert(len(sys.argv)==5)

file = np.copy(PIL.Image.open(sys.argv[1], mode='r')) #On ouvre l'image sous forme de matrice, copiée dans la variable file
nb_couleurs= int(sys.argv[2])
nb_iter= int(sys.argv[3])
type_fichier = int(sys.argv[4]) # 0 pour YCbCr; 1 pour RGB; 2 pour RGBA


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
    return mini




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
    
    return couleurs #pertinence du renvoi de coordonnees_couleurs remise en question une fois de plus


def update_couleurs(image, couleurs, nb_iter):
    liste = [ [] for i in couleurs]
    for i in range(nb_iter):
        
        for ligne in range(hauteur):
            for colonne in range(largeur):
                couleurs_proches=[]
                pixel=image[ligne][colonne]
                for k in couleurs: #On cherche de quelle couleur prédéfinie le pixel se rapproche le plus
                    dist= np.sqrt(sum((pixel[i]-k[i])**2 for i in range(3))) #en comparant la "distance" aux couleurs précédemment définies, selon l'écart à la valeur r, g et b de chacune d'entre elles
                    couleurs_proches.append(dist) #le range 3 est un peu douteux parce que quand on fera sur d'autres trucs (ex la compression sur la chrominance) ce sera plus 3
                #Faut virer cette liste là
                couleur_la_plus_proche=min_list(couleurs_proches) #renvoie l'indice de la couleur la plus proche
                liste[couleur_la_plus_proche].append([pixel]) #On ajoute la couleur du pixel à l'indice de la couleur la plus proche
                #liste c'est une liste... de listes (1 par couleur)... de listes à 3 éléments (les pixels assimilés à cette couleur)
        
        for k in range(len(couleurs)):
            couleurs[k]= np.mean(liste[k], axis = 0)  #Modification des couleurs vers la moyenne des couleurs des pixels qui lui ont été associés
            #fonction np.mean utilisée pour plus d'adaptabilité, par exemple quand on traitera que 2 coordonnées (CrB, CrR)
    return couleurs
                
#Une fois les couleurs définies et mises à jour plusieurs fois sur la base des couleurs présentes dans l'image,
#on peut désormais réduire l'image à ces couleurs.

def update_image( image, couleurs):
    for ligne in range(hauteur):
        for colonne in range(largeur):
            #On refait en fait la même chose que dans la fonction update...
            couleurs_proches=[]
            pixel=image[ligne][colonne]
            for k in couleurs: 
                dist= np.sqrt(sum((pixel[i]-k[i])**2 for i in range(type_fichier+2))) 
                couleurs_proches.append(dist) 
            couleur_la_plus_proche=min_list(couleurs_proches)
            image[ligne][colonne]=couleurs[couleur_la_plus_proche]
    return image

                
#Il n'y a plus qu'à adapter le programme à d'autres "découpages" de l'image (RGBA, Chrominances) et à essayer de l'optimiser, peut-être.
#Note: actuellement le programme semble très lent, à tester sur différentes configurations matérielles.
#Note 2 - après test sur le pc perso - ça mange de la mémoire en quantité non négligeable (test sur une image de dimension 1920x1080, 40 couleurs et 20 itérations, le résultat est visible sur l'accueil du repo - test arrêté à la main avant de voir la totalité de ma mémoire mangée par le programme)

couleurs_initiales =init_couleurs(file, 12)
nouvelles_couleurs=update_couleurs(file,couleurs_initiales,nb_iter)
nouvelle_image=update_image(file,nouvelles_couleurs)
plt.imsave("compressed.jpg", nouvelle_image)
