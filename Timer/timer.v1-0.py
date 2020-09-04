import sys
if (sys.version_info > (3, 0)):
	import tkinter as tk
	from tkinter import ttk, PhotoImage, filedialog, messagebox
else:
	import Tkinter as tk
	import ttk
	import tkFileDialog as filedialog
	import tkMessageBox as messagebox
from datetime import datetime, timedelta
import json
import os


# display current time, refresh the text entry items
def displayTime():
    currentTime = datetime.utcnow() + timedelta(hours=float(tz.get()))
    timeLabel['text'] = currentTime.strftime('%I:%M:%S %p') + ' ' + tzDispValue.get()

    # if the timer is stopped, enable the ability to change values
    if startTimerButton.cget('bg') == '#CCCCCC':
        # if countdown is chosen, figure out the time the counter will expire, and display that in blue
        if isfloat(countdown.get()) and counterType.get() == 'down':
            try:
                countMinutes = float(countdown.get())
                timesUp = currentTime + timedelta(minutes=countMinutes)
                countToH.delete(0, tk.END)
                countToH.insert(0, timesUp.strftime('%I'))
                countToH.config(foreground='blue')
                countToM.delete(0, tk.END)
                countToM.insert(0, timesUp.strftime('%M'))
                countToM.config(foreground='blue')
                meridian.set(timesUp.strftime('%p'))
                apply(countToAM, (tkk, meridian) + tuple(meridianList))
            except:
                pass

        else:
            countToH.config(foreground='black')
            countToM.config(foreground='black')

        # if setting the timer for a specific time, calculate the number of minutes to set the countdown to
        if isfloat(countToH.get()) and isfloat(countToM.get()) and counterType.get() == 'up':
            try:
                timeMinutes = int(countToM.get())
                timeHours = int(countToH.get()) % 12
                if meridian.get() == 'PM':
                    timeHours = timeHours + 12
                deltaTime = currentTime.replace(hour=timeHours, minute=timeMinutes, second=0) - currentTime
                countMinutes = round(deltaTime.total_seconds() / 60, 6)
                if countMinutes < 0:
                    countMinutes = countMinutes + 1440
                countdown.delete(0, tk.END)
                countdown.insert(0, countMinutes)
                countdown.config(foreground='blue')
            except:
                messagebox.showerror("Error", "Values for HH and MM must be integers")

        else:
            countdown.config(foreground='black')

    r.after(200, displayTime)


# updates the countdown once the timer has started
def timerloop():
    if startTimerButton.cget('bg') == '#FF9900' and countdownValue > timedelta(seconds=0):
        currentTime = datetime.now().replace(microsecond=0)
        currentCount = countdownValue - (currentTime - startTime)
        countDisplay = str(currentCount).split('.')[0]
        clockLabel['text'] = countDisplay
        monitorLabel['text'] = countDisplay
        monitorTz['text'] = tzDispValue.get()
        activityLabel['text'] = activity.get()
        timesUp = 'Countdown to ' + countToH.get() + ':' + countToM.get() + ' ' + meridian.get() + ' ' + tzDispValue.get()
        timesUpLabel['text'] = timesUp
        if timerFileName:
            with open(timerFileName, 'w') as f:
                f.write(countDisplay)
        if activityFileName:
            with open(activityFileName, 'w') as f:
                f.write(activity.get())
        if countToFileName:
            with open(countToFileName, 'w') as f:
                f.write(timesUp)

    if startTimerButton.cget('bg') == '#FF9900' and currentCount > timedelta(seconds=0):
        r.after(500, timerloop)
    else:
        clockLabel['text'] = ""
        monitorLabel['text'] = ""
        startTimerButton.config(bg='#CCCCCC', highlightbackground='#CCCCCC')
        stopTimerButton.config(bg='#FF9900', highlightbackground='#FF9900')
        countdown.config(state=tk.NORMAL)
        countToH.config(state=tk.NORMAL)
        countToM.config(state=tk.NORMAL)
        countToAM.config(state=tk.NORMAL)
        countdown.delete(0, tk.END)
        countToH.delete(0, tk.END)
        countToM.delete(0, tk.END)
        rb1.config(state=tk.NORMAL)
        rb2.config(state=tk.NORMAL)
        if timerFileName:
            with open(timerFileName, 'w') as f:
                f.write(str(""))
        if countToFileName:
            with open(countToFileName, 'w') as f:
                f.write(str(""))


