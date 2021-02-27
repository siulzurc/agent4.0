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

def stop_opcua_server():
    uaserver.stop()

def update_opcua_variable(node_id_str,data):
    node_id = uaserver.get_node(node_id_str)
    try:
        node_id.set_value(data)
    except:
        print('error while updating OPC UA variable')
        return

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
    uri = "agent40/application"
    idx = server.register_namespace(uri)



    # Generic Model
    order_model = server.nodes.base_object_type.add_object_type(idx, "order_model")
    order_model_set_blue = order_model.add_variable(idx, "order_model_set_blue", 0)
    order_model_set_blue.set_modelling_rule(True)
    order_model_set_blue.set_writable()
    order_model_set_green = order_model.add_variable(idx, "order_model_set_green", 0)
    order_model_set_green.set_modelling_rule(True)
    order_model_set_green.set_writable()
    order_model_add = order_model.add_variable(idx, "order_model_add", 0)
    order_model_add.set_modelling_rule(True)
    order_model_add.set_writable()
    order_model_blue = order_model.add_variable(idx, "order_model_blue", 0)
    order_model_blue.set_modelling_rule(True)
    order_model_blue.set_writable()
    order_model_green = order_model.add_variable(idx, "order_model_green", 0)
    order_model_green.set_modelling_rule(True)
    order_model_green.set_writable()
    order_model_free = order_model.add_variable(idx, "order_model_free", 0)
    order_model_free.set_modelling_rule(True)
    order_model_free.set_writable()
    order_model_availability = order_model.add_variable(idx, "order_model_availability", 0.0)
    order_model_availability.set_modelling_rule(True)
    order_model_availability.set_writable()
    order_model_performance = order_model.add_variable(idx, "order_model_performance", 0.0)
    order_model_performance.set_modelling_rule(True)
    order_model_performance.set_writable()
    order_model_quality = order_model.add_variable(idx, "order_model_quality", 0.0)
    order_model_quality.set_modelling_rule(True)
    order_model_quality.set_writable()
    order_model_oee = order_model.add_variable(idx, "order_model_oee", 0.0)
    order_model_oee.set_modelling_rule(True)
    order_model_oee.set_writable()

    # First a folder to organize our nodes
    order_folder = server.nodes.objects.add_folder(idx, "order_folder")

    order_model_ua_1 = order_folder.add_object(idx, "order_model_ua_1", order_model)
    order_model_ua_2 = order_folder.add_object(idx, "order_model_ua_2", order_model)
    order_model_ua_3 = order_folder.add_object(idx, "order_model_ua_3", order_model)

    ## permissions
    # order_model_ua.get_child("2:order_model_set_blue").set_writable()
    # order_model_ua.get_child("2:order_model_set_green").set_writable()
    # order_model_ua.get_child("2:order_model_add").set_writable()
    # order_model_ua.get_child("2:order_model_blue").set_writable()
    # order_model_ua.get_child("2:order_model_green").set_writable()
    # order_model_ua.get_child("2:order_model_free").set_writable()
    # order_model_ua.get_child("2:order_model_availability").set_writable()
    # order_model_ua.get_child("2:order_model_performance").set_writable()
    # order_model_ua.get_child("2:order_model_quality").set_writable()
    # order_model_ua.get_child("2:order_model_oee").set_writable()


    # creating a default event object
    # The event object automatically will have members for all events properties
    # you probably want to create a custom event type, see other examples
    myevgen = server.get_event_generator()
    myevgen.event.Severity = 300

    # starting!
    server.start()
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
