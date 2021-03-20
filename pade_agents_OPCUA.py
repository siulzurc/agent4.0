###
# agent_example_1.py
# A simple hello agent in PADE!
# PADE
from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.core.new_ams import AMS
from pade.acl.aid import AID
from sys import argv
from pade.behaviours.protocols import TimedBehaviour

## AASX
from aas import model  # Import all PYI40AAS classes from the model package
import aas.adapter.json
import aas.adapter.xml
import gc

## Serialization
import pickle
from pade.acl.messages import ACLMessage

## OPC UA
from opcua import Client
from opcua import ua

import logging
import time




## OPC UA SubHandler


set_blue_value = 0
set_green_value = 0
order_no_value = 0
add1_value = 0
add2_value = 0
blue_value = 0
green_value = 0
free_value = 0
availability_value = 0
performance_value = 0
quality_value = 0
oee_value = 0
orderWIP_value = 0
achieveB_value = 0
achieveG_value = 0
order_achieved_value = 0
perform_time_value = 0
active_pade_value = 0

## OPC UA Client
logging.basicConfig(level=logging.WARN)
#logger = logging.getLogger("KeepAlive")
#logger.setLevel(logging.DEBUG)

client = Client("opc.tcp://192.168.0.30:53880/")

class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        global client
        global set_blue_value
        global set_green_value
        global order_no_value
        global add1_value
        global add2_value
        global blue_value
        global green_value
        global free_value
        global availability_value
        global performance_value
        global quality_value
        global oee_value
        global orderWIP_value
        global achieveB_value
        global achieveG_value
        global order_achieved_value
        global perform_time_value
        global active_pade_value
        print("New data change event", node, val)

        set_blue_uanode = client.get_node("ns=1;s=SetBlue")
        set_green_uanode = client.get_node("ns=1;s=SetGreen")
        order_no_uanode = client.get_node("ns=1;s=orderNo")
        add1_uanode = client.get_node("ns=1;s=Add1")
        add2_uanode = client.get_node("ns=1;s=Add2")
        blue_uanode = client.get_node("ns=1;s=Blue")
        green_uanode = client.get_node("ns=1;s=Green")
        free_uanode = client.get_node("ns=1;s=Free")
        availability_uanode = client.get_node("ns=1;s=Availability")
        performance_uanode = client.get_node("ns=1;s=Performance")
        quality_uanode = client.get_node("ns=1;s=Quality")
        oee_uanode = client.get_node("ns=1;s=OEE")
        orderWIP_uanode = client.get_node("ns=1;s=orderWIP")
        achieveB_uanode = client.get_node("ns=1;s=AchieveB")
        achieveG_uanode = client.get_node("ns=1;s=AchieveG")
        order_achieved_uanode = client.get_node("ns=1;s=orderAchieved")
        perform_time_uanode = client.get_node("ns=1;s=PerformTime")
        active_pade_uanode = client.get_node("ns=1;s=activePADE")

        set_blue_value = set_blue_uanode.get_value()
        set_green_value = set_green_uanode.get_value()
        order_no_value = order_no_uanode.get_value()
        add1_value = add1_uanode.get_value()
        add2_value = add2_uanode.get_value()
        blue_value = blue_uanode.get_value()
        green_value = green_uanode.get_value()
        free_value = free_uanode.get_value()
        availability_value = availability_uanode.get_value()
        performance_value = performance_uanode.get_value()
        quality_value = quality_uanode.get_value()
        oee_value = oee_uanode.get_value()
        orderWIP_value = orderWIP_uanode.get_value()
        achieveB_value = achieveB_uanode.get_value()
        achieveG_value = achieveG_uanode.get_value()
        order_achieved_value = order_achieved_uanode.get_value()
        perform_time_value = perform_time_uanode.get_value()
        active_pade_value = active_pade_uanode.get_value()

    def event_notification(self, event):
        print("New event", event)



