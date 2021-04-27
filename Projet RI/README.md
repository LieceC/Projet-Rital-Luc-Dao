#Projet TAL
##Introduction
Il s'agit ici d'un cour résumé de ce qui a été fait dans les différents TMEs et les tests réalisés.  
##TME1-Indexation
La grande partie du travail efféctué à été placé dans le code collection.py et les tests dans le code test_indexation.   
Le parser récupère toutes les informations disponibles dans les fichiers et les stockes dans des objects Document.  
Nous avons ajouté la possibilité d'ajouté sa propre liste de stopwords pour l'indexation.  
De plus nous avons ajouté une fonction getIDFsForStem.   
Pour la vérification de l'indexation nous utilisons l'exemple donnée dans le TME,  
nous vérifions aussi la cohérence entre TF-IDFs des documents et des termes qui donnent bien les mêmes valeurs (certaines vérifiées à la main).
De même pour les TFs.  
De plus nous avons tester la cohérence avec les TFs et IDFs des termes que nous renvoyons avec les TF-IDFs calculés.  
Durant nos tests nous avons observé un bug dans TextRepresenter que nous avons corrigé. 
En effet si un mot apparaissait sous 2 formes différentes mais avec un même stem il n'apparaissait qu'une fois dans le tf.
##TME2-Appariement