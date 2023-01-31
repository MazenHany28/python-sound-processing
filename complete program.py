#importing libraries
import sounddevice as sd 
import librosa
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk 
from tkinter import filedialog as fd
import pyrubberband as pyrb
import soundfile as sf

#defining functions
def readfile():
    audiofile=fd.askopenfilename(title='choose a file')
    global y,ymodified,time,timemodified,sr
    y,sr=librosa.load(audiofile)
    time=np.arange(len(y))/sr
    timemodified=time
    ymodified=y
    
def savefile():
    savedfile=fd.asksaveasfilename(title='Save As',
                                   filetypes=[("wav file", ".wav")],
                                   defaultextension=".wav")
    sf.write(savedfile, ymodified, sr,subtype='PCM_24')
    
def timeshift():
   global timemodified,sr,ymodified
   n = float(ent_timesh.get())
   nsec = int(n*sr)
   if nsec>0:
       ymodified=np.pad(ymodified, (nsec,0))
       timemodified=np.arange(len(ymodified))/sr
   else:
       ymodified=np.pad(ymodified, (0,abs(nsec)))
       timemodified=np.arange(len(ymodified))/sr
def timescale():
    n = abs(float(ent_timesc.get()))
    global ymodified,timemodified
    ymodified=pyrb.time_stretch(ymodified, sr, n)
    timemodified=np.arange(len(ymodified))/sr
def reflect():
    global ymodified
    ymodified=ymodified[::-1]
def amplitudescale():
    n = abs(float(ent_ampsc.get()))
    global ymodified
    ymodified=n*ymodified
def plotdata():
    global y,ymodified,time,timemodified
    fig, ax =plt.subplots(2,1)
    ax[0].plot(time,y,color='red',label='original signal')
    ax[1].plot(timemodified,ymodified,color='blue',label='modified signal')
    for i in range(2):
        ax[i].grid()
        ax[i].set(xlabel='time(s)'
               ,ylabel='amplitude'
                )
        if i ==0:
            ax[i].set_title('audio wave')
        ax[i].legend()
def playsound():
    global ymodified,sr
    sd.play(ymodified,sr)
def reset():
    global ymodified,y,timemodified,time
    ymodified = y
    timemodified = time
    
#building interface
window = tk.Tk()
window.title("Mazen Hany")
frame=[1,2,3,4,5,6]
for i in range(6):
    frame[i] = tk.Frame(master=window)
    frame[i].pack(fill=tk.BOTH, expand=True,padx=5,pady=5)
butt_path=tk.Button(frame[0],text="select file",command=readfile,width=30)
butt_path.pack(padx=10,pady=10)
label_timesh=tk.Label(frame[1],text="TIME SHIFTING")
label_timesh.pack(padx=5,pady=5)
ent_timesh=tk.Entry(frame[1])
ent_timesh.pack(padx=5,pady=5)
butt_timesh=tk.Button(frame[1],text="perform",command=timeshift)
butt_timesh.pack(padx=5,pady=5)
label_timesc=tk.Label(frame[2],text="TIME SCALING")
label_timesc.pack(padx=5,pady=5)
ent_timesc=tk.Entry(frame[2])
ent_timesc.pack(padx=5,pady=5)
butt_timesc=tk.Button(frame[2],text="perform",command=timescale)
butt_timesc.pack(padx=5,pady=5)
label_reflect=tk.Label(frame[3],text="REFLECTION")
label_reflect.pack(padx=5,pady=5)
butt_reflect=tk.Button(frame[3],text="perform",command=reflect)
butt_reflect.pack(padx=5,pady=5)
label_ampsc=tk.Label(frame[4],text="AMPLITUDE SCALING")
label_ampsc.pack(padx=5,pady=5)
ent_ampsc=tk.Entry(frame[4])
ent_ampsc.pack(padx=5,pady=5)
butt_ampsc=tk.Button(frame[4],text="perform",command=amplitudescale)
butt_ampsc.pack(padx=5,pady=5)
butt_plot=tk.Button(frame[5],text="plot",command=plotdata)
butt_plot.pack(padx=5,pady=5)
butt_playsound=tk.Button(frame[5],text="play sound",command=playsound)
butt_playsound.pack(padx=5,pady=5)
butt_save=tk.Button(frame[5],text="Save AS",command=savefile)
butt_save.pack(padx=5,pady=5)
butt_reset=tk.Button(frame[5],text="Reset",command=reset)
butt_reset.pack(padx=5,pady=5)
window.mainloop()