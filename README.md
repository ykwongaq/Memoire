Ce répertoire GitHub a été créé dans le cadre de mon mémoire intitulé "Étude de l’effet de la complexité du récif corallien de Polynésie française sur les communautés d'invertébrés par la technique de photogrammétrie". 
Il a pour objectif de rendre disponibles les codes R et Python que j'ai utilisé pour la collecte et l'analyse des données sur la diversité des invertébrés et la complexité structurelle des coraux de Polynésie Française.

Le script python "début" a été utilisé pour l'alignement des photos. Le script "suite" a, quant à lui, été utilisé pour générer le nuage de point dense, construire le maillage, appliquer la texture et remplir les trous. Enfin le script "fin" a été utilisé créer le DEM et l'orthomosaïque puis exporter les DEM en format GeoTIFF. Pour les étapes mannuelles, se référer au document "Protocole modèle 3D Agisoft". 

Les métriques de complexités ont été générées avec le code R s'intitulant "code_metriques_complexites". 

L'analyse des variables de compléxités et de diversités ont été réalisées sur Rstudio version 2023.12.1. avec trois codes différents : "code_diversite", "analyse_complexites" et "code_complexite_diversite". 
