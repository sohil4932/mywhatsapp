from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import PresenceProtocolEntity
from yowsup.layers.protocol_media.protocolentities       import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
import threading
from config import config

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
        for target in self.getProp(self.__class__.PROP_MESSAGES, []):
            phone, message, message_type = target
            if int(message_type) == config.MESSAGE:
                print "Sending message"
                if '@' in phone:
                    messageEntity = TextMessageProtocolEntity(message, to = phone)
                elif '-' in phone:
                    messageEntity = TextMessageProtocolEntity(message, to = "%s@g.us" % phone)
                else:
                    messageEntity = TextMessageProtocolEntity(message, to = "%s@s.whatsapp.net" % phone)
                self.ackQueue.append(messageEntity.getId())
                self.toLower(messageEntity)
            elif int(message_type) == config.IMAGE:
                print "Sending Image"
                if '@' in phone:
                    jid = phone
                elif '-' in phone:
                    jid = "%s@g.us" % phone
                else:
                    jid = "%s@s.whatsapp.net" % phone
                path = message
                print "Sending image to : " + jid + " with : " + path
                entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, filePath=path)
                successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, path, successEntity, originalEntity)
                errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)
                self._sendIq(entity, successFn, errorFn)

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

    def doSendImage(self, filePath, url, to, ip = None):
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to)
        self.toLower(entity)

    def onRequestUploadResult(self, jid, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendImage(filePath, resultRequestUploadIqProtocolEntity.getUrl(), jid,
                             resultRequestUploadIqProtocolEntity.getIp())
        else:
            # successFn = lambda filePath, jid, url: self.onUploadSuccess(filePath, jid, url, resultRequestUploadIqProtocolEntity.getIp())
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      self.onUploadSuccess, self.onUploadError, self.onUploadProgress, async=False)
            mediaUploader.start()

    def onRequestUploadError(self, jid, path, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        logger.error("Request upload for file %s for %s failed" % (path, jid))

    def onUploadSuccess(self, filePath, jid, url):
        self.doSendImage(filePath, url, jid)

    def onUploadError(self, filePath, jid, url):
        logger.error("Upload file %s to %s for %s failed!" % (filePath, url, jid))

    def onUploadProgress(self, filePath, jid, url, progress):
        sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        sys.stdout.flush()