from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import PresenceProtocolEntity
from yowsup.layers.protocol_media.protocolentities       import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
import threading

class EchoLayer(YowInterfaceLayer):

    def __init__(self):
        super(EchoLayer, self).__init__()
        self.ackQueue = []
        self.lock = threading.Condition()

    # List of (jid, message) tuples
    PROP_MESSAGES = "org.openwhatsapp.yowsup.prop.sendclient.queue"

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery")
        self.toLower(ack)

    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        self.lock.acquire()
        for target in self.getProp(self.__class__.PROP_MESSAGES, []):
            phone, message, message_type = target
            print "Message type : " + message_type
            if int(message_type) == 1:
                print "Sending message"
                if '@' in phone:
                    messageEntity = TextMessageProtocolEntity(message, to = phone)
                elif '-' in phone:
                    messageEntity = TextMessageProtocolEntity(message, to = "%s@g.us" % phone)
                else:
                    messageEntity = TextMessageProtocolEntity(message, to = "%s@s.whatsapp.net" % phone)
                self.ackQueue.append(messageEntity.getId())
                self.toLower(messageEntity)
            elif int(message_type) == 2:
                print "Sending Image"
                if '@' in phone:
                    self.demoContactJid = phone
                elif '-' in phone:
                    self.demoContactJid = "%s@g.us" % phone
                else:
                    self.demoContactJid = "%s@s.whatsapp.net" % phone
                 
                self.filePath = message 
                requestUploadEntity = RequestUploadIqProtocolEntity("image", filePath = message)
                self._sendIq(requestUploadEntity, self.onRequestUploadResult, self.onRequestUploadError)
        self.lock.release()

    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        self.lock.acquire()

        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))

        if not len(self.ackQueue):
            self.lock.release()
            print("Message sent")
            raise KeyboardInterrupt()

        self.lock.release()

    def onRequestUploadResult(self, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        mediaUploader = MediaUploader(self.demoContactJid, self.getOwnJid(), self.filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      self.onUploadSuccess, self.onUploadError, self.onUploadProgress)
        mediaUploader.start()

    def onRequestUploadError(self, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        print("Error requesting upload url")

    def onUploadSuccess(self, filePath, jid, url):
        #convenience method to detect file/image attributes for sending, requires existence of 'pillow' library
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, None, to)
        self.toLower(entity)

    def onUploadError(self, filePath, jid, url):
        print("Upload file failed!")