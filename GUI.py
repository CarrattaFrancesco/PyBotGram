#importi basic toolkit for view
from sys import version_info

if version_info.major == 2:
    # Python 2.x
    from Tkinter import *
    from Tkinter.ttk import *

elif version_info.major == 3:
    # Python 3.x
    from tkinter import *
    from tkinter.ttk import *



class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

root=Tk()
root.title("PyGramBot")


app=FullScreenApp(root)

Label(root, text="First").grid(row=0, sticky=W)
Label(root, text="Second").grid(row=1, sticky=W)

e1 = Entry(root)
e2 = Entry(root)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

root.mainloop()