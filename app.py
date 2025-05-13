from flask import Flask, request, jsonify                                                         
import threading
import paho.mqtt.client as pmc
import paho.mqtt.subscribe as subscribe
import time
from countdown import Timer 
isRunning = True




HOTE = "rapper"
#BROKER = "mqttbroker.lan"
BROKER = "192.168.137.1"
PORT = 1883
TOPIC_SEND_T = "final/%s/T" % HOTE
TOPIC_SEND_H = "final/%s/H" % HOTE
TOPIC_RECEIVE_T = "final/+/T"
TOPIC_HUMIDITY_RECEIVE_H = "final/+/H"
etat = True
mqtt_temparatures = {}
mqtt_humidities = {} 

lastest_messsage = ""
def connexion(client, userdata, flags, code, properties):
    print(client)
    if code == 0:
        print("Connecté")
    else:
        print("Erreur code %d\n", code)

def reception_msg(cl,userdata,msg):
    message_content = msg.payload.decode()
    print("Recu", message_content)
    print(msg.topic)
    if message_content.isnumeric():
        if msg.topic[-1] == "T":
            mqtt_temparatures[msg.topic] = message_content
            print(mqtt_temparatures)
        if msg.topic[-1] == "H":
            mqtt_humidities[msg.topic] = message_content
            print(mqtt_humidities)


def temparature_max_topic() -> str:
    maxtopic = None
    for i in mqtt_temparatures:
        if not maxtopic or mqtt_temparatures[i] > mqtt_temparatures[maxtopic]:
            maxtopic = i
    return maxtopic
def humidity_max_topic() -> str:
    maxtopic = None
    for i in mqtt_humidities:
        if not maxtopic or mqtt_humidities[i] > mqtt_humidities[maxtopic]:
            maxtopic = i
    return maxtopic






def send_sensor_data():
    pass

def read_temperature_data()->int:
    pass
def read_humidity_data()->int:
    pass


# starting source :https://stackoverflow.com/questions/31264826/start-a-flask-application-in-separate-thread

host_name = "0.0.0.0"
port = 23336
app = Flask(__name__)

@app.route("/")
def main():
    return lastest_messsage

# test : curl -X POST http://192.168.137.222:23336/etat -H "Content-type:application/json" -d "{\"etat\":\"1\"}"
@app.route("/etat", methods=["POST"])
def etat():
    data : dict = request.get_json()
    if "etat" in data:
        global etat
        etat = True if "1" in data["etat"] else False
        print(etat)
    return data
#curl -X GET http://192.168.137.222:23336/donnees -H "Content-type:application/json"
@app.route("/donnees", methods=["GET"])
def donnees():
    # source jsonify : https://www.geeksforgeeks.org/use-jsonify-instead-of-json-dumps-in-flask/
    if mqtt_humidities.get(TOPIC_SEND_H,"unknown") != "unknown" and mqtt_temparatures.get(TOPIC_SEND_T,"unknown") != "unknown":
        return_dict = {"H" : mqtt_humidities[TOPIC_SEND_H],
        "T" : mqtt_temparatures[TOPIC_SEND_T]}
        return return_dict


    response = {"message" : "data unknown"}
    return response




if __name__ == "__main__":
    
    #threads objects
    timer = Timer()

    #flask
    flask_thread = threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False))
    flask_thread.start()
    
    # mqtt
    client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
    client.on_connect = connexion
    client.connect(BROKER,PORT)
    client.on_message = reception_msg
    #source : https://pypi.org/project/paho-mqtt/#callbacks
    client.subscribe(TOPIC_RECEIVE_T)
    client.subscribe(TOPIC_HUMIDITY_RECEIVE_H)
    # client.publish(TOPIC,"allo")


    threads = [timer]
    for i in threads: #starts the threads
        i.start()
    print("threads started")
    
    
    client.loop_start()
    try :
        while isRunning and flask_thread.is_alive():
            if timer.get_state() == "timeout":
                pass
    except KeyboardInterrupt:
        pass
    client.loop_stop()

    threads_amount = len(threads)
    all_threads_ended_number = threading.active_count() - threads_amount
    for i in threads:
        i.kill = True
    while threading.active_count() > all_threads_ended_number:
        print("waiting for {0} threads".format(str(threading.active_count() - all_threads_ended_number)))
        time.sleep(1)
    print("Program end")
 
 

