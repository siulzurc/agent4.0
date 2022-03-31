# -*- coding: utf-8 -*-
# Realized by Luis Alberto Cruz Salazar - Technical University of Munich 07/05/2021
# FIPA Contract Net Protocol for agents' Call of Proposals (CFPs)
# Example of Initial FIPA-CNP behaviour that sends CFP messages between a Process agent (PA) and two
# Resource agents (RA), which are asking for restoration proposals.
# This example behaviour also analyzes the CFPs and selects the one it judges to be the best.
# Source" Adapted from: https://pade.readthedocs.io/en

from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.acl.messages import ACLMessage
from pade.behaviours.protocols import FipaContractNetProtocol
from sys import argv
from random import uniform
from opcua import Client
from opcua import ua
import time
#from opcua import CryptographyNone
#from opcua import SecurityPolicy

#from opcua.crypto import security_policies

'''#Setting and conecting OPC UA client with NONE Security
url = "opc.tcp://localhost:4840"
client = Client(url)
client.connect()
var = client.get_node("ns=2;i=2")'''

#Setting and conecting OPC UA client with NONE security
url = "opc.tcp://192.168.82.11:4840"
client = Client(url)
client.application_uri = "urn:BeckhoffAutomation:TcOpcUaServer"
#client.set_security_string("Basic256Sha,Sign,certificate.der,privateKey.pem")
# Beckhoff_OpcUaServer.der and Beckhoff_OpcUaServer.pem files should be in the same folder (download these from the PLC OPCUSA server certificates)
client.set_security_string("Basic256Sha256,Sign,Beckhoff_OpcUaServer.der,Beckhoff_OpcUaServer.pem")
client.connect()

#Setting all variables
#double_node = client.get_node("ns=2;s=Demo.Static.Scalar.Double") # returns a Node-Class
#var.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
#dv = ua.DataValue(ua.Variant(200.0, ua.VariantType.Double))
#var1 = ua.DataValue(ua.Variant(122, ua.VariantType.Int16))

SensorValueLSC = client.get_node("ns=4;s=GVL.SensorValueLSC")
var1 = ua.DataValue(ua.Variant(10, ua.VariantType.Float))
SensorValueLSC.set_value(var1)

calculatedSensorValue = client.get_node("ns=4;s=GVL.calculatedSensorValue")
var2 = ua.DataValue(ua.Variant(10, ua.VariantType.Float))
calculatedSensorValue.set_value(var2)

VsensorPCvalue = client.get_node("ns=4;s=GVL.VsensorPCvalue")
var3 = ua.DataValue(ua.Variant(10, ua.VariantType.Float))
VsensorPCvalue.set_value(var3)

VsensorRCvalue = client.get_node("ns=4;s=GVL.VsensorRCvalue")
var4 = ua.DataValue(ua.Variant(10, ua.VariantType.Float))
VsensorRCvalue.set_value(var4)
 
VsensorSSCvalue = client.get_node("ns=4;s=GVL.VsensorSSCvalue")
var5 = ua.DataValue(ua.Variant(10, ua.VariantType.Float))
VsensorSSCvalue.set_value(var5)

statusSensorLSC = client.get_node("ns=4;s=GVL.statusSensorLSC")
var6 = statusSensorLSC.get_value()
#print("var6 is {}".format(var6))
#time.sleep(1)
#var6 = ua.DataValue(ua.Variant(0, ua.VariantType.Boolean))
#statusSensorLSC.set_value(var6) 
#statusSensorLSC.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))

statusVsensorRC = client.get_node("ns=4;s=GVL.statusVsensorRC")
var7 = statusVsensorRC.get_value()

statusVsensorSSC = client.get_node("ns=4;s=GVL.statusVsensorSSC")
var8 = statusVsensorSSC.get_value()

statusVsensorPC = client.get_node("ns=4;s=GVL.statusVsensorPC")
var9 = statusVsensorPC.get_value()
        
activePADE = client.get_node("ns=4;s=GVL.activePADE")
var10 = activePADE.get_value()

