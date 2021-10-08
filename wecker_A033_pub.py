"""
This code is experemental and not very good. 
There are a lot ways to do it better: your challange?

Its just for tests and learning purposes.
(And fits a personal need.)

it shows tools for:
♦ time handling 
♦ audio
♦ tkinter GUI
♦ not in use, but how to set a thread [def start_music()]


Alpha 03
"""

from time import strftime
import tkinter as tk
from tkinter.constants import END
import pygame
import sounddevice
import threading
import ctypes
import time
#hides pygame console
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )


MP3FILE = "C:\\full\\path\\to\\sound\\loop\\track.mp3"
VIETNAM = "C:\\full\\path\\to\\sound\\first\\track.mp3"
APP_TITLE = "Wecker mit Tkinter"
APP_XPOS = 100
APP_YPOS = 100
APP_WIDTH = 300
APP_HEIGHT = 400

LABEL_01_FONT = ('Helevtica', 14, 'bold')
LABEL_BG = 'light blue'
LABEL_ALARM_BG = 'red'



class Application(tk.Frame):
    #not in use yet.
    def get_audio_devices(self):
        devs = sounddevice.query_devices()
        for dev in devs:
            print(dev['hostapi'] , dev['name'])
            return devs

    #limits charakters to two in entry
    def character_limit(self, label:tk.Entry):
        while label.get().__len__()>2:
            label.delete(0,1)

    def character_entry(self):
        self.character_limit(self.entry_std) 
        self.character_limit(self.entry_min)
        self.character_limit(self.entry_sec)

    def __init__(self, master):
        self.my_mp3 = MP3FILE
        self.devs = self.get_audio_devices()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.pre_init(devicename='Lautsprecher (Realtek High Definition Audio)')
        pygame.mixer.init()
        pygame.init()
        self.LoopWindow(master)

    #should implement to chose a sound device for output
    def SoundDeviceWindow():
        pass

    def LoopWindow(self, master):
        self.master = master
        tk.Frame.__init__(self, master)

        self.act_time_var = tk.StringVar()
        tk.Label(self, textvariable=self.act_time_var, font=LABEL_01_FONT, fg='green').pack()

        label_frame = tk.Frame(self, bg=LABEL_BG, padx=2, pady=2)
        label_frame.pack(pady=4)
        
        self.label_01 = tk.Label(label_frame, text='Weckzeit angeben:', font=LABEL_01_FONT, bg=LABEL_BG)
        self.label_01.pack()
        
        self.label_02 = tk.Label(label_frame, text='ss:mm(:ss)', bg=LABEL_BG)
        self.label_02.pack()
        
        time_frame = tk.Frame(self)
        time_frame.pack(pady=4)
        entry_frame = tk.Frame(time_frame)
        entry_frame.pack(pady=4)

        

        time_controll_frame = tk.Frame(time_frame)
        time_controll_frame.pack()


        std_time_controll_frame = tk.Frame(time_controll_frame)
        std_time_controll_frame.pack(pady=1, side='left')
        min_time_controll_frame = tk.Frame(time_controll_frame)
        min_time_controll_frame.pack(pady=1, side='left')
        sec_time_controll_frame = tk.Frame(time_controll_frame)
        sec_time_controll_frame.pack(pady=1, side='left')


#minus Buttons
        minusOneStdButton = tk.Button(std_time_controll_frame, width=3, height=1, text='▲10', command=lambda:self.change_std(10))
        minusOneStdButton.pack()
        minusfiveStdButton = tk.Button(std_time_controll_frame, width=3, height=1, text='▲ 5', command=lambda:self.change_std(5))
        minusfiveStdButton.pack()
        minusTenStdButton = tk.Button(std_time_controll_frame, width=3, height=1, text='▲ 1', command=lambda:self.change_std(1))
        minusTenStdButton.pack()

        minusOneMinButton = tk.Button(min_time_controll_frame, width=3, height=1, text='▲10', command=lambda:self.change_min(10))
        minusOneMinButton.pack()
        minusfiveMinButton = tk.Button(min_time_controll_frame, width=3, height=1, text='▲ 5', command=lambda:self.change_min(5))
        minusfiveMinButton.pack()
        minusTenMinButton = tk.Button(min_time_controll_frame, width=3, height=1, text='▲ 1', command=lambda:self.change_min(1))
        minusTenMinButton.pack()

