-- Créer une nouvelle base de données appelée "weather_data"
CREATE DATABASE weather_data;

-- Se connecter à la base de données "weather_data"
\c weather_data;


-- Créer une table pour stocker les données météo
CREATE TABLE weather (
    id SERIAL PRIMARY KEY,                 -- Identifiant unique auto-incrémenté
    city VARCHAR(50) NOT NULL,             -- Nom de la ville
    date DATE NOT NULL,                    -- Date des données météo
    temperature_min NUMERIC(5, 2),         -- Température minimale (en degrés Celsius)
    temperature_max NUMERIC(5, 2),         -- Température maximale (en degrés Celsius)
    humidity NUMERIC(5, 2),                -- Taux d'humidité (en %)
    wind_speed NUMERIC(5, 2),              -- Vitesse du vent (en m/s)
    weather_condition VARCHAR(100),        -- Description des conditions météorologiques
    created_at TIMESTAMP DEFAULT NOW()     -- Timestamp indiquant quand l'enregistrement a été inséré
);


-- Afficher la structure de la table "weather"
\d weather;
