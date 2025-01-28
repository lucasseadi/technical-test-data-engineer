# Réponses du test

## _Utilisation de la solution (étape 1 à 3)_

<p>
Vous trouverez ci-dessous la documentation technique du module moovitamix_dailyfeed.

Pour exécuter les tests, utilisez python -m pytest .\test\{test_file}.py</p>

### moovitamix_dailyfeed package

### Submodules

#### moovitamix_dailyfeed.fetch_data module

#### Module for fetching data from Moovitamix API

#### async moovitamix_dailyfeed.fetch_data.fetch_data(method: str) → List[Dict[str, Any]] | None[source]
Function fetching data

#### async moovitamix_dailyfeed.fetch_data.fetch_paginated_data(method: str) → List[Dict[str, Any]] | None[source]
Function fetching paginated data

#### moovitamix_dailyfeed.main module

#### moovitamix_dailyfeed.main.graceful_shutdown() -> None
Function to flush logs when application is interrupted

#### moovitamix_dailyfeed.main.log_config() -> None
Function to config logs

#### moovitamix_dailyfeed.main.main() -> None
Data feed main function

#### moovitamix_dailyfeed.storage module
Module for storing data retrieved from API

#### moovitamix_dailyfeed.storage.update_storage(key: str, data: List[Dict[str, Any]] | None) → None[source]
Function for updating database object

## Questions (étapes 4 à 7)

### Étape 4

<p>
J'utiliserais un schéma à trois tables similaire au format de données reçu de l'API : table TRACKS, table USERS et table LISTEN_HISTORY.</p>
Table TRACKS : track_id (clé primaire), nom, artiste, auteurs-compositeurs, durée, genres, album, created_at, updated_at</p>
Table USERS : user_id (clé primaire), first_name, last_name, email, gender, favorite_genres, created_at, updated_at</p>
Table LISTEN_HISTORY : user_id (clé étrangère), items (liste de track_id (clé étrangère)), created_at, updated_at</p>
Je recommanderais d'utiliser MongoDB hébergé dans AWS S3. Mongo est bien adapté, car l'application a besoin d'une récupération rapide et n'est pas aussi préoccupée par la cohérence des données, c'est donc un compromis équitable. S3 est une bonne solution d'hébergement car elle est élastique et redondante, et nous nous attendons à ce que la quantité de données renvoyées par l'API augmente au fil du temps même si nous ne conservons pas de données historiques.</p>

### Étape 5

<p>
J'utiliserais une combinaison des journaux générés quotidiennement et un rapport de type Grafana pour le code d'ingestion de données et CloudWatch pour la base de données. Les indicateurs clés incluraient le temps d'exécution, le nombre d'enregistrements de base de données, le temps de latence de l'API, le nombre total d'appels d'API pour l'exécution, le nombre d'appels d'API ayant échoué.
</p>

### Étape 6

<p>
Pour le calcul des recommandations, je mettrais en place une approche de filtrage collaborative basée sur la similarité cosinus entre les utilisateurs. Elle calculerait la similarité entre les utilisateurs ayant des éléments communs (track_id, artiste, album, auteurs-compositeurs, genres) pour classer les chansons et renvoyer les plus probables. 
</p>
<p>
Un aspect à prendre en compte serait d’équilibrer les chansons qui ne sont pas dans l’historique des pistes de l’utilisateur avec celles qui le sont, de sorte que la recommandation serait un mélange de favoris et de découvertes.
</p>

### Étape 7

<p>J'effectuerais des tests hebdomadaires réguliers mesurant des indicateurs de performance tels que l'exactitude, la précision et le rappel. Lorsque ces indicateurs se détériorent en dessous d'un certain seuil (80 % par exemple), le modèle doit être réentraîné.
<p>Une option serait de mettre en œuvre la Retrieval-Augmented Generation pour ralentir la dégradation des données et rendre le réentraînement plus rare.</p>

