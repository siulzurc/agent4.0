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
class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("New data change event", node, val)

    def event_notification(self, event):
        print("New event", event)



class TemporalBehavior(TimedBehaviour):
    def __init__(self,agent,time):
        super(TemporalBehavior,self).__init__(agent,time)

    def on_time(self):
        super(TemporalBehavior,self).on_time()
        display_message(self.agent.aid.localname, '(PA) Sending message TB...')
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        message.add_receiver(AID('Resource_Agent_Luis'))
        message.set_content('Prueba TB')
        self.agent.send(message)

#Defining type of agents: Reading the AASX file
class ProcessAgent(Agent):
    def __init__(self, aid):
        super(ProcessAgent, self).__init__(aid=aid)
        temp_behavior = TemporalBehavior(self,5.0)
        self.behaviours.append(temp_behavior)
        self.receiver_aid = "Resource_Agent_Luis"

        display_message(self.aid.localname, 'Process Agent initialized!')
        #Library to create AASX file
        identifier = model.Identifier('https://acplt.org/Simple_Submodel', model.IdentifierType.IRI)
        submodel = model.Submodel(identification=identifier)

        # create a global reference to a semantic description of the property
        semantic_reference = model.Reference(
            (model.Key(
                type_=model.KeyElements.GLOBAL_REFERENCE,
                local=False,
                value='http://acplt.org/Properties/SimpleProperty',
                id_type=model.KeyType.IRI
            ),)
        )
        property = model.Property(
            id_short='ExampleProperty',  # Identifying string of the element within the submodel namespace
            value_type=model.datatypes.String,  # Data type of the value
            value='exampleValue',  # Value of the property
            semantic_id=semantic_reference  # set the semantic reference
        )
        submodel.submodel_element.add(property)

        from aas.adapter.xml import write_aas_xml_file

        data: model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
        data.add(submodel)
        with open('Simple_Submodel_Agent.xml', 'wb') as f:
            write_aas_xml_file(file=f, data=data)
        display_message(self.aid.localname, 'AASX file created!!')
        '''
        with open('Simple_Submodel_Agent.xml', 'rb') as xml_file:
            display_message(self.aid.localname, 'Reading XML file!')
            xml_file_data = aas.adapter.xml.read_aas_xml_file(xml_file)
            submodel_from_xml = xml_file_data.get_identifiable(model.Identifier('https://acplt.org/Simple_Submodel',
                                                                    model.IdentifierType.IRI))
            display_message(self.aid.localname, 'Submodel from XML ' + str(submodel_from_xml))'''

        call_later(2.0, self.sending_message)
        temp_behavior = TemporalBehavior(self,5.0)
        self.behaviours.append(temp_behavior)

    def on_start(self):
        super(ProcessAgent, self).on_start()
        display_message(self.aid.localname, 'Sending message...')
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        message.add_receiver(AID('Resource_Agent_Luis'))
        message.set_content('Prueba')
        self.send(message)
        display_message(self.aid.localname, 'Message sent...')
        call_later(2.0, self.sending_message)


    def sending_message(self):
        display_message(self.aid.localname, '(PA) Sending message...')
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        message.add_receiver(AID('Resource_Agent_Luis'))
        message.set_content('Prueba')
        self.send(message)
#
class ResourceAgent(Agent):
    def __init__(self, aid):
        super(ResourceAgent, self).__init__(aid=aid)
        display_message(self.aid.localname, 'Resource Agent initialized!')
        display_message(self.aid.localname, 'Resource Init finalized')

    def react(self, message):
        super(ResourceAgent, self).react(message)
        display_message(self.aid.localname, '(RA) Message received from {}'.format(message.sender.name))

        display_message(self.aid.localname, '(RA) Message: {}'.format(message.content))

class ManagerAgent(Agent):
    def __init__(self, aid):
        super(ManagerAgent, self).__init__(aid=aid)
        display_message(self.aid.localname, 'Manager Agent initialized!')
        display_message(self.aid.localname, 'Manager Init finalized')



#Simple Program: 2 agents
if __name__ == '__main__':
    agents_per_process = 3
    agents = list()
    #port = int(argv[1]) + c ## Args
    port = 20000
    #agent_process = ProcessAgent(AID(name="Process_Agent_Generic@localhost:{}".format(55200)))
    #agent_resource = ResourceAgent(AID(name="Resource_Agent_Generic@localhost:{}".format(8100)))
    #agent_manager = ResourceAgent(AID(name="Manager_Agent_Generic@localhost:{}".format(8200)))
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
    #agent_process.debug =True
    #agent_resource.debug =True
    #agents.append(agent_process)
    #agents.append(agent_resource)
    #agents.append(agent_manager)
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
    #ams_agent_2 = AMS()
    #agents.append(ams_agent_2)
    #print(agents)


    ## OPC UA Client
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("KeepAlive")
    #logger.setLevel(logging.DEBUG)

    client = Client("opc.tcp://0.0.0.0:4840/tum/ai40server/")
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
        uri = "tum/ai40"
        idx = client.get_namespace_index(uri)

        # using child definitions
        generic_node = root.get_child(['0:Objects', '2:ProcessFolder', '2:generic_model_1', '2:generic_analog_variable'])


        ## using identifier definition
        generic_node_2 = client.get_node("ns=2;i=9")

        # subscribing to a variable node
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        sub.subscribe_data_change(generic_node)
        sub.subscribe_data_change(generic_node_2)


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
    start_loop(agents)
