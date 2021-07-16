import psutil
import functions

runningproc = functions.runningProcessesImportant()

uptime = []
for proc in runningproc:
    uptime.append([functions.getProcessUptime(proc)])

print(uptime)

functions.saveData(uptime)