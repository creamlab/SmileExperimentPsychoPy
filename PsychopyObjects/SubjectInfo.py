from Tkinter import *

class SubjectInfo():
	def __init__(self):
		self.Age 	= None 
		self.HF  	= None
		self.master = None

	def callback(self):
		Age = self.Age.get()
		HF 	= self.HF.get()
		self.master.destroy()

	def main(self):
		self.master = Tk()

		#Fullscreenmode:
		pad = 3
		self.master._geom='200x200+0+0'
		self.master.geometry("{0}x{1}+0+0".format(
		self.master.winfo_screenwidth()-pad, self.master.winfo_screenheight()-pad))

		#H/F
		Label(self.master, text="Homme/Femme ? ").pack()
		self.HF = Entry(self.master)
		self.HF.pack(padx = 5)

		#Age
		Label(self.master, text="Age en chiffres ").pack()
		self.Age = Entry(self.master)
		self.Age.pack(padx = 5)

		e = Button(self.master, text = "OK", command = self.callback)
		e.pack(pady=5)
		mainloop()

SI = SubjectInfo()
SI.main()