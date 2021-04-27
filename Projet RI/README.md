# Projet TAL
## Introduction
Il s'agit ici d'un court résumé de ce qui a été fait dans les différents TMEs et les tests réalisés.  
## TME1-Indexation
La grande partie du travail efféctué à été placé dans le code collection.py et les tests dans le code test_indexation.py.   
Le parser récupère toutes les informations disponibles dans les fichiers et les stockes dans des objects Document.  
Nous avons ajouté la possibilité d'ajouté sa propre liste de stopwords pour l'indexation.  
De plus nous avons ajouté une fonction getIDFsForStem.   
Pour la vérification de l'indexation nous utilisons l'exemple donnée dans le TME,  
nous vérifions aussi la cohérence entre TF-IDFs des documents et des termes qui donnent bien les mêmes valeurs (certaines vérifiées à la main).
De même pour les TFs.  
De plus nous avons tester la cohérence avec les TFs et IDFs des termes que nous renvoyons avec les TF-IDFs calculés.  
Durant nos tests nous avons observé un bug dans TextRepresenter que nous avons corrigé. 
En effet si un mot apparaissait sous 2 formes différentes mais avec un même stem il n'apparaissait qu'une fois pour le stemmer.
## TME2-Appariement
Les modèles sont codés dans le code modeles.py et les weighters dans le code weighters.py, 
la totalité des modèles sont opérationnels.  
Le modèle de langue est inspiré du code [ici](https://github.com/prdx/RetrievalModels/tree/master/models) (on passe le modèle au log ici).
Il existe 2 fichiers de tests :  
- test_modeles.py qui test la cohérence des résultats obtenus dans l'application réel en affichant la requète avec le meilleurs score pour une query avec les différents models.  
Nous utilisons aussi ces tests pour verifier la rapidité du ranking (il est de l'ordre de 0.1 seconde, ce qui est très bon).
- test_modeles_results.py qui vérifie les résultats obtenues sur une collection réduite et une query prédéfinie.  
Nous avons réalisé de plus réalisé le bonus pour obtenir les meilleurs paramètres de nos modèles.  
## TME3-Evaluation

## TME4-Algorithme de PageRank
## Répartition du travail
TME1-Indexation Code : Luc STERKERS - Dao THAUVIN   
TME1-Indexation Tests : Dao THAUVIN   
TME2-Appariement Code : Luc STERKERS - Dao THAUVIN    
TME2-Appariement Tests : Dao THAUVIN  
TME2-Appariement Bonus : Dao THAUVIN    
TME3-Evaluation Code : Luc STERKERS - Dao THAUVIN  
TME3-Evaluation Tests : Dao THAUVIN  
TME3-Evaluation Bonus : Luc STERKERS  
TME4-Algorithme de PageRank Code : Luc STERKERS  
TME4-Algorithme de PageRank Tests : Luc STERKERS  