class CompContNet1(FipaContractNetProtocol):
    '''CompContNet1: CNP  + Analyzing CFps'''

    def __init__(self, agent, message):
        super(CompContNet1, self).__init__(
            agent=agent, message=message, is_initiator=True)
        self.cfp = message

    def handle_all_proposes(self, proposes):
        """
        """

        super(CompContNet1, self).handle_all_proposes(proposes)

        best_proposer = None
        higher_accuracy = 0.0
        
        
        other_proposers = list()
        display_message(self.agent.aid.name, 'Analyzing proposals...')
#part 1 completed
        i = 1

        # logic to select proposals by the higher available accuracy.
        for message in proposes:
            content = message.content
            accuracy = float(content)
            display_message(self.agent.aid.name,
                            'Analyzing proposal {i}'.format(i=i))
            
            display_message(self.agent.aid.name,
                            'Accuracy Offered: {pot}'.format(pot=accuracy))
            i += 1
            if accuracy > higher_accuracy:
#part 2 completed
                if best_proposer is not None:
                    other_proposers.append(best_proposer)

                higher_accuracy = accuracy            
                best_proposer = message.sender
            else:
                other_proposers.append(message.sender)

        display_message(self.agent.aid.name,
                        'The best proposal was: {pot} %'.format(
                            pot=higher_accuracy))

        #setting higher accuracy to the OPC client
        #var.set_value(higher_accuracy, ua.VariantType.int16)
        var2 = ua.DataValue(ua.Variant(higher_accuracy, ua.VariantType.Float))
        calculatedSensorValue.set_value(var2)

        if other_proposers != []:
            display_message(self.agent.aid.name,
                            'Sending REJECT_PROPOSAL answers...')
            answer = ACLMessage(ACLMessage.REJECT_PROPOSAL)
            answer.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
            answer.set_content('')
            for agent in other_proposers:
                answer.add_receiver(agent)

            self.agent.send(answer)

        if best_proposer is not None:
#part 3 completed
 
            display_message(self.agent.aid.name,
                            'Sending ACCEPT_PROPOSAL answer...')

            answer = ACLMessage(ACLMessage.ACCEPT_PROPOSAL)
            answer.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
            answer.set_content('OK')
            answer.add_receiver(best_proposer)
            self.agent.send(answer)

    def handle_inform(self, message):
        """
        """
        super(CompContNet1, self).handle_inform(message)

        display_message(self.agent.aid.name, 'INFORM message received')
        
#part 4 completed
    def handle_refuse(self, message):
        """
        """
        super(CompContNet1, self).handle_refuse(message)

        display_message(self.agent.aid.name, 'REFUSE message received')

    def handle_propose(self, message):
        """
        """
        super(CompContNet1, self).handle_propose(message)

        display_message(self.agent.aid.name, 'PROPOSE message received')


class CompContNet2(FipaContractNetProtocol):
    '''CompContNet2

       FIPA-ContractNet Participant Behaviour that runs when an agent
       receives a CFP message. A proposal is sent and if it is selected,
       the restrictions are analized to enable the restoration.'''

    def __init__(self, agent):
        super(CompContNet2, self).__init__(agent=agent,
                                           message=None,
                                           is_initiator=False)

    def handle_cfp(self, message):
        """
        """
        self.agent.call_later(1.0, self._handle_cfp, message)

    def _handle_cfp(self, message):
        """
        """
        super(CompContNet2, self).handle_cfp(message)
        self.message = message

        display_message(self.agent.aid.name, 'CFP message received')

        answer = self.message.create_reply()
        answer.set_performative(ACLMessage.PROPOSE)
        answer.set_content(str(self.agent.pot_disp))
        self.agent.send(answer)

    def handle_reject_propose(self, message):
        """
        """
        super(CompContNet2, self).handle_reject_propose(message)

        display_message(self.agent.aid.name,
                        'REJECT_PROPOSAL message received')

    def handle_accept_propose(self, message):
        """
        """
        super(CompContNet2, self).handle_accept_propose(message)

        display_message(self.agent.aid.name,
                        'ACCEPT_PROPOSE message received')

        answer = message.create_reply()
        answer.set_performative(ACLMessage.INFORM)
        answer.set_content('OKvalue')
        self.agent.send(answer)
        
