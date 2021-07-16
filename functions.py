import psutil
import time
import os
import datetime
from datetime import timedelta
import csv
import pandas as pd

#functions for engine

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

def getCurrentUptimesAndNames():
    '''
    Listing all currently executed programs plus their current runtimes
    :return: Data that can be saved by saveData(data) into csv
    '''
    runningproc = runningProcessesImportant()
    data = []
    for proc in runningproc:
        data.append([proc, getProcessUptime(proc)])
    return data

#functions for csv-data

def saveUptimes(data):
    '''
    Provisional saveData function
    :param data: Data of executed (important) programs and their runtime
    :return: 0 (mainly for saving a .csv file)
    '''
    dataframe = pd.DataFrame(data, columns=['Name', 'Uptime'])
    dataframe.to_csv(r'C:\Users\Manuel Kleinschmager\Desktop\Time Tracker\Uptimes.csv')
    return 0

def saveCurrentUptimes(data):
    '''
        Provisional saveData function
        :param data: Data of currently executed (important) programs and their runtime
        :return: 0 (mainly for saving a .csv file)
        '''
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(r'C:\Users\Manuel Kleinschmager\Desktop\Time Tracker\CurrentUptimes.csv')
    return 0

def readCSV():
    '''
    Reads CSV data of current uptimes
    :return: .csv-savable data
    '''
    currentData = pd.read_csv(r'C:\Users\Manuel Kleinschmager\Desktop\Time Tracker\Uptimes.csv', index_col=0)
    return currentData

def splitUpCSV():
    '''
    Function to split up the .csv-file into separat dataFrames to make reading easier
    :return: b file with *.exe names and c file with uptimes
    '''
    data = readCSV()
    names = data['Name']
    uptimes = data['Uptime']
    return names, uptimes

def getAssociatedCSVUptime(proc):
    '''

    :param proc: name of process
    :return: Asscociated CSV-Uptime to process
    '''
    data = readCSV()
    b = data.loc['1', 'Names']
    return b

#other functions

def execute():
    '''

    :return:
    '''
    #saving (important) executables
    uptimes = getCurrentUptimesAndNames()
    saveUptimes(uptimes)

    # load data csv
    database = readCSV()

    while True:

        #load data engine
        currentProcesses = runningProcessesImportant()
        currentUptimes = getCurrentUptimesAndNames()

        #setting currently running executables to new value
        index = 0
        for name in database['Name']:
            if checkIfProcessRunning(name):
                database.iloc[index, 1] = getProcessUptime(name)

            index = index + 1

        index2 = 0
        for name in currentProcesses:
            if name in database['Name']:
                print('no')
            else:
                runTime = currentUptimes[index2][1]
                dataFrame = pd.DataFrame([[name, runTime]], columns=['Name', 'Uptime'])
                database.append(dataFrame)

            index2 = index2 + 1
            #TODO list index out of range error

        print(database)
        time.sleep(10)




    #TODO: check if *.exe are still running

        #TODO: YES: update data by overwriting existing data to that executable
        #TODO: NO: pass

    #TODO: check if already saved executable is running again
        #TODO: YES: update runtime by adding new current runtime to existing runtime
        #TODO: NO: pass
    #time.sleep(10)

    return 0