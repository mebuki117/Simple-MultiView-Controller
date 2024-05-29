# v0.3.1

import tkinter
import tkinter.ttk as ttk
import os

root = tkinter.Tk()
root.resizable(False, False)

# --- Option ---
view = 6  # max views

# main
class Application(tkinter.Frame):
  def __init__(self, master = None):
    super().__init__(master)

    # set
    self.master.title('Simple MultiView Controller')
    self.master.geometry(f'192x{view*32+42}')

    # defs
    def Refresh():
      name_list = []
      path = f'{os.path.dirname(os.path.realpath(__file__))}\\data\\names.txt'
      with open(path, 'w') as f:
        for l in range(len(combobox)):
          if focusnum.get() == l:
            name_list.insert(0, combobox[l].get())
          else:
            name_list.append(combobox[l].get())
        f.writelines('\n'.join(name_list))
        f.writelines('\n'.join('\n'))

    def Clear():
      path = f'{os.path.dirname(os.path.realpath(__file__))}\\data\\names.txt'
      with open(path, 'w') as f:
        for l in range(len(combobox)):
          f.writelines('\n'.join('\n'))

    # get all names
    path = f'{os.path.dirname(os.path.realpath(__file__))}\\data\\allnames.txt'
    path_dir = f'{os.path.dirname(os.path.realpath(__file__))}\\data'

    if os.path.isdir(path_dir) == False:
      os.makedirs(path_dir)
    try:
      with open(path, 'x') as f:
        f.write('')
    except FileExistsError:
      pass
    with open(path) as f:
      name = f.read().splitlines()
      name.insert(0, '')

    # set labels and comboboxes
    combobox = []
    for l in range(view):
      label = tkinter.Label(root, text=f'Player {l+1}')
      label.place(x=8, y=(l)*32+8)
      combobox.append(ttk.Combobox(root, value=name, state='readonly', width=12))
      combobox[l].place(x=64, y=(l)*32+8)
    
    # set focus radios
    focusnum = tkinter.IntVar()
    focusnum.set(view)
    for l in range (view+1):
      radio = tkinter.Radiobutton(root, value=l, variable=focusnum)
      radio.place(x=164, y=(l)*32+8)
    
    # set buttons
    button = tkinter.Button(root,text="Refresh",command=Refresh,width=12)
    button.place(x=64, y=(view)*32+8)

    button = tkinter.Button(root,text="Clear",command=Clear, width=5)
    button.place(x=8, y=(view)*32+8)

app = Application(master = root)
app.mainloop()