### Author: Santiago Gil
from threading import Thread
import copy
import logging
from datetime import datetime
import time
from math import sin
import sys
sys.path.insert(0, "..")

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()

import opcua
from opcua import ua, uamethod, Server


class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)

# method to be exposed through server
@uamethod
def save_into_database(parent, data):
    ret = "Nothing received"
    if data != None:
        print("received data: " + str(data))
        ret = "Data saved successfully"
    print(ret)
    #return [ua.Variant(ret, ua.VariantType.String)]
    return ret

# method to be exposed through server
# uses a decorator to automatically convert to and from variants

@uamethod
def perform_prediction(parent, x1,x2):
    #y = ml_model.predict(x1,x2)
    print("Predicting output of ML model with inputs: ", x1, x2)
    return x1 * x2


class VarUpdater(Thread):
    def __init__(self, var):
        Thread.__init__(self)
        self._stopev = False
        self.var = var

    def stop(self):
        self._stopev = True

    def run(self):
        while not self._stopev:
            v = sin(time.time() / 10)
            self.var.set_value(v)
            time.sleep(0.1)

if __name__ == "__main__":
    # optional: setup logging
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("opcua.address_space")
    # logger.setLevel(logging.DEBUG)
    #logger = logging.getLogger("opcua.internal_server")
    # logger.setLevel(logging.DEBUG)
    #logger = logging.getLogger("opcua.binary_server_asyncio")
    # logger.setLevel(logging.DEBUG)
    #logger = logging.getLogger("opcua.uaprocessor")
    # logger.setLevel(logging.DEBUG)

    # now setup our server
    server = Server()
    #server.disable_clock()

    server.set_endpoint("opc.tcp://0.0.0.0:4840/tum/ai40server/")
    server.set_server_name("Pade-AAS OPC UA Server")
    # set all possible endpoint policies for clients to connect through
    server.set_security_policy([
                ua.SecurityPolicyType.NoSecurity,
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                ua.SecurityPolicyType.Basic256Sha256_Sign])

    # setup our own namespace
    uri = "tum/ai40"
    idx = server.register_namespace(uri)



    # Generic Model
    generic_model_1 = server.nodes.base_object_type.add_object_type(idx, "generic_model_1")
    generic_model_1_var = generic_model_1.add_variable(idx, "generic_analog_variable", 0.0).set_modelling_rule(True)
    #generic_model_1_var.set_writable()



    # Modelo recurso de software
    generic_model_2 = server.nodes.base_object_type.add_object_type(idx, "generic_model_2")
    generic_model_2_var = generic_model_2.add_variable(idx, "generic_boolen_variable", False).set_modelling_rule(True)
    #generic_model_2_var.set_writable()

    # First a folder to organise our nodes
    process_folder = server.nodes.objects.add_folder(idx, "ProcessFolder")

    generic_object_ua_1 = process_folder.add_object(idx, "generic_model_1", generic_model_1)
    generic_object_ua_2 = process_folder.add_object(idx, "generic_model_2", generic_model_2)


    ## permissions
    generic_object_ua_1.get_child("2:generic_analog_variable").set_writable()
    generic_object_ua_2.get_child("2:generic_boolen_variable").set_writable()



    # creating a default event object
    # The event object automatically will have members for all events properties
    # you probably want to create a custom event type, see other examples
    myevgen = server.get_event_generator()
    myevgen.event.Severity = 300

    # starting!
    server.start()
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
