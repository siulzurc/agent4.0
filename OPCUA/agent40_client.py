#Author: Santiago Gil
import sys
sys.path.insert(0, "..")
import logging
import time

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()


from opcua import Client
from opcua import ua


class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("KeepAlive")
    #logger.setLevel(logging.DEBUG)

    client = Client("opc.tcp://admin@localhost:4840/tum/ai40server/")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
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
        uri = "agent40/application"
        idx = client.get_namespace_index(uri)

        #folders
        order_folder = client.get_node("ns=2;i=12")

        #models
        order_model = client.get_node("ns=2;i=1")

        order_model_ua_4 = order_folder.add_object(idx, "order_model_ua_4", order_model)

        order_model_set_blue_4 = order_model_ua_4.get_child("2:order_model_set_blue")
        order_model_set_blue_4.set_value(11)

        order_model_ua_5.get_child("2:order_model_set_blue")


        # subscribing to a variable node
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        #sub.subscribe_data_change(var)

        time.sleep(0.1)

        # we can also subscribe to events from server
        sub.subscribe_events()
        # sub.unsubscribe(handle)
        # sub.delete()

        # calling a method on server
        #res = obj.call_method("{}:multiply".format(idx), 3, "klk")
        #print("method result is: ", res)

        embed()
    finally:
        client.disconnect()