try:
    client.connect()
    client.load_type_definitions()  # load definition of server specific structures/extension objects

    # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
    root = client.get_root_node()
    print("Root node is: ", root)
    objects = client.get_objects_node()
    print("Objects node is: ", objects)

    # Node objects have methods to read and write node attributes as well as browse or populate address space
    print("Children of root are: ", root.get_children())

    # gettting our namespace idx
    uri = ""
    idx = client.get_namespace_index(uri)

    ## variables
    set_blue_uanode = client.get_node("ns=1;s=SetBlue")
    set_green_uanode = client.get_node("ns=1;s=SetGreen")
    order_no_uanode = client.get_node("ns=1;s=orderNo")
    add1_uanode = client.get_node("ns=1;s=Add1")
    add2_uanode = client.get_node("ns=1;s=Add2")
    blue_uanode = client.get_node("ns=1;s=Blue")
    green_uanode = client.get_node("ns=1;s=Green")
    free_uanode = client.get_node("ns=1;s=Free")
    availability_uanode = client.get_node("ns=1;s=Availability")
    performance_uanode = client.get_node("ns=1;s=Performance")
    quality_uanode = client.get_node("ns=1;s=Quality")
    oee_uanode = client.get_node("ns=1;s=OEE")
    orderWIP_uanode = client.get_node("ns=1;s=orderWIP")
    achieveB_uanode = client.get_node("ns=1;s=AchieveB")
    achieveG_uanode = client.get_node("ns=1;s=AchieveG")
    order_achieved_uanode = client.get_node("ns=1;s=orderAchieved")
    perform_time_uanode = client.get_node("ns=1;s=PerformTime")
    active_pade_uanode = client.get_node("ns=1;s=activePADE")

    # subscribing to a variable node
    handler = SubHandler()
    sub = client.create_subscription(500, handler)
    sub.subscribe_data_change(set_blue_uanode)
    sub.subscribe_data_change(set_green_uanode)
    sub.subscribe_data_change(order_no_uanode)
    sub.subscribe_data_change(add1_uanode)
    sub.subscribe_data_change(add2_uanode)
    sub.subscribe_data_change(blue_uanode)
    sub.subscribe_data_change(green_uanode)
    sub.subscribe_data_change(free_uanode)
    sub.subscribe_data_change(availability_uanode)
    sub.subscribe_data_change(performance_uanode)
    sub.subscribe_data_change(quality_uanode)
    sub.subscribe_data_change(oee_uanode)
    sub.subscribe_data_change(orderWIP_uanode)
    sub.subscribe_data_change(achieveB_uanode)
    sub.subscribe_data_change(achieveG_uanode)
    sub.subscribe_data_change(order_achieved_uanode)
    sub.subscribe_data_change(perform_time_uanode)
    sub.subscribe_data_change(active_pade_uanode)


    time.sleep(0.1)

    # we can also subscribe to events from server
    sub.subscribe_events()
    # sub.unsubscribe(handle)
    # sub.delete()

    # calling a method on server
    #res = obj.call_method("{}:multiply".format(idx), 3, "klk")
    #print("method result is: ", res)

    # IPython embed to enable interactive shell
    #embed()

finally:
    client.disconnect()



########################## Agents ###############################

class TemporalProductAgentBehavior(TimedBehaviour):
    def __init__(self,agent,time):
        super(TemporalProductAgentBehavior,self).__init__(agent,time)

    def on_time(self):
        super(TemporalProductAgentBehavior,self).on_time()
        global client
        global set_blue_value
        global set_green_value
        global order_no_value
        global add1_value
        global add2_value
        global blue_value
        global green_value
        global free_value
        global availability_value
        global performance_value
        global quality_value
        global oee_value
        global orderWIP_value
        global achieveB_value
        global achieveG_value
        global order_achieved_value
        global perform_time_value
        global active_pade_value
        display_message(self.agent.aid.localname, '(PA) Temporal Behavior')
        #message = ACLMessage(ACLMessage.INFORM)
        #message.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        #message.add_receiver(AID('Agent_name'))
        #message.set_content('content')
        #self.agent.send(message)
        #Business logic PAs
        #client.get_node("ns=1;s=SetBlue").set_value(15)

class TemporalResourceAgentBehavior(TimedBehaviour):
    def __init__(self,agent,time):
        super(TemporalResourceAgentBehavior,self).__init__(agent,time)

    def on_time(self):
        super(TemporalResourceAgentBehavior,self).on_time()
        global client
        global set_blue_value
        global set_green_value
        global order_no_value
        global add1_value
        global add2_value
        global blue_value
        global green_value
        global free_value
        global availability_value
        global performance_value
        global quality_value
        global oee_value
        global orderWIP_value
        global achieveB_value
        global achieveG_value
        global order_achieved_value
        global perform_time_value
        global active_pade_value
        display_message(self.agent.aid.localname, '(RA) Temporal Behavior')
        #message = ACLMessage(ACLMessage.INFORM)
        #message.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        #message.add_receiver(AID('Agent_name'))
        #message.set_content('content')
        #self.agent.send(message)
        #Business logic RAs
        #client.get_node("ns=1;s=SetBlue").set_value(15)

