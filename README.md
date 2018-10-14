myks-bank
=========

Objectifs
---------

Cet outil extrait les lignes des relevés de compte et les catégorise.

Il est conçu pour mon usage personnel en local et n'inclut aucune sécurité.

Utilisation
-----------

Mettre dans .env :

    PYTHONPATH=path/to/myks-bank
    DJANGO_SETTINGS_MODULE=bank.settings
    DJANGO_SECRET_KEY=<une chaîne aléatoire et secrète>

Créer la base de données :

    django-admin migrate

Lancer le serveur :

    django-admin runserver

Créer des catégories et des règles de catégorisation dans l'interface web.

Importer un relevé :

    django-admin import_lcl_statement < $file.pdf