#part 5 completed


class AgentInitiator(Agent):

    def __init__(self, aid, participants):
        super(AgentInitiator, self).__init__(aid=aid, debug=False)

        message = ACLMessage(ACLMessage.CFP)
        message.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        message.set_content('sensor value accuracy?')

        for participant in participants:
            message.add_receiver(AID(name=participant))

#part 6 completed

        self.call_later(8.0, self.launch_contract_net_protocol, message)

    def launch_contract_net_protocol(self, message):
        comp = CompContNet1(self, message)
        self.behaviours.append(comp)
        comp.on_start()


class AgentParticipant(Agent):

    def __init__(self, aid, pot_disp):
        super(AgentParticipant, self).__init__(aid=aid, debug=False)

        self.pot_disp = pot_disp

        comp = CompContNet2(self)

        self.behaviours.append(comp)

var10 = activePADE.get_value()
if __name__ == "__main__" and var10 == True:
    agents_per_process = 1
    c = 0
    agents = list()
    for i in range(agents_per_process):
        port = int(argv[1]) + c        
        k = 10000
        participants = list()

# Real Sensor (in LSC)
        agent_name = 'SensorAgentLSC_{}@localhost:{}'.format(port - k, port - k)
        participants.append(agent_name)
        var6 = statusSensorLSC.get_value()
        if var6 == True:
           var1 = uniform(98.5, 100.0)            
        else:
           var1 = uniform(0.5, 50.0)
        agente_part_0 = AgentParticipant(AID(name=agent_name), var1)
        var1 = ua.DataValue(ua.Variant(var1, ua.VariantType.Float))
        SensorValueLSC.set_value(var1)
        agents.append(agente_part_0)

#part 7 completed
              
# Virtual Sensor 1 (in RC)
        var7 = statusVsensorRC.get_value()
        if var7 == True:
           agent_name = 'VsensorAgentRC_{}@localhost:{}'.format(port + k, port + k)
           participants.append(agent_name)
           var4 = uniform(90.0, 95.0)
           agente_part_1 = AgentParticipant(AID(name=agent_name), var4)
           var4 = ua.DataValue(ua.Variant(var4, ua.VariantType.Float))
           VsensorRCvalue.set_value(var4)
           agents.append(agente_part_1)

# Virtual Sensor 2 (in SSC)
        var8 = statusVsensorSSC.get_value()
        if var8 == True:
           agent_name = 'VsensorAgentSSC_{}@localhost:{}'.format(port + 2*k, port + 2*k)
           participants.append(agent_name)
           var5 = uniform(85.0, 90.0)
           agente_part_2 = AgentParticipant(AID(name=agent_name), var5)
           var5 = ua.DataValue(ua.Variant(var5, ua.VariantType.Float))
           VsensorSSCvalue.set_value(var5) 
           agents.append(agente_part_2)

# Virtual Sensor 3 (in PC)
        var9 = statusVsensorPC.get_value()
        if var9 == True:
           agent_name = 'VsensorAgentPC_{}@localhost:{}'.format(port + 3*k, port + 3*k)
           participants.append(agent_name)
           var3 = uniform(80.0, 85.0)
           agente_part_3 = AgentParticipant(AID(name=agent_name), var3)
           var3 = ua.DataValue(ua.Variant(var3, ua.VariantType.Float))
           VsensorPCvalue.set_value(var3)
           agents.append(agente_part_3)

# Slide Agent (in LSC)
        agent_name = 'SlideAgentLSC_init_{}@localhost:{}'.format(port, port)
        agente_init_1 = AgentInitiator(AID(name=agent_name), participants)
        agents.append(agente_init_1)

        c += 1000
    
    #newvalue = var.get_value(port) + 0
    #newvalue = 1000
 
        
    start_loop(agents)
