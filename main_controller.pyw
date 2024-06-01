# v0.7.0

import tkinter
import tkinter.ttk as ttk
import os

root = tkinter.Tk()
root.resizable(False, False)

path_current = f'{os.path.dirname(os.path.realpath(__file__))}'
path_names = f'{path_current}\\data\\names.txt'
path_allnames = f'{path_current}\\data\\allnames.txt'
path_eval = f'{path_current}\\data\\evaluation.txt'
path_temp = f'{path_current}\\data\\temp.txt'
path_dir = f'{path_current}\\data'

# --- Options ---
view = 6  # max views
autoswitch = True  # auto scene switch

# --- Advanced Option ---
pacecatcher = False  # ONLY TRUE IF USE PACECATCHER

# main
class Application(tkinter.Frame):
  def __init__(self, master = None):
    super().__init__(master)

    # set
    self.master.title('Simple MultiView Controller')
    self.master.geometry(f'192x{view*32+42}')

    # defs
    def getallnames(path, path_dir):
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
      return name

    def Refresh():
      name_list = []
      with open(path_names) as f:
        name = f.read().splitlines()
      with open(path_names, 'w') as f:
        with open(path_eval) as e:
          eval = e.read().splitlines()
        with open(path_eval, 'w') as e:
          for l in range(len(combobox)):
            name_list.append(combobox[l].get())
            if pacecatcher:
              if combobox[l].get() == '':
                eval[l] = '-1'
              elif combobox[l].get() not in name:
                eval[l] = '0'
          if focusnum.get() < len(combobox):
            name_list[0], name_list[focusnum.get()] = name_list[focusnum.get()], name_list[0]
            if pacecatcher:
              eval[0], eval[focusnum.get()] = eval[focusnum.get()], eval[0]
          f.writelines('\n'.join(name_list))
          if pacecatcher:
            e.writelines('\n'.join(eval))
          if autoswitch:
            f.writelines(f'\n{focusnum.get()}')
          else:
            f.writelines(f'\n-1')
        name = getallnames(path_allnames, path_dir)
      for l in range(view):
        combobox[l].configure(value=name)

    def Clear():
      with open(path_names, 'w') as f:
        f.writelines('\n'*len(combobox)+'-1')

    def TempLoad():
      with open(path_names) as f:
        name = f.read().splitlines()
        dummy = name.pop()
      try:
        with open(path_temp, 'x') as f:
          f.write('')
      except FileExistsError:
        pass
      with open(path_temp) as f:
        temp = f.read().splitlines()
        if len(temp):
          if temp[0] not in name:
            try:
              with open(path_eval, 'x') as f:
                f.write('0\n0\n0\n0\n0\n0')
            except FileExistsError:
              pass
            with open(path_eval) as e:
              eval = e.read().splitlines()
            eval_min = int(min(eval))
            if int(eval_min) <= int(temp[1]):
              for l in range(view):
                if int(eval.index(eval_min)) == l:
                  name[l] = temp[0]
                  combobox[l].set(temp[0])
                  break
              eval[eval.index(eval_min)] = f'{temp[1]}'
              with open(path_eval, 'w') as f:
                f.writelines('\n'.join(eval))
              with open(path_temp, 'w') as f:
                f.write('')
              with open(path_names, 'w') as f:
                f.writelines('\n'.join(name))
                if autoswitch:
                  f.writelines(f'\n{focusnum.get()}')
                else:
                  f.writelines(f'\n-1')
              with open(path_temp, 'w') as f:
                f.write('')
      app.after(5000, TempLoad)

    def EvalSwitch():
      with open(path_eval) as f:
        eval = f.read().splitlines()
      with open(path_names) as f:
        name = f.read().splitlines()
      # evaluation: -1=NoPlayer, 0= Nothing, 1=FS, 3=SS, 4=B, 5=E, 6=SSPB, 7=EE, 8=BPB, 9=EPB, 10=EEPB
      if 4 <= int(max(eval)):
        focusnum.set(eval.index(max(eval)))
        name[len(name)-1] = max(eval)
      else:
        focusnum.set(view)
        name[len(name)-1] = str(view)
      with open(path_names, 'w') as f:
        f.writelines('\n'.join(name))
      app.after(5000, EvalSwitch)

    # get all names
    name = getallnames(path_allnames, path_dir)

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
    
    if pacecatcher:
      self.after(5000, TempLoad)
      self.after(5000, EvalSwitch)


app = Application(master = root)
app.mainloop()
