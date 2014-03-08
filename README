lcl
===

Objectifs
---------

Cet outil extrait les lignes des relevés de compte PDF de LCL et les
enregistrer dans une base de données. Il permet aussi de les catégoriser.

Il est conçu pour mon usage personnel en local et n'inclut aucune sécurité.

Utilisation
-----------

Installer les dépendances (de préférence dans un virtualenv) :

    pip install -r REQUIREMENTS

Avant toute action (à mettre dans le postactivate du virtualenv):

    export DJANGO_SECRET_KEY='<une chaîne aléatoire et secrète>'

Créer la base de données :

    ./manage.py syncdb

Lancer le serveur :

    ./manage.py runserver

Créer des catégories et des règles de catégorisation dans l'interface web.

Importer un relevé :

    ./manage.py import_lcl_statement < $file.pdf

Sauvegarder la base de données :

    ./manage.py dumpdata > backup.json
