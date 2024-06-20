# v0.9.0 pre3

import tkinter
import tkinter.ttk as ttk
import os
import requests
import json

root = tkinter.Tk()
root.resizable(False, False)

path_current = f'{os.path.dirname(os.path.realpath(__file__))}'
path_names = f'{path_current}\\data\\names.txt'
path_allnames = f'{path_current}\\data\\allnames.txt'
path_pr = f'{path_current}\\data\\priority.txt'
path_temp = f'{path_current}\\data\\temp.txt'
path_dir = f'{path_current}\\data'

# --- Options ---
view = 6  # max views
autoSwitch = True  # auto scene switch

# --- Advanced Options ---
usePr = False  # ONLY TRUE IF USE PRIORITY
switchPr = 4  # priority that automatically switches the scene. default priorities: -1=nodata, 0=no priority
usePaceManAPI = False  # [beta feature] automatically reset the priority using PaceManAPI. for PaceCatcherBot (usePr must be true)

# main
class Application(tkinter.Frame):
  def __init__(self, master = None):
    super().__init__(master)

    # set
    self.master.title('Simple MultiView Controller')
    self.master.geometry(f'234x{view*32+42}')

    # defs
    def getallnames(path, path_dir):
      if os.path.isdir(path_dir) == False:
        os.makedirs(path_dir)
      try:
        with open(path, 'x', encoding='utf-8') as f:
          f.write('')
      except FileExistsError:
        pass
      with open(path, encoding='utf-8') as f:
        name = f.read().splitlines()
        name.insert(0, '')
      return name

    def Refresh():
      name_list = []
      with open(path_names, encoding='utf-8') as f:
        name = f.read().splitlines()
      with open(path_names, 'w', encoding='utf-8') as f:
        with open(path_pr, encoding='utf-8') as e:
          pr = e.read().splitlines()
          pr_int = [int(s) for s in pr]
        with open(path_pr, 'w', encoding='utf-8') as e:
          for l in range(len(combobox)):
            name_list.append(combobox[l].get())
            if usePr:
              if combobox[l].get() == '':
                pr[l] = '-1'
                radio[l].configure(text='-1')
              elif combobox[l].get() in name_list and pr_int[l] == -1:
                pr[l] = '0'
                radio[l].configure(text='0')
          if focusnum.get() < len(combobox):
            name_list[0], name_list[focusnum.get()] = name_list[focusnum.get()], name_list[0]
          f.writelines('\n'.join(name_list))
          if usePr:
            e.writelines('\n'.join(pr))
          if autoSwitch:
            f.writelines(f'\n{focusnum.get()}')
          else:
            f.writelines(f'\n-1')
        name = getallnames(path_allnames, path_dir)
      for l in range(view):
        combobox[l].configure(value=name)

    def Clear():
      with open(path_names, 'w', encoding='utf-8') as f:
        f.writelines('\n'*len(combobox)+'-1')

    def TempLoad():
      with open(path_names, encoding='utf-8') as f:
        name = f.read().splitlines()
        dummy = name.pop()
      try:
        with open(path_temp, 'x', encoding='utf-8') as f:
          f.write('')
      except FileExistsError:
        pass
      with open(path_temp, encoding='utf-8') as f:
        temp = f.read().splitlines()
        if (len(temp)) != 2:
          temp = ''
          with open(path_temp, 'w', encoding='utf-8') as f:
            f.write('')
        if len(temp):
          with open(path_pr, encoding='utf-8') as e:
            pr = e.read().splitlines()
            pr_int = [int(s) for s in pr]
            pr_min = min(pr_int)
          if int(pr_min) <= int(temp[1]):
            combobox_list = []
            for l in range(view):
              combobox_list.append(combobox[l].get())
            if temp[0] in combobox_list:
              d = combobox_list.index(temp[0])
              name[d] = temp[0]
              radio[d].configure(text=temp[1])
              pr[d] = f'{temp[1]}'
              pr_int[d] = int(temp[1])
              if switchPr <= max(pr_int) <= int(temp[1]):
                focusnum.set(d)
              elif switchPr <= max(pr_int):
                focusnum.set(pr.index(str(max(pr_int))))
              else:
                focusnum.set(view)
            else:
              d = pr.index(str(pr_min))
              name[d] = temp[0]
              combobox[d].set(temp[0])
              combobox_list[d] = temp[0]
              radio[d].configure(text=temp[1])
              pr[d] = f'{temp[1]}'
              pr_int[d] = int(temp[1])
              if switchPr <= int(temp[1]):
                focusnum.set(d)
              elif switchPr <= max(pr_int):
                focusnum.set(pr.index(str(max(pr_int))))
              else:
                focusnum.set(view)
          if usePr:
            if usePaceManAPI:
              nickname_list = []
              url = requests.get('https://paceman.gg/api/ars/liveruns')
              data = json.loads(url.text)
              for l in range(len(data)):
                nickname_list.append(data[l]['nickname'])
              print(f'nickname_list: {nickname_list}')
              for l in range(len(combobox_list)):
                if combobox_list[l] not in nickname_list:
                  print(f'not in nickname list: {combobox_list[l]}')
                  if pr[l] != '-1':
                    pr[l] = '0'
                    pr_int[l] = 0
                    radio[l].configure(text='0')
                    if switchPr <= max(pr_int):
                      focusnum.set(pr.index(str(max(pr_int))))
                    elif switchPr > max(pr_int):
                      focusnum.set(view)
          with open(path_pr, 'w', encoding='utf-8') as f:
            f.writelines('\n'.join(pr))
          with open(path_temp, 'w', encoding='utf-8') as f:
            f.write('')
          with open(path_names, 'w', encoding='utf-8') as f:
            f.writelines('\n'.join(name))
            if autoSwitch:
              f.writelines(f'\n{focusnum.get()}')
            else:
              f.writelines(f'\n-1')
          with open(path_temp, 'w', encoding='utf-8') as f:
            f.write('')
          app.after(1000, Refresh)
      app.after(3000, TempLoad)

    def PrReset():
      with open(path_pr, encoding='utf-8') as f:
        pr = f.read().splitlines()
        if var.get() != view:
          if combobox[var.get()].get() == '':
            pr[var.get()] = '-1'
            radio[var.get()].configure(text='-1')
            var.set(view)
          else:
            pr[var.get()] = '0'
            radio[var.get()].configure(text='0')
            var.set(view)
        with open(path_pr, 'w', encoding='utf-8') as f:
          f.writelines('\n'.join(pr))
      app.after(500, PrReset)

    # get all names
    name = getallnames(path_allnames, path_dir)

    # set labels and comboboxes
    combobox = []
    for l in range(view):
      label = ttk.Label(root, text=f'Player {l+1}')
      label.place(x=8, y=(l)*32+8)
      combobox.append(ttk.Combobox(root, value=name, state='readonly', width=12))
      combobox[l].place(x=64, y=(l)*32+8)
    
    # set focus radios
    focusnum = tkinter.IntVar()
    focusnum.set(view)
    for l in range (view+1):
      radio = ttk.Radiobutton(root, value=l, variable=focusnum)
      radio.place(x=206, y=(l)*32+7)
    
    # set buttons
    radio = []
    var = tkinter.IntVar()
    var.set(view)
    try:
      with open(path_pr, 'x', encoding='utf-8') as f:
        f.write('-1\n'*(view-1)+'-1')
    except FileExistsError:
      pass
    with open(path_pr, encoding='utf-8') as f:
      pr = f.read().splitlines()
    for l in range(view):
      radio.append(ttk.Radiobutton(root, value=l, text=pr[l], variable=var))
      radio[l].place(x=170, y=(l)*32+7)
    radio.append(ttk.Radiobutton(root, value=l+1, variable=var))
    radio[l+1].place(x=170, y=(l+1)*32+7)

    button_other = ttk.Button(root, text='Refresh', command=Refresh, width=14)
    button_other.place(x=62, y=(view)*32+7)

    button_other = ttk.Button(root, text='Clear', command=Clear, width=5)
    button_other.place(x=8, y=(view)*32+7)
    
    # set after
    if usePr:
      self.after(500, TempLoad)
      self.after(500, PrReset)

app = Application(master = root)
app.mainloop()