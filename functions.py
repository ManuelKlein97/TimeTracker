import psutil
import time
import os
import datetime
from datetime import timedelta
import csv

def checkIfProcessRunning(processName):
    '''
    checks if specific process is running (by name)
    :param processName: Name of the process
    :return: True if currently running, false if not
    '''
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def findProcessByName(processName):
    '''
    Finds all currently running processes with specific process name
    :param processName: Name of the process you want to overview
    :return: List (strings) of all current running processes by that name
    '''

    list_processes = []
    for proc in psutil.process_iter():
        try:
            if proc.name() == processName:
                list_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return list_processes

def findProcessIdByName_dict(processName):
    '''
    Finds all currently running processes with specific process name
    :param processName: Name of the process you want to overview
    :return: List (Process class [psutil]) of all current running processes by that name
    '''
    listOfProcessObjects = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            if processName.lower() in pinfo['name'].lower():
                listOfProcessObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return listOfProcessObjects

def runningProcessesImportant():
    '''
    Sorts out all 'not important' processes currently running
    :return: List of important processes wanted to get the data from
    '''
    useless = ['backgroundTaskHost.exe', 'System Idle Process', 'System', 'Registry', 'dllhost.exe', 'RadeonSoftware.exe', 'smss.exe', 'svchost.exe', 'csrss.exe',
 'wininit.exe', 'services.exe', 'lsass.exe', 'fontdrvhost.exe', 'ctfmon.exe', 'amdfendrsr.exe', 'atiesrxx.exe', 'Memory Compression',
 'cpumetricsserver.exe', 'WacomHost.exe', 'conhost.exe', 'SteelSeriesEngine.exe', 'cmd.exe', 'ROCCAT_Swarm_Monitor.exe',
 'jusched.exe', 'armsvc.exe', 'novapdfs.exe', 'PnkBstrA.exe', 'AdobeUpdateService.exe', 'WTabletServicePro.exe',
 'LogiRegistryService.exe', 'RtkAudUService64.exe', 'MsMpEng.exe', 'AGSService.exe', 'OriginWebHelperService.exe',
 'AGMService.exe', 'OfficeClickToRun.exe', 'jucheck.exe', 'dasHost.exe', 'TeamViewer_Service.exe', 'HxOutlook.exe',
 'AdobeCollabSync.exe', 'AMDRSServ.exe', 'GamingServicesNet.exe', 'GamingServices.exe', 'fsnotifier64.exe', 'unsecapp.exe',
 'ApplicationFrameHost.exe', 'cncmd.exe', 'RuntimeBroker.exe', 'spoolsv.exe', 'LCore.exe', 'SearchApp.exe',
 'ShellExperienceHost.exe', 'NisSrv.exe', 'sihost.exe', 'Wacom_TouchUser.exe', 'GoogleCrashHandler.exe', 'MoUsoCoreWorker.exe',
 'GoogleCrashHandler64.exe', 'audiodg.exe', 'SgrmBroker.exe', 'amdow.exe', 'HxTsr.exe', 'Wacom_Tablet.exe',
 'CredentialUIBroker.exe', 'SystemSettings.exe', 'SearchFilterHost.exe', 'TextInputHost.exe', 'taskhostw.exe',
 'SearchIndexer.exe', 'dwm.exe', 'WinStore.App.exe', 'SecurityHealthService.exe', 'SearchProtocolHost.exe', 'smartscreen.exe',
 'SecurityHealthSystray.exe', 'AcrobatNotificationClient.exe', 'explorer.exe', 'SettingSyncHost.exe',
 'StartMenuExperienceHost.exe', 'muachost.exe', 'YourPhone.exe', 'atieclxx.exe', 'LockApp.exe', 'AMDRSSrcExt.exe',
 'OneDrive.exe', 'WmiPrvSE.exe', 'winlogon.exe', 'python.exe', 'Wacom_TabletUser.exe',
 'laclient.exe', 'UserOOBEBroker.exe', 'SteelSeriesGG.exe', 'WWAHost.exe', 'winpty-agent.exe', 'QMxNetworkSync.exe']
    list1 = []
    all = runningProcessesNames()
    for elem in all:
        if elem not in useless:
            list1.append(elem)

    final_list = list(dict.fromkeys(list1))

    return final_list

def runningProcessesNames():
    '''
    :return: All currently running processes by name
    '''
    names = []
    process_pids = psutil.pids()
    for proc in psutil.process_iter(['name']):
        names.append(proc.name())
    return names

def getProcessUptime(processName):
    '''

    :param processName: Name of the process
    :return: Uptime of the wanted process in seconds
    '''
    createtime_float = findProcessByName(processName)[0].create_time()
    create_time = datetime.datetime.fromtimestamp(createtime_float)
    current_time = datetime.datetime.now()
    new_time = current_time - create_time
    uptime = new_time.total_seconds()

    #Maybe change the return to another format (Min, Sec)?
    minuten = int(uptime / 60)
    sekunden = round(uptime - minuten * 60, 2)

    return uptime



def saveData(data):
    #TODO Marius
            
    return 0