# Command from the Stop Timer button
def stopTimer():
    if isfloat(countdown.get()):
        startTimerButton.config(bg='#CCCCCC', highlightbackground='#CCCCCC')
        stopTimerButton.config(bg='#FF9900', highlightbackground='#FF9900')
        countdown.config(state=tk.NORMAL)
        countToH.config(state=tk.NORMAL)
        countToM.config(state=tk.NORMAL)
        countToAM.config(state=tk.NORMAL)
        rb1.config(state=tk.NORMAL)
        rb2.config(state=tk.NORMAL)

        currentCount = None
        timerloop()


# command from the start timer button
def startTimer(event):
    global startTime, countdownValue, currentCount
    if isfloat(countdown.get()):
        startTimerButton.config(bg='#FF9900', highlightbackground='#FF9900')
        stopTimerButton.config(bg='#CCCCCC', highlightbackground='#CCCCCC')
        startTime = datetime.now().replace(microsecond=0)
        countdownValue = timedelta(minutes=float(countdown.get()))
        currentCount = countdownValue
        countdown.config(state=tk.DISABLED)
        countToH.config(state=tk.DISABLED)
        countToM.config(state=tk.DISABLED)
        countToAM.config(state=tk.DISABLED)
        rb1.config(state=tk.DISABLED)
        rb2.config(state=tk.DISABLED)

        timerloop()


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# load the settings.json file
def getSettings():
    global timerFileName, activityFileName, countToFileName, activityListFileName, tzOffset, tzDisp
    timerFileName = ''
    activityFileName = ''
    countToFileName = ''
    activityListFileName = ''
    tzOffset = '0'
    tzDisp = ''
    try:
        with open('settings.json') as infile:
            settingDict = json.load(infile)
            timerFileName = settingDict['timerFileName']
            activityFileName = settingDict['activityFileName']
            countToFileName = settingDict['countToFileName']
            activityListFileName = settingDict['activityListFileName']
            tzOffset = settingDict['tzOffset']
            tzDisp = settingDict['tzDisp']
    except:
        messagebox.showerror("Error", "settings.json file missing")

    timerCountdownFPValue.insert(0, timerFileName)
    activityFPValue.insert(0, activityFileName)
    countdownToFPValue.insert(0, countToFileName)
    activityListFPValue.insert(0, activityListFileName)
    tz.set(tzOffset)
    tzDispValue.insert(0, tzDisp)


# save the settings.json file
def saveSettings():
    settingDict = {
        "timerFileName": timerCountdownFPValue.get(),
        "activityFileName": activityFPValue.get(),
        "countToFileName": countdownToFPValue.get(),
        "activityListFileName": activityListFPValue.get(),
        "tzOffset": tz.get(),
        "tzDisp": tzDispValue.get(),
    }

    with open('settings.json', 'w') as outfile:
        json.dump(settingDict, outfile)


# function for file browsing (choosing file locations from settings page)
def saveFileDialog(initDir):
    filePath = os.path.split(initDir.get())
    fileName = filePath[1]

    if '.' in fileName:
        fileExt = '*.' + fileName.split('.')[1]
        fileTypes = {(fileName.split('.')[1] + ' files', fileExt),
                     ("all files", "*.*")}
    else:
        fileExt = '  '
        fileTypes = {("all files", "*.*")}

    if filePath[0] == '':
        filePathStr = os.getcwd()
    else:
        filePathStr = filePath[0]

    saveFile = filedialog.asksaveasfilename(initialdir=filePathStr,
                                            title="Select file",
                                            filetypes=fileTypes,
                                            initialfile=fileName,
                                            defaultextension=fileExt[1])

    if saveFile:
        initDir.delete(0, tk.END)
        initDir.insert(0, saveFile)


# close timer window
def exitTimer():
    if timerFileName:
        with open(timerFileName, 'w') as f:
            f.write(str(""))
    if countToFileName:
        with open(countToFileName, 'w') as f:
            f.write(str(""))
    r.destroy()


