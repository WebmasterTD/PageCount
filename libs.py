from easysnmp import Session
from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp
import os
import signal
                            #PRINTER IP
session = Session(hostname='192.168.1.70', community='public', version=2)

class trap:
    #Callback function fro SNMP Trap
    def cbFun(self, transportDispatcher, transportDomain, transportAddress, wholeMsg):
        os.kill(os.getpid(), signal.SIGUSR1)
    #SNMP Trap init setup
    def __init__(self):
        transportDispatcher = AsyncoreDispatcher()
        transportDispatcher.registerRecvCbFun(self.cbFun)
        transportDispatcher.registerTransport(udp.domainName, udp.UdpSocketTransport().openServerMode(('192.168.1.111', 162))) #RASPBERRY   /   PC IP ADRESS
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
    #Read snmp value
    def get_counter(self):
        count = int(session.get(self.snmp).value)
        return count
    #Difference in values from last reset
    def delta(self):
        delt = self.get_counter() - self.previous
        return delt
    #Reset counter
    def job_reset(self):
        self.previous = self.get_counter()
