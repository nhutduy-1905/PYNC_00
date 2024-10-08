import tkinter as tk
from tkinter import ttk
import math
from tkinter import Button
from tkinter import scrolledtext
from tkinter import messagebox
win = tk.Tk()
#Tiêu đề
win.title("Caculator")

tabControl = ttk.Notebook(win)
# Tạo tab 1 (tab tính toán phương trình bậc 2)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="GIẢI PHƯƠNG TRÌNH BẬC HAI")

# Hiển thị tab control 
tabControl.grid(column=0, row=0)

#Chữ a 
Label1= ttk.Label(tab1,text="Hệ số a ")
Label1.grid(column=0,row = 1) # colum: cột, row : hàng 

# Nhập 
input_a = ttk.Entry(tab1,width = 12)
input_a.grid(column=0, row =2)

# Chữ b
Label2= ttk.Label(tab1,text="Hệ số b")
Label2.grid(column=0,row = 3)

# Nhập b
input_b = ttk.Entry(tab1,width = 12)
input_b.grid(column= 0, row = 4)

#  Chữ
Label3= ttk.Label(tab1,text="Hệ số c")
Label3.grid(column=0,row = 5)

# Nhập
input_c = ttk.Entry(tab1,width = 12)
input_c.grid(column=0, row =6)

# scrol
scrol_w = 30
scrol_h = 10
scr = scrolledtext.ScrolledText(tab1, width = scrol_w, height = scrol_h, wrap = tk.WORD)
scr.grid(column=0, row=8, padx=10, pady=5)
# Tạo hàm tính toán
def solve():
  try:
      a = float(input_a.get())
      b = float(input_b.get())
      c = float(input_c.get())
      #tinh delta
      delta = b**2 - 4*a*c
      if delta < 0:
            scr.insert(tk.INSERT, "\nPhương trình vô nghiệm")
      elif delta > 0:
            x1 = (-b + math.sqrt(delta)) / (2*a)
            x2 = (-b - math.sqrt(delta)) / (2*a)
            scr.insert(tk.INSERT,"\nPhương trình có hai nghiệm phân biệt: \n" f"x1 = {x1:.2f}\n x2 = {x2:.2f}")  
      else:
           x = -b / (2*a)
           scr.insert(tk.INSERT, f"\n Nghiệm kép: x1 = x2 = {x:.2f}")  
  except ValueError:
         scr.insert(tk.INSERT,"\n Nhập sai dữ liệu. ")  
  except ZeroDivisionError:
         scr.insert(tk.INSERT,"\nLỗi đầu vào.Không được nhập số 0 tại hệ số a cho phương trình bậc 2.Mời bạn nhập lại.")  
button_math = ttk.Button(win,text = "Enter",command = solve)
button_math.grid(column = 0, row = 7)
# menu

menubar = tk.Menu(win)
setting_menu = tk.Menu(menubar,tearoff=0)
setting_menu.add_command(label = "Appearence",command=win.quit)

help_menu = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label="Setting", menu=setting_menu)
menubar.add_cascade(label ="Help",menu=help_menu)
def show_menu():
    messagebox.showinfo("Menu caculator")
help_menu.add_command(label="About",command=win)
# menu win
win.config(menu=menubar)

#--------------------------Tab2-----------------------------
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text="TÍNH TAM GIÁC")

# Nhãn
label_x = ttk.Label(tab2,text ="Cạnh x")
label_x.grid(column=0,row=1)
#Nhập
input_x = ttk.Entry(tab2,width=12)
input_x.grid(column=0, row = 2)
#Nhãn
label_y = ttk.Label(tab2,text ="Cạnh y")
label_y.grid(column=0,row=3)
#Nhập
input_y = ttk.Entry(tab2,width=12)
input_y.grid(column=0, row = 4)

#Nhãn
label_z = ttk.Label(tab2,text ="Cạnh z")
label_z.grid(column=0,row=5)
#Nhập
input_z = ttk.Entry(tab2,width=12)
input_z.grid(column=0, row = 6)
# Hiện kết quả
scrol_w1 = 30
scrol_h1 = 10
scr_champ = scrolledtext.ScrolledText(tab2, width = scrol_w1, height = scrol_h1, wrap = tk.WORD)
scr_champ.grid(column=0, row=8)
#Tính toán
def tinhtoan():
     try:
            x = float(input_x.get())
            y = float(input_y.get())
            z = float(input_z.get())
            if x + y > z and x + z > y and y + z > x:
                s = (x + y + z) / 2  
                dien_tich = math.sqrt(s * (s - x) * (s - y) * (s - z)) 
                scr_champ.insert(tk.INSERT, f"Diện tích tam giác: {dien_tich:.2f}\n")
            else:
             scr.insert(tk.INSERT, "Không thể tạo thành tam giác.\n")
     except ValueError:
        scr.insert(tk.INSERT, "Nhập số không hợp lệ.\n")

# Nút tính diện tích tam giác
button_tinhtoan = ttk.Button(tab2, text="Tính diện tích", command=tinhtoan)
button_tinhtoan.grid(column=0, row=7)
# Thoát 
class Exit():
    def __init__(self,done):
      self.done = done
      self.quit_button = Button(done, text="Exit", command=self.quit)
      self.quit_button.grid(column = 0, row = 9)
    def quit(self):
        self.done.quit()
Exit_App = Exit(win)
#Dòng win để chạy 
win.mainloop()
       