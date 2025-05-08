from flask import Flask, request                                                         
import threading
import paho.mqtt.client as pmc
import paho.mqtt.subscribe as subscribe

HOTE = "rapper"
#BROKER = "mqttbroker.lan"
BROKER = "192.168.137.1"
PORT = 1883
TOPIC_SEND_T = "final/%s/T" % HOTE
TOPIC_SEND_H = "final/%s/H" % HOTE
TOPIC_RECEIVE_T = "final/+/T"
TOPICHUMIDITY_RECEIVE_H = "final/+/H"
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
    if msg.topic[-1] == "T":
        mqtt_temparatures[msg.topic] = message_content
        print(mqtt_temparatures)
    if msg.topic[-1] == "H":
        mqtt_humidities[msg.topic] = message_content
        print(mqtt_humidities)
def temparature_max_topic():
    pass
def humidity_max_topic():
    pass

def send_sensor_data():
    pass
def receive_sensor_h(client, userdata, message):
    pass
def receive_sensor_t(client, userdata, message):
    print(client)
    print(message.payload.decode())
    print(userdata)

# starting source :https://stackoverflow.com/questions/31264826/start-a-flask-application-in-separate-thread

data = 'foo'
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



if __name__ == "__main__":
    client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
    client.on_connect = connexion
    client.connect(BROKER,PORT)
    client.on_message = reception_msg

    
    #source : https://pypi.org/project/paho-mqtt/#callbacks
    client.subscribe(TOPIC_RECEIVE_T)
    
    # client.publish(TOPIC,"allo")
    threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False)).start()
    client.loop_forever()

client.loop_stop()