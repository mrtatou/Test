Je teste ici le fonctionnement de git, afin de sauvegarder sur github mon projet de TIPE et pouvoir y accéder facilement.\
TIPE pour l'instant largement inspiré de : https://towardsdatascience.com/clear-and-visual-explanation-of-the-k-means-algorithm-applied-to-image-compression-b7fdc547e410\

Premiers tests... pas très concluants.\
![Yup, works just as intended](https://github.com/mrtatou/Test/assets/100464038/2a1ff18d-c39e-44af-9d04-802d3a3e62d6)

Après modifications, le programme a une consommation mémoire raisonnable et peut compresser des images de taille usuelle (exemple: image de taille 1920x1200 réduit à 12 couleurs en 10 itérations)\
![compressed2](https://github.com/mrtatou/Test/assets/100464038/4eb6c8de-8bbd-44ec-a384-014009a4c3c8)
<sub>source de l'image originale: l'un des fonds d'écran windows 10 par défaut</sub>
\
\
En revanche une très grande image en format vertical (3472x4624) s'est retrouvée tournée à 90°, étrange
![Do a flip!](https://github.com/mrtatou/Test/assets/100464038/206eca93-c66d-4077-a03c-226faff9c812)
