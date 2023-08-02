import paho.mqtt.client as mqtt
import xml.etree.ElementTree as ET


def on_connect(client, userdata, flags, rc):
    print(f"Connack received with code {rc}")


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def print_menu():
    print("\nChoose an option")
    for i in options.keys():
        print(i, " ", options[i])


def subscribe(list):
    for topic in list:
        client.subscribe(f'{topic[0]}/#', qos=int(topic[1]))
def add_subscription():
    topic_to_sub = input("Enter the topic to subscribe: ")
    qos_to_sub = int(input("Enter qos: (default 0)") or "0")
    (result, mid) = client.subscribe(f'{topic_to_sub}/#', qos=qos_to_sub)
    if (result == 0):
        tree = ET.parse("config.xml")
        root = tree.getroot()
        subscriptionList = root.find("subscriptionList")
        subscription = ET.SubElement(subscriptionList, "subscription")
        topic = ET.SubElement(subscription, "topic")
        qos = ET.SubElement(subscription, "qos")
        topic.text = topic_to_sub
        qos.text = str(qos_to_sub)
        tree.write("config.xml")

def publish():
    topic_to_pub = input("Enter the topic to publish: ")
    qos_to_pub = int(input("Enter qos: (default 0)") or "0")
    msg = input("Enter the message: ")
    (rc, mid) = client.publish(f'{topic_to_pub}', str(msg), qos=qos_to_pub)  # rc: return code mid: message id

options = {
    1: "Add subscription",
    2: "Publish",
    3: "See messages",
    4: "Exit"
}

# host_name = input("Enter the host name: ") or "broker.mqtt-dashboard.com"
# port_number = input("Enter the port number: ") or "1883"
def parseXMl(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    topics = []
    for connection in root.findall("connection"):
        host = connection.find("host").text
        port = connection.find("port").text
    for sublist in root.findall("subscriptionList"):
        for sub in sublist.findall("subscription"):
            topic = sub.find("topic").text
            qos = sub.find("qos").text
            topics.append((topic, qos))

    return [host, port, topics]


host_name, port_number, topics = parseXMl("config.xml")

client = mqtt.Client()
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect(host_name, int(port_number))
subscribe(topics)

while True:
    print_menu()
    option = input("Enter the option: ")
    if (option == "1"):
        add_subscription()
    elif (option == "2"):
        publish()
        continue
    elif (option == "3"):
        pass
    elif (option == "4"):
        exit()
    else:
        print("Enter a valid option")
        continue

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        continue
