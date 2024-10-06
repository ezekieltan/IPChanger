import wmi
import ctypes


def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def getNicConfigs():
    nicConfigs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)
    return nicConfigs

def getInterfacesPreviewList():
    # Obtain network adaptors configurations
    nicConfigs = getNicConfigs()
    indexedNicConfigs = [(index, item) for index, item in enumerate(nicConfigs)]
    previewList = [str(x[0]) + ' : ' + x[1].Caption + ' ' + str(x[1].IPAddress) for x in indexedNicConfigs]
    return previewList

def setIP(enteredIP, subnetMask, enteredGateway, setGateway, interfaceIndex):
    nicConfigs = getNicConfigs()
    nic = nicConfigs[interfaceIndex]
    print(nic)
    nic.EnableStatic(IPAddress=[enteredIP],SubnetMask=[subnetMask])
    if setGateway:
        nic.SetGateways(DefaultIPGateway=[enteredGateway])
    else:
        # https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/setgateways-method-in-class-win32-networkadapterconfiguration
        # "To clear the gateway, set your gateway to the same IP you use on EnableStatic."
        output = nic.SetGateways(DefaultIPGateway=[enteredIP])

def setAuto(interfaceIndex):
    nicConfigs = getNicConfigs()
    nic = nicConfigs[interfaceIndex]
    nic.EnableDHCP()