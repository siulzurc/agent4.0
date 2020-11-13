###
# agent_example_1.py
# A simple hello agent in PADE!
# PADE
from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
from pade.behaviours.protocols import TimedBehaviour

## AASX
from aas import model  # Import all PYI40AAS classes from the model package
import aas.adapter.json
import aas.adapter.xml

## Serialization
import pickle
from pade.acl.messages import ACLMessage

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


#Simple Program: 2 agents
if __name__ == '__main__':
    agents_per_process = 3
    agents = list()
    #port = int(argv[1]) + c ## Args
    port = 20000
    agent_process = ProcessAgent(AID(name="Process_Agent_Luis@localhost:{}".format(55200)))
    agent_resource = ResourceAgent(AID(name="Resource_Agent_Luis@localhost:{}".format(8100)))
    #agent_process.debug =True
    #agent_resource.debug =True
    agents.append(agent_process)
    agents.append(agent_resource)

    start_loop(agents)