# set-up window
global r
r = tk.Tk()
r.title('AWS T&C Timer v1.0')
r.geometry("700x500")

# tabs
tabControl = ttk.Notebook(r)

global tab1, tab2, tab3
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Timer')
tabControl.add(tab2, text='Display')
tabControl.add(tab3, text='Settings')
tabControl.pack(expand=1, fill='both')



# ==================================================================================
# tab 1 - Timer
ttk.Label(tab1, text='Current Time').grid(column=0, row=0, padx=5, pady=5)

# current time
timeLabel = ttk.Label(tab1)
timeLabel.grid(column=1, row=0, padx=5, pady=5, columnspan=4, sticky=tk.W)

# counter type selection - count down, or count up to a specific time
counterType = tk.StringVar()

# make default counterType the countdown
counterType.set('down')

rb1 = ttk.Radiobutton(tab1, text='Countdown', variable=counterType, value='down')
rb1.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
rb2 = ttk.Radiobutton(tab1, text='Count to', variable=counterType, value='up')
rb2.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)

ttk.Label(tab1, text='minutes').grid(column=3, row=1, padx=5, pady=5, sticky=tk.W)
ttk.Label(tab1, text='HH : MM').grid(column=1, row=3, padx=5, pady=5, columnspan=4, sticky=tk.W)

monitorTz = ttk.Label(tab1)
monitorTz.grid(column=4, row=2, padx=0, pady=5, sticky=tk.W)
monitorTz.config(font=("San Serif", 10), foreground='#FF9900')

# timer text entry
countdown = ttk.Entry(tab1, width=6)
countdown.grid(column=1, row=1, padx=5, pady=5, columnspan=4, sticky=tk.W)
countdown.focus_set()
countdown.bind('<KP_Enter>', startTimer)
countdown.bind('<Return>', startTimer)


countToH = ttk.Entry(tab1, width=3)
countToH.grid(column=1, row=2, padx=5, pady=5, sticky=tk.W)

countToM = ttk.Entry(tab1, width=3)
countToM.grid(column=2, row=2, padx=0, pady=5, sticky=tk.W)

# AM / PM drop-down
meridianList = ['AM', 'PM']
meridian = tk.StringVar(r)
meridian.set(meridianList[1])
countToAM = ttk.OptionMenu(tab1, meridian, meridianList[0], *meridianList)
countToAM.grid(column=3, row=2, padx=0, pady=5, sticky=tk.W)

activityList = ["-Break-", "-Class Starts-", "-Lunch-", "-Lab-"]

ttk.Label(tab1, text='Displayed Activity').grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)
stl = ttk.Style()
stl.configure("CA.TMenubutton", font=("San Serif", 20), foreground='#005276')
activity = tk.StringVar(r)
classActivities = ttk.OptionMenu(tab1, activity, activityList[0], *activityList, style="CA.TMenubutton")
classActivities.grid(column=1, row=4, padx=0, pady=5, columnspan=4, sticky=tk.W)

startTimerButton = tk.Button(tab1, text="Start Timer", width=25, bg='#CCCCCC', highlightbackground='#CCCCCC', command=lambda: startTimer(0))
startTimerButton.grid(column=1, row=5, padx=0, pady=5, columnspan=4, sticky=tk.W)

stopTimerButton = tk.Button(tab1, text="Stop Timer", width=25, bg='#CCCCCC', highlightbackground='#CCCCCC', command=stopTimer)
stopTimerButton.grid(column=1, row=6, padx=0, pady=5, columnspan=4, sticky=tk.W)

monitorLabel = ttk.Label(tab1)
monitorLabel.grid(column=1, row=8, padx=0, pady=5, columnspan=4)
monitorLabel.config(font=("San Serif", 20), foreground='#FF9900')

# ==================================================================================
# tab2 - Display

logo = tk.PhotoImage(file="aws_logo_smile.gif")

logoLabel = ttk.Label(tab2, image=logo)
logoLabel.grid(column=0, row=0, padx=5, pady=5)

