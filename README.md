# Team PNP | Atreya

![Annapurna base camp, Nepal](https://aidadventure.com/wp-content/uploads/2018/05/annapurna-base-camp-trek.jpg)

# Problem Statement

Once in our life time we must have planned a trip to some beautiful base camp or a trekking destination but, the fear of bad weather has to be one of the biggest hurdle for most of us. It is also one of the biggest reason for us and our loved ones to cancel the trip. Even the stats show that the number of deaths caused due to problems like snowstorm, avalanche are way too high in almost all mountain countries. Nepal is a country whose special ability is to attract tourist from all over the world and the risk of being burried under these snow disasters is enough for anyone to back off. Currently there are not many efficient ways to rescue people from these situations.

# Proposed Solution (**Our Objective**)
Our proposed solution is a ***small and portable*** physical device that can be carried out throughout their trip and since it is a ***low-powered*** device, it can last for days. The device will have a push button, which the user will press inorder to send a distress signal to the nearest base station with the help of **LoRa Module** within a ***Mesh-Network***. The rescue team will then be able to locate the user with the help of **GPS Module** and **LoRa Module** and rescue them.

![User Device](https://i.ibb.co/3RGmjgb/user.jpg)
<p align='center'>Device carried by the user</p>

![Base Station Device](https://i.ibb.co/G5K0410/base.jpg)
<p align='center'>Base Station Device</p>

# Frequently Asked Questions (FAQs):

**Q1.** *What is LoRa?*

LoRa is a long range wide area network (LoRaWAN) designed to wirelessly connect battery operated “things” to the internet in regional, national or global networks, and targets key Internet of Things (IoT) requirements such as bi-directional communication, end-to-end security, mobility and localization services.
![](https://www.makerfabs.com/image/cache/makerfabs/SX1276%20LoRa%20Module%20915MHz%20RFM95/SX1276%20LoRa%20Module%20915MHz%20RFM95-1000x750.jpg)

**Q2.** *What is GPS?*

The Global Positioning System (GPS) is a space-based satellite navigation system that provides location and time information in all weather conditions, anywhere on or near the Earth where there is an unobstructed line of sight to four or more GPS satellites.
![](https://images.squarespace-cdn.com/content/v1/59b037304c0dbfb092fbe894/1561135682906-WWEYOIG7JWB7N7W2NKEE/neo6m_main.JPG?format=1500w)

**Q3.** *What is Mesh-Network?*

Mesh networking is a method of connecting devices to each other in a network topology that resembles a mesh. 
![](https://i.ytimg.com/vi/9d1qyeix2pk/maxresdefault.jpg)
It is a type of network topology in which each node in the network is connected to two or more neighboring nodes, forming a kind of mesh or web. The connections between nodes are established using any of several wireless or wired network technologies, such as Wi-Fi, Ethernet, or Bluetooth


**Q4.** *Why not use Mobile phones for the same purpose?*

Mobile phones are not a good option for this purpose because they are not designed to work in such harsh conditions and also they are not portable enough to be carried throughout the trip. Also, the battery life of mobile phones is not enough to last for days.

**Q5.** *What is the cost of the device?*

The cost of the device will be around ***20$(rougly Rs.2300)***. The cost of the device will be low because we are using the LoRa Module. The module is very cheap and affordable.

**Q6.** *Will LoRa be able to communicate in such high distances?*

Yes, LoRa is capable of communicating in such high distances. The LoRa Module has a range of 10-15km. Also, we will be working with mesh network, which will help us to communicate with the base station even if the user is in a remote area.

**Q7.** *How will we expand the capabilities of the device?*

We intend to expand the device's capaility by reading the sensor information from the user device(smartphones-> temperature/humidity || smart watches-> heart-rate, SPO2, BPM) and sending it to the base station. This will help the rescue team to know the health condition of the user and also the weather conditions in the area. This will help the rescue team to plan their rescue mission accordingly.