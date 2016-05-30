### Disd

#### Introduction

Gestion des daemons qui se lancent au démarrage.

* Python 3.4 et supérieur.

#### Get started

Afficher les daemons qui se lancent au démarrage.
```
python disd.py -e
```

Afficher les daemons qui ne se lancent plus au démarrage.
```
python disd.py -d
```

Activer un daemon au démarrage.
```
python disd.py -e tor bluetooth
```

Désactiver un daemon au démarrage.
```
python disd.py -d tor rabbitmq-server
```

Activer un daemon immédiatement et au démarrage.

```
python disd.py -n -e rabbitmq-server
```