activityLabel = ttk.Label(tab2)
activityLabel.grid(column=0, row=1, padx=5, pady=5)
activityLabel.config(font=("San Serif", 60), foreground='#005276')

clockLabel = ttk.Label(tab2)
clockLabel.grid(column=0, row=2, padx=5, pady=5)
clockLabel.config(font=("San Serif", 60), foreground='#FF9900')

timesUpLabel = ttk.Label(tab2)
timesUpLabel.grid(column=0, row=3, padx=5, pady=5)
timesUpLabel.config(font=("San Serif", 30), foreground='#232F3E')

tab2.columnconfigure(0, weight=1)
tab2.rowconfigure(0, weight=1)
tab2.rowconfigure(3, weight=1)

# ==================================================================================
# tab3 - Settings

timerCountdownFPLabel = ttk.Label(tab3, text='Timer countdown file path')
timerCountdownFPLabel.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
timerCountdownFPValue = ttk.Entry(tab3, width=40)
timerCountdownFPValue.grid(column=1, row=0, padx=0, pady=5, sticky=tk.W)

timerCountdownSaveAs = ttk.Button(tab3, text='Browse', command=lambda: saveFileDialog(timerCountdownFPValue))
timerCountdownSaveAs.grid(column=2, row=0, padx=0, pady=5, sticky=tk.W)

activityFPLabel = ttk.Label(tab3, text='Activity output file path')
activityFPLabel.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
activityFPValue = ttk.Entry(tab3, width=40)
activityFPValue.grid(column=1, row=1, padx=0, pady=5, sticky=tk.W)

activityFPSaveAs = ttk.Button(tab3, text='Browse', command=lambda: saveFileDialog(activityFPValue))
activityFPSaveAs.grid(column=2, row=1, padx=0, pady=5, sticky=tk.W)

countdownToFPLabel = ttk.Label(tab3, text='Countdown to file path')
countdownToFPLabel.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)
countdownToFPValue = ttk.Entry(tab3, width=40)
countdownToFPValue.grid(column=1, row=2, padx=0, pady=5, sticky=tk.W)

countdownToSaveAs = ttk.Button(tab3, text='Browse', command=lambda: saveFileDialog(countdownToFPValue))
countdownToSaveAs.grid(column=2, row=2, padx=0, pady=5, sticky=tk.W)

activityListFPLabel = ttk.Label(tab3, text='Activity list file path')
activityListFPLabel.grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)
activityListFPValue = ttk.Entry(tab3, width=40)
activityListFPValue.grid(column=1, row=3, padx=0, pady=5, sticky=tk.W)

activityListSaveAs = ttk.Button(tab3, text='Browse', command=lambda: saveFileDialog(activityListFPValue))
activityListSaveAs.grid(column=2, row=3, padx=0, pady=5, sticky=tk.W)

tz = tk.StringVar(r)

tzDispLabel = ttk.Label(tab3, text='Time Zone Display')
tzDispLabel.grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)
tzDispValue = ttk.Entry(tab3, width=10)
tzDispValue.grid(column=1, row=4, padx=0, pady=5, sticky=tk.W)

offsetList = []
for ofst in range(-120, 145, 5):
    offsetList.append(ofst / 10.0)

tzOffsetLabel = ttk.Label(tab3, text='Time Zone Offset from UTC')
tzOffsetLabel.grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)
tzOffsetValue = ttk.OptionMenu(tab3, tz, "0", *offsetList)
tzOffsetValue.grid(column=1, row=5, padx=0, pady=5, sticky=tk.W)

saveButton = ttk.Button(tab3, text='Save', command=saveSettings)
saveButton.grid(column=1, row=6, padx=0, pady=5, sticky=tk.W)

# ==================================================================================

exitButton = tk.Button(r, text='Exit', width=25, command=exitTimer)
exitButton.pack()

getSettings()

try:
    with open(activityListFileName) as classActivity:
        activityList = json.load(classActivity)
        classActivities['menu'].delete(0,'end')
        for activity_item in activityList:
            classActivities['menu'].add_command(label=activity_item, command=tk._setit(activity, activity_item))
        activity.set(activityList[0])
except:
    messagebox.showerror("Error", "Activity List file missing")

displayTime()
r.mainloop()