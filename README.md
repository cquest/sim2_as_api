# micro-API SIM2

Ce projet implémente une API minimale pour requêter les données SIM2 de Météo-France stockées dans une base locale postgresql.

## Prérequis

Ce projet n'a été testé que sur Ubuntu 20.04 et 22.04 et a besoin à minima des éléments suivants:
- Python 3
- un serveur local postgresql avec une base contenant l'extension PostGIS v3.x

## Installation

Installer les dépendances python avec:
`pip install -r requirements.txt`

## Chargement des données

Deux scripts bash permettent de télécharger puis importer les données dans Postgresql:
- download.sh
- import_postgresql.sh

## Lancement du serveur

`gunicorn sim2_as_api:app -b 0.0.0.0:8989`

## Paramètres reconnus par l'API

*(les liens interrogent une version temporaire de l'API sur, sans garantie de disponibilité)*

Données climatique pour une date (date, from + to)et un lieu donné (lat, lon):
- http://api.cquest.org:8989/sim2?date=2000-12-25&lat=48.85&lon=2.35 pour le 25/12/2000 à Paris
- http://api.cquest.org:8989/sim2?date=1960-01&lat=45.7578&lon=4.8351 pour le mois de janvier 1960 à Lyon
- http://api.cquest.org:8989/sim2?from=1981-01-01&to=1981-03-31&lat=43.2804&lon=5.3806 pour les mois de janvier à mars 1981 à Marseille

cq - 2024-04-09