class TemporalManagerAgentBehavior(TimedBehaviour):
    def __init__(self,agent,time):
        super(TemporalManagerAgentBehavior,self).__init__(agent,time)

    def on_time(self):
        super(TemporalManagerAgentBehavior,self).on_time()
        global client
        global set_blue_value
        global set_green_value
        global order_no_value
        global add1_value
        global add2_value
        global blue_value
        global green_value
        global free_value
        global availability_value
        global performance_value
        global quality_value
        global oee_value
        global orderWIP_value
        global achieveB_value
        global achieveG_value
        global order_achieved_value
        global perform_time_value
        global active_pade_value
        display_message(self.agent.aid.localname, '(MA) Temporal Behavior')
        #message = ACLMessage(ACLMessage.INFORM)
        #message.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        #message.add_receiver(AID('Agent_name'))
        #message.set_content('content')
        #self.agent.send(message)
        #Business logic MAs
        #client.get_node("ns=1;s=SetBlue").set_value(15)


#Defining type of agents: Reading the AASX file
class ProcessAgent(Agent):
    def __init__(self, aid):
        super(ProcessAgent, self).__init__(aid=aid)
        temp_behavior_pa = TemporalProductAgentBehavior(self,1.0)
        self.behaviours.append(temp_behavior_pa)

        display_message(self.aid.localname, 'Process Agent initialized!')
        #call_later(2.0, self.sending_message)

    def on_start(self):
        super(ProcessAgent, self).on_start()


    def sending_message(self):
        display_message(self.aid.localname, '(PA) Sending message...')
        #message = ACLMessage(ACLMessage.INFORM)
        #message.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        #message.add_receiver(AID('Agent_name'))
        #message.set_content('content')
        #self.agent.send(message)

    def react(self, message):
        super(ProcessAgent, self).react(message)
        display_message(self.aid.localname, '(PA) Message received from {}'.format(message.sender.name))

        display_message(self.aid.localname, '(PA) Message: {}'.format(message.content))

class ResourceAgent(Agent):
    def __init__(self, aid):
        super(ResourceAgent, self).__init__(aid=aid)
        temp_behavior_ra = TemporalResourceAgentBehavior(self,1.0)
        self.behaviours.append(temp_behavior_ra)
        display_message(self.aid.localname, 'Resource Agent initialized!')

    def on_start(self):
        super(ResourceAgent, self).on_start()


    def sending_message(self):
        display_message(self.aid.localname, '(RA) Sending message...')
        #message = ACLMessage(ACLMessage.INFORM)
        #message.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        #message.add_receiver(AID('Agent_name'))
        #message.set_content('content')
        #self.agent.send(message)

    def react(self, message):
        super(ResourceAgent, self).react(message)
        display_message(self.aid.localname, '(RA) Message received from {}'.format(message.sender.name))

        display_message(self.aid.localname, '(RA) Message: {}'.format(message.content))

class ManagerAgent(Agent):
    def __init__(self, aid):
        super(ManagerAgent, self).__init__(aid=aid)
        temp_behavior_ma = TemporalManagerAgentBehavior(self,1.0)
        self.behaviours.append(temp_behavior_ma)
        display_message(self.aid.localname, 'Manager Agent initialized!')



#Simple Program: 2 agents
if __name__ == '__main__':
    agents = list()
    agent_RATransportB = ResourceAgent(AID(name="Resource_Agent_TransportB@localhost:{}".format(8101)))
    agent_RATransportG = ResourceAgent(AID(name="Resource_Agent_TransportG@localhost:{}".format(8102)))
    agent_RAPickAndPlace = ResourceAgent(AID(name="Resource_Agent_PickAndPlace@localhost:{}".format(8103)))
    agent_RAFillingB = ResourceAgent(AID(name="Resource_Agent_FillingB@localhost:{}".format(8104)))
    agent_RAFillingG = ResourceAgent(AID(name="Resource_Agent_FillingG@localhost:{}".format(8105)))
    agent_PAProducingB = ResourceAgent(AID(name="Process_Agent_ProducingB@localhost:{}".format(55201)))
    agent_PAProducingG = ResourceAgent(AID(name="Process_Agent_ProducingG@localhost:{}".format(55202)))
    agent_PAProducingO = ResourceAgent(AID(name="Process_Agent_ProducingO@localhost:{}".format(55203)))
    agent_AMSdt1 = ResourceAgent(AID(name="Agent_Manager_dt1@localhost:{}".format(8201)))
    agent_AMSdt2 = ResourceAgent(AID(name="Agent_Manager_dt2@localhost:{}".format(8202)))
    agent_AMSdt3 = ResourceAgent(AID(name="Agent_Manager_dt3@localhost:{}".format(8203)))
    agents.append(agent_RATransportB)
    agents.append(agent_RATransportG)
    agents.append(agent_RAPickAndPlace)
    agents.append(agent_RAFillingB)
    agents.append(agent_RAFillingG)
    agents.append(agent_PAProducingB)
    agents.append(agent_PAProducingG)
    agents.append(agent_PAProducingO)
    agents.append(agent_AMSdt1)
    agents.append(agent_AMSdt2)
    agents.append(agent_AMSdt3)
    start_loop(agents)