#timetable
        self.entry_std = tk.Entry(std_time_controll_frame, width=4, justify='center')
        self.entry_std.pack()
        self.entry_std.insert(0, '00')
        
        self.entry_min = tk.Entry(min_time_controll_frame, width=4, justify='center')
        self.entry_min.pack()
        self.entry_min.insert(0, '00')

        self.entry_sec = tk.Entry(sec_time_controll_frame, width=4, justify='center')
        self.entry_sec.pack()
        self.entry_sec.insert(0, '00')
#plus buttons
        plusOneStdButton = tk.Button(std_time_controll_frame, width=3, height=1, text='▼ 1', command=lambda:self.change_std(1, True))
        plusOneStdButton.pack()
        plusfiveStdButton = tk.Button(std_time_controll_frame, width=3, height=1, text='▼ 5', command=lambda:self.change_std(5, True))
        plusfiveStdButton.pack()
        plusTenStdButton = tk.Button(std_time_controll_frame, width=3, height=1, text='▼10', command=lambda:self.change_std(10, True))
        plusTenStdButton.pack()

        plusOneMinButton = tk.Button(min_time_controll_frame, width=3, height=1, text='▼ 1', command=lambda:self.change_min(1, True))
        plusOneMinButton.pack()
        plusfiveMinButton = tk.Button(min_time_controll_frame, width=3, height=1, text='▼ 5', command=lambda:self.change_min(5, True))
        plusfiveMinButton.pack()
        plusTenMinButton = tk.Button(min_time_controll_frame, width=3, height=1, text='▼10', command=lambda:self.change_min(10, True))
        plusTenMinButton.pack()
 
        self.alarm_set_var = tk.IntVar()
        self.alarm_set_var.set(1)
        self.checkbox = tk.Checkbutton(time_controll_frame, text='An', onvalue=1, offvalue=0,variable=self.alarm_set_var)
        self.checkbox.pack(expand=False, side='right')
        self.checkbox = tk.Button(time_controll_frame, width=1, height=1, text='♠', command=lambda:self.paste_current_time())
        self.checkbox.pack(expand=False, side='right')

        controll_frame = tk.Frame(self)
        controll_frame.pack(pady=4)

        Button1 = tk.Button(controll_frame, width=7, height=1, text='▶', command=self.play)
        Button2 = tk.Button(controll_frame, width=7, height=1, text='■', command=self.stop)
        Button3 = tk.Button(controll_frame, width=7, height=1, text='▐▐', command=self.pause)

        Button1.pack(pady=4, side='left')
        Button2.pack(pady=4, side='left')
        Button3.pack(pady=4, side='left')

        self.alarm_flag = True
        self.label_frame = label_frame

        
        self.update_time()

    def set_time(self, int_std, int_min, int_sec):
        if int_std<10:
            int_std = '0' + str(int_std)
        if int_min<10:
            int_min = '0' + str(int_min)
        if int_sec<10:
            int_sec = '0' + str(int_sec)

        self.entry_std.delete(0,END)
        self.entry_std.insert(0, int_std)
        self.entry_min.delete(0,END)
        self.entry_min.insert(0, int_min)
        self.entry_sec.delete(0,END)
        self.entry_sec.insert(0, int_sec)

    # 24h format
    def correct_time(self):
        self.character_entry()
        int_sec = int(self.entry_sec.get())
        int_min = int(self.entry_min.get())
        int_std = int(self.entry_std.get())

        if int_sec>=60:
            int_sec = int_sec%60
            int_min +=1
        elif int_sec<0:
            int_sec = int_sec%60
            int_min -=1

        if int_min<0:
            int_min = 60+int_min
            int_std -=1
        elif int_min>=60:
            int_min = int_min%60
            int_std +=1
        
        if int_std<0:
            int_std = 24+int_std
        elif int_std>=24:
            int_std = int_std%24

        self.set_time(int_std, int_min, int_sec)
        
    def paste_current_time(self):
        hour_int, min_int = map(int, time.strftime("%H %M").split())
        self.set_time(hour_int, min_int, 0)

    # plus/minus button functions
    def change_std(self,time=0,sub=False):
        std_int = int(self.entry_std.get())
        self.entry_std.delete(0,END)
        if time:
            if sub:
                self.entry_std.insert(2,str(std_int-time))
            else:
                self.entry_std.insert(2,str(std_int+time))

    # plus/minus button functions
    def change_min(self,time=0,sub=False):
        min_int = int(self.entry_min.get())
        self.entry_min.delete(0,END)
        if time:
            if sub:
                self.entry_min.insert(2,str(min_int-time))
            else:
                self.entry_min.insert(2,str(min_int+time))
         
    # music button functions
    def play(self):
        pygame.mixer.music.load(self.my_mp3)
        pygame.mixer.music.play()
    def stop(self):
        pygame.mixer.music.stop()
    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    # only continues until checkbox is True
    def play_until_end(self):
        volume = 0.4
        playlist = []
        playlist.append(VIETNAM)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.load(playlist.pop())  # Get the first track from the playlist
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        
        while alarm:=self.alarm_set_var.get():
            while pygame.mixer.music.get_busy():
                if alarm:
                    continue  
                else:
                    print('stopped')
                    pygame.mixer.music.stop()
            else:
                if len(playlist)==0:
                    print('QueLen():' , len(playlist))
                    playlist.append(self.my_mp3)
                    print('add queue')
                if len(playlist) > 0:       # If there are more tracks in the queue...
                    pygame.mixer.music.queue(playlist.pop()) # Q
                    print('add queue')
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play()
                if volume <= 0.8:
                        volume += 0.2
                print('Volume:', volume)

    # pygame has problems with play music in threads: not a good idea
    def start_music(self):
        player = threading.Thread(target=self.play_until_end, daemon=True)      
        player.start()

    # Main clock loop
    def update_time(self):
        self.correct_time()
        act_time = strftime('%H:%M:%S')
        self.act_time_var.set(act_time)

        alarm_time = "{}:{}:{}".format(
            self.entry_std.get(),
            self.entry_min.get(),
            self.entry_sec.get())
                    
        if self.alarm_set_var.get():
            if alarm_time == act_time:
                self.alarm_display(True)
                
                self.start_music()
                
        else:
            if self.alarm_flag:
                self.alarm_display(False)
                     
        self.after(100, self.update_time)

    #alarm animation. bg = background
    def alarm_display(self, alarm=False):
        self.alarm_flag = alarm
        if alarm:
            self.label_frame['bg'] = LABEL_ALARM_BG
            self.label_01['bg'] = LABEL_ALARM_BG
            self.label_02['bg'] = LABEL_ALARM_BG
        else:
            self.label_frame['bg'] = LABEL_BG
            self.label_01['bg'] = LABEL_BG
            self.label_02['bg'] = LABEL_BG

def main():
    app_win = tk.Tk()
    app_win.title(APP_TITLE)
    app_win.geometry("+{}+{}".format(APP_XPOS, APP_YPOS))
    app_win.geometry("{}x{}".format(APP_WIDTH, APP_HEIGHT))
    app = Application(app_win).pack(expand=True)
    
    app_win.mainloop()
 
if __name__ == '__main__':
    print('begin')
    main()     