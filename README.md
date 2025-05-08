
# Variables/Legend
Hote :  HOTE par le « hostname » de votre RaspberryPi.
T : (int) : Nombre entier correspondant à la dernière température lue
H :  (int) : Nombre entier de 0 à 100 correspondant à la dernière valeur d’humidité lue
etat (int) : 0 désactive l’envoi de données, 1 active l’envoi de données.
# MQTT, Envoie, Fonction

## condition, si **etat** == VRAI
1. Température, envoyé à final/HOTE/T
2. Humidité, envoyé à final/HOTE/H




# MQTT, Recoie, Fonction
4. Lire, température, envoyé à final/#/T -> si (soi) plus grande -> Led Rouge = 1 sinon 0
5. Lire Humidité, envoyé à final/#/H -> si (soi) plus grande -> Led bleu = 1 sinon 0


# Event, Appel -> MQTT, Envoie, Fonction
1. chaque 30 sec
2. Appui, sec < 2 sec since relache


# EVENT, CHANGE, VARIABLE **ENVOI** = ! **ENVOI**
1. Appui, sec > 2 sec since relache

# EVENT, CHANGE, VARIABLE **ENVOI** == VALUE
1. Flask, etat = result 
DONE
# EVENT, GET, FLASK, TEMPERATURE ET HUMIDITÉ
1. 
T (int) : Nombre entier correspondant à la dernière température lue
 H (int) : Nombre entier de 0 à 100 correspondant à la dernière valeur d’humidité lue


