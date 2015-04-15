import sys

from layer import EchoLayer
from yowsup.layers.auth                        import YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.protocol_presence           import YowPresenceProtocolLayer
from yowsup.stacks import YowStack
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup import env

CREDENTIALS = ("919137195248", "bwoN7y9B/c08GnSz/5/icXceNnM=")

def send_message(destination, message, message_type):

    ''' destination is <phone number> without '+'
        and with country code of type string,
        message is string
        e.g send_message('11133434343','hello')
    '''
    print "Sending message to : " + str(destination) + " with : " + str(message)
    messages = [(destination, message, message_type)]
    
    layers = (EchoLayer,
              (YowAuthenticationProtocolLayer,
               YowMessagesProtocolLayer,
               YowReceiptProtocolLayer,
               YowAckProtocolLayer,
               YowPresenceProtocolLayer)
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

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('%s send number message\nrecv\n' % sys.argv[0])
        sys.exit(1)
    if sys.argv[1] == 'send':
        try:
            send_message(sys.argv[2],sys.argv[3],sys.argv[4])
        except KeyboardInterrupt:
            print('closing')
            sys.exit(0)