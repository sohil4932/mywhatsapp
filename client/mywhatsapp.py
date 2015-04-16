import sys

from layer import EchoLayer
from yowsup.layers.auth                        import YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.protocol_presence           import YowPresenceProtocolLayer
from yowsup.layers.protocol_media              import YowMediaProtocolLayer
from yowsup.stacks import YowStack
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup import env
from config import config

CREDENTIALS = (config.ID, config.PASSWORD)

def send_message(destination, message, message_type):

    messages = [(destination, message, message_type)]
    
    layers = (EchoLayer,
              (YowAuthenticationProtocolLayer,
               YowMessagesProtocolLayer,
               YowReceiptProtocolLayer,
               YowAckProtocolLayer,
               YowPresenceProtocolLayer,
               YowMediaProtocolLayer)
              ) + YOWSUP_CORE_LAYERS
    
    stack = YowStack(layers)
    
    stack.setProp(EchoLayer.PROP_MESSAGES, messages)
    stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
    # Setting credentials
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)

    # WhatsApp server address
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)              
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())

    # Sending connecting signal
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
    try:
        # Program main loop
        stack.loop()
    except AuthError as e:
        print('Authentication error %s' % e.message)
        sys.exit(1)
        