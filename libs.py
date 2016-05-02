from easysnmp import Session
from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp
import os
import signal

session = Session(hostname='192.168.1.70', community='public', version=2)

class trap:

    def cbFun(self, transportDispatcher, transportDomain, transportAddress, wholeMsg):
        #print os.getpid()
        #print "job done"
        os.kill(os.getpid(), signal.SIGUSR1)

    def __init__(self):
        transportDispatcher = AsyncoreDispatcher()
        transportDispatcher.registerRecvCbFun(self.cbFun)
        transportDispatcher.registerTransport(udp.domainName, udp.UdpSocketTransport().openServerMode(('192.168.1.111', 162))) #PC IP ADRESS
        transportDispatcher.jobStarted(1)
        try:
            transportDispatcher.runDispatcher()
        except:
            transportDispatcher.closeDispatcher()
            raise

class counter():
    def __init__(self, snmp):
        self.snmp = snmp
        self.previous = self.get_counter()

    def get_counter(self):
        count = int(session.get(self.snmp).value)
        return count

    def delta(self):
        delt = self.get_counter() - self.previous
        return delt

    def job_reset(self):
        self.previous = self.get_counter()


