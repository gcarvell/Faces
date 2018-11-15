import tkinter as tk
import time
import random
import csv
from PIL import Image, ImageTk

app = tk.Tk()
app.title = "Facial Expressions"
app.geometry('800x600')
#app.resizable(0,0)
app.wm_attributes("-topmost", 1)

player = tk.Frame(app, width=400, height=300, pady=30)
player.pack()
canvas = tk.Frame(app, width=400, height=300)
canvas.pack()

class Session:
	def __init__(self, canvas, player):
		self.player = player
		self.canvas= canvas
		self.trialNumber = 0
		self.first = True
		self.init_time = int(round(time.time() * 1000))
		self.source = ["happy.jpg", "sad.jpg", "neutral.jpg"]
		self.morphs = random.sample(self.source, len(self.source))

	def start(self):
		self.nameLabel = tk.Label(canvas, text="Please enter your name:")
		self.nameLabel.pack(pady=10)
		self.enterName = tk.Entry(canvas)
		self.enterName.pack()
		self.enterName.focus_set()
		self.btn_start = tk.Button(canvas, text = "Click to Begin", width = 30, command = self.trial)
		self.btn_start.pack(padx=5, pady=10)

	def trial(self):
		if self.first:
			self.name = self.enterName.get()
			self.nameLabel.destroy()
			self.enterName.destroy()
			self.btn_start.destroy()
		self.trialNumber += 1
		print("Trial: "+ str(self.trialNumber))
		self.clip()
		self.init_time = self.current_time()
		self.buttons()

	def clip(self):
		print(self.morphs[self.trialNumber-1])
		image = Image.open(self.morphs[self.trialNumber-1])
		morph = ImageTk.PhotoImage(image)
		self.label = tk.Label(player, image=morph)
		self.label.image = morph
		self.label.pack()

	def buttons(self):
		self.btn_1 = tk.Button(canvas, text = "One", width = 20, command = self.b1)
		self.btn_1.pack(padx=5, pady=2)
		self.btn_2 = tk.Button(canvas, text = "Two", width = 20, command = self.b2)
		self.btn_2.pack(padx=5, pady=2)
		self.btn_3 = tk.Button(canvas, text = "Three", width = 20, command = self.b3)
		self.btn_3.pack(padx=5, pady=2)
		self.btn_4 = tk.Button(canvas, text = "Four", width = 20, command = self.b4)
		self.btn_4.pack(padx=5, pady=2)

	def b1(self):
		self.record(1)
	def b2(self):
		self.record(2)
	def b3(self):
		self.record(3)
	def b4(self):
		self.record(4)

	def removeButtons(self):
		self.btn_1.destroy()
		self.btn_2.destroy()
		self.btn_3.destroy()
		self.btn_4.destroy()
		self.label.destroy()

	def record(self, resp):
		self.removeButtons()
		f = open("%s Responses.csv" % self.name, "a", newline='')
		head = ["Trial", "Stimulus", "Response", "Latency"]
		elapsed_time = self.current_time() - self.init_time
		stim = self.morphs[self.trialNumber-1][:-4]
		response = [self.trialNumber, stim, resp, elapsed_time]
		try:
			writer = csv.writer(f)
			if self.first:
				writer.writerow(head)
				self.first = False
			writer.writerow(response)
		finally:
			f.close()
		self.canvas.after(1000, self.nextTrial)

	def nextTrial(self):
		if self.trialNumber == len(self.morphs):
			self.end()
		else:
			self.trial()

	def current_time(self):
		return int(round(time.time() * 1000))

	def end(self):
		self.exitLabel = tk.Label(canvas, text = "Thank you! Your results have been recorded")
		self.exitLabel.pack()
		self.btn_end = tk.Button(canvas, text = "Click to Exit", width = 30, command = self.endSession)
		self.btn_end.pack(padx=5, pady=10)

	def endSession(self):
		exit()

session = Session(canvas, player)
session.start()
app.mainloop()