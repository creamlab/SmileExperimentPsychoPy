from Tkinter import *

class MyDialog:
    def __init__(self, parent):
        self.parent=parent
        pad=3
        self._geom='200x200+0+0'
        parent.geometry("{0}x{1}+0+0".format(
        parent.winfo_screenwidth()-pad, parent.winfo_screenheight()-pad))
        parent.bind('<Escape>',self.toggle_geom)
        
        top = self.top = Toplevel(parent)
        
        Label(top, text = "Age : ").pack()
        self.e = Entry(top)
        self.e.pack(padx = 5)
        
        Label(top, text="H/F : ").pack()
        self.e = Entry(top)
        self.e.pack(padx = 5)
        
        Label(top, text="Homme/Femme ? ").pack()
        self.e = Entry(top)
        self.e.pack(padx = 5)
        b = Button(top, text = "OK", command = self.ok)
        b.pack(pady=5)

    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

    def ok(self):

        print "value is", self.e.get()
        self.top.destroy()


root = Tk()
d   = MyDialog(root)
root.wait_window(d.top)
