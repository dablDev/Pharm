import Mod.IntegrationTypes as it



class fcsNotificationEF(it.zfcs_notificationEFType):
    "Извещение о проведении ЭА (электронный аукцион)"
    
    def __init__(self, dic):
        it.zfcs_notificationEFType.__init__(self, dic)
        
class fcsProtocolEF1(it.zfcs_protocolEF1Type):
    "Протокол рассмотрения заявок на участие в электронном аукционе"
    
    def __init__(self, dic):
        it.zfcs_protocolEF1Type.__init__(self)
    