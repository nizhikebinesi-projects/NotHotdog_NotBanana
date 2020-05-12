import pandas as pd
import numpy as np

import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from skimage.io import imread
from glob import glob
from pathlib import Path

from random import shuffle

import gc

import os
# if file does not exist write header

invalids = []

cache = []

df_name = 'nothotdog_notbanana_data.csv'
columns = ['path', 'hotdog', 'banana']

assessed_paths = []

exist = os.path.isfile(df_name)
if exist:
    df = pd.read_csv(df_name)
    assessed_paths = df['path'].tolist()
    del df
    gc.collect()

root = tkinter.Tk()
root.wm_title("NotHotdog_NotBanana assessing tool")


r_var = tkinter.BooleanVar()
r_var.set(0)
h_var = tkinter.BooleanVar()
h_var.set(0)
b_var = tkinter.BooleanVar()
b_var.set(0)

v = tkinter.StringVar()
tkinter.Label(root, textvariable=v).pack(side=tkinter.TOP)

 
#if not os.path.isfile('filename.csv'):
#   df.to_csv('filename.csv', header='column_names')
#else: # else it exists so append without writing the header
#   df.to_csv('filename.csv', mode='a', header=False)

def is_image(x):
    ext = x.split('.')[-1]
    accepted = {'jp', 'png', 'gif'}
    for a in accepted:
        if a in ext.lower():
            return True
    return False

def on_enter():
    global images, cache, path, r_var, h_var, b_var, left, size, df_name, columns, exist

    cache.append(
        (path, int(h_var.get()), int(b_var.get()))
    )
    #print(cache)

    r_var.set(0)
    h_var.set(0)
    b_var.set(0)

    left -= 1

    path = next(images)

    v.set(str(left) + " left\n" + str(size - left) + ' assessed\n' + path)
    fig.get_axes()[0].imshow(imread(path))
    canvas.draw()

    gc.collect()
    
    if len(cache) == 100 or left == 0:
        df = pd.DataFrame(cache)
        args = {
            'path_or_buf': df_name,
            'header': columns,
        }
        if exist:
            args['header'] = False
            args['mode'] = 'a'
        else:
            exist = os.path.isfile(df_name)
        df.to_csv(**args)
        del cache, df
        gc.collect()
        cache = []


#def on_enter1(event):
#    global images, df, cache, path
#    path = next(images)
#    fig.get_axes()[0].imshow(imread(path))
#    canvas.draw()
#    
#    if len(cache) > 100:
#        df = pd.DataFrame(cache)
#        args = {
#            'path_or_buf': df_name,
#            'header': columns,
#        }
#        if exist:
#            args['header'] = False
#            args['mode'] = 'a'
#        df.to_csv(**args)


def is_interesting(x):
    f = x.lower().split('/')[1]
    if 'insta_data' in f and ('banana' in x or 'hotdog' in x):
        return True
    if 'food-101' in f and 'hot_dog' in x:
        return True
    if 'downloads' in f and ('dog' in x or 'banana' in x or 'frankf' in x or 'minion' in x):# or 'kfc' in x or 'mcdonalds' in x):# or 'subway' in x):
        return True
    if 'data' == f and ('sausage' in x or 'dog' in x or 'frankf' in x or 'banana' in x):
        return True
    return False
#def get_valid_path(images):
#    global invalids, left
#    path = next(images)
#    try:
#        imread(path)
#    except:
#        invalids.append(path)
#        left -= 1
#        return next(images)
#    return path


images = set(list(filter(lambda x: is_image(x) and is_interesting(x), (map(str, Path('../').glob('**/*.*'))))))
assessed_paths = set(assessed_paths)
images = images.difference(assessed_paths)

del assessed_paths
gc.collect()

images = list(images)
shuffle(images)
left = len(images)
size = len(images)
images = iter(images)

path = next(images)

v.set(str(left) + " left\n" + str(size - left) + ' assessed\n' + path)

#frame = tkinter.Frame(root)
#frame.bind()

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
#fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))


fig.add_subplot(111).imshow(imread(path))
fig.get_axes()[0].axis('off')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)




def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

radio = tkinter.Frame(master=root)


hotdog = tkinter.Checkbutton(text="Hotdog", variable=h_var, onvalue=1, offvalue=0, master=radio)
banana = tkinter.Checkbutton(text="Banana", variable=b_var, onvalue=1, offvalue=0, master=radio)
ready = tkinter.Checkbutton(text="I'm ready for the next image!", variable=r_var, onvalue=1, offvalue=0, master=root)


hotdog.pack(side=tkinter.LEFT)
banana.pack(side=tkinter.LEFT)

radio.pack()

ready.pack()

#button = tkinter.Button(master=root, text="Quit", command=_quit)
#button.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH)

enter = tkinter.Button(root, text=u'Send a result', command=on_enter)
#enter.bind('<Enter>', on_enter1)
enter.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH)

def on_key_press(event):
    global r_var, b_var, h_var
#    print("you pressed {}".format(event.key))
    if event.key == '1':
        h_var.set(not bool(h_var.get()))
    if event.key == '2':
        b_var.set(not bool(b_var.get()))
    if event.key == '3':
        r_var.set(not bool(r_var.get()))
    if r_var.get() and event.key == 'enter':
        on_enter()
    #key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)

def on_closing():
    global cache, df_name, exist, columns
    if len(cache):
        df = pd.DataFrame(cache)
        args = {
            'path_or_buf': df_name,
            'header': columns,
        }
        if exist:
            args['header'] = False
            args['mode'] = 'a'
        else:
            exist = os.path.isfile(df_name)
        df.to_csv(**args)
        del cache, df
        gc.collect()
        cache = []
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
#tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
