# Projet ETL : Airflow, PostgreSQL et Grafana

## Description du projet

Ce projet est un pipeline ETL (Extract, Transform, Load) qui récupère des données météorologiques en temps réel via l'API **OpenWeatherMap** pour la ville de Paris. Les données extraites sont ensuite transformées et chargées dans une base de données PostgreSQL. Enfin, des tableaux de bord interactifs sont créés à l'aide de **Grafana** pour visualiser les données météorologiques. 

Les principales fonctionnalités incluent :
- Extraction des données météorologiques (températures, humidité, conditions météo, etc.)
- Transformation des données pour extraire uniquement les champs nécessaires
- Chargement des données dans une base de données PostgreSQL
- Visualisation des données via Grafana

## Instructions d'installation

Pour installer ce projet, vous devez avoir [Docker](https://www.docker.com/get-started) et [Docker Compose](https://docs.docker.com/compose/install/) installés sur votre machine.

### 1. Cloner le dépôt

```bash
git clone https://github.com/elhassane1230/projet-ETL-Airflow-PostgreSQL-Grafana.git
cd projet-ETL-Airflow-PostgreSQL-Grafana
```
### 2. Configurer l'API OpenWeatherMap
- Inscrivez-vous sur OpenWeatherMap et récupérez votre clé API.
- Ouvrez le fichier Python où se trouve l'API (dans votre DAG Airflow) et remplacez la clé API par la vôtre :
  ```bash
  API_KEY = 'VOTRE_CLE_API'
  ```
- Créez un fichier .env à la racine du projet avec votre clé API OpenWeatherMap :
  ```bash
  echo "API_KEY=<votre_clé_API_OpenWeatherMap>" > .env
  ```
### 3. Démarrez les services avec Docker Compose :
```bash
  docker-compose up -d
  ```
Cela démarrera les services suivants :

 - Airflow (Scheduler, Webserver) : pour orchestrer le pipeline ETL.
 - PostgreSQL : pour stocker les données météorologiques.
 - Adminer : pour gérer la base de données PostgreSQL via une interface web.
 - Grafana : pour visualiser les données.

## Instructions pour exécuter le projet : 
### 1. Accédez à l'interface Airflow à http://localhost:8080.
 #### - dentifiants :
         - Utilisateur : airflow
         - Mot de passe : airflow

### 2. Activez le DAG : 
    - weather_etl et exécutez-le manuellement ou laissez-le s'exécuter automatiquement selon sa planification (par heure).
    - Une fois le pipeline exécuté, les données seront insérées dans PostgreSQL.
## Utilisation d'Adminer:
### 1. Accédez à Adminer à http://localhost:8081.
  #### -Identifiants :
        - Serveur : postgres
        - Utilisateur : postgres
        - Mot de passe : postgres
        - Base de données : weather_db

### 2. Vérifiez les données :
        - Sélectionnez la table weather pour visualiser les données météorologiques insérées par le pipeline ETL.
        - Vous pouvez également exécuter des requêtes SQL pour analyser les données.

## Informations sur les dashboards Grafana : 
### 1. Accédez à Grafana à l'adresse http://localhost:3000.
  #### Identifiants :
      - Utilisateur : admin
      - Mot de passe : admin
### 2. Importez les dashboards : 
  - Allez dans le menu principal et sélectionnez "Dashboards" > "Manage".
  - Cliquez sur "Import" et utilisez le fichier JSON de votre dashboard local ou entrez l'URL si vous avez des dashboards en ligne.
  - Suivez les instructions pour l'importation, en spécifiant la source de données (PostgreSQL) créée précédemment.
### 3. Visualisez les dashboards :
  - Une fois importés, vous pouvez accéder aux dashboards sous l'onglet "Home".
  - Les visualisations comprennent :
       - Températures (min, max) pour la ville choisie.
       - Humidité et vitesse du vent en temps réel.
       - Tendances météorologiques (moyennes, variations) sur plusieurs jours.
## Informations sur l'API utilisée : 
  - Ce projet utilise l'API OpenWeatherMap pour collecter les données météorologiques. Les données extraites incluent :
       - Ville : Paris
       - Température (min, max)
       - Humidité
       - Vitesse du vent
       - Condition météorologique

 - L'API est appelée avec les paramètres suivants :

       - API_KEY : Clé API OpenWeatherMap
       - CITY : Paris

 - Pour plus d'informations sur l'API, consultez la documentation officielle d'OpenWeatherMap.
