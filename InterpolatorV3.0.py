#!/usr/bin/env python
# coding: utf-8

# In[4]:


#Load packages  
import greenlet
import pandas as pd 
import numpy as np
from scipy.interpolate import interp1d
import webbrowser
import tkinter as tk 
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename 
import ctypes

def interpolator(filepath, interpolation_type):
    global output_df
    #read test data for interpolation
    data_path = filepath 
    df =pd.read_csv(data_path, header=None) 
    df.columns=['time','temp']
    
    #perform interpolation
    x_known = np.array(df["time"])
    y_known = np.array(df["temp"])
    x_interp = np.linspace(min(x_known), max(x_known), 1000)
    
    #Choose interpolation method (linear, cubic, etc) 
    if interpolation_type.upper() == 'LINEAR':
        interpolation_method = 'linear'
    elif interpolation_type.upper() == 'CUBIC':
        interpolation_method = 'cubic'
    elif interpolation_type.upper() == 'QUADRATIC':
        interpolation_method = 'quadratic'
        
    #create an interpolation function 
    interp_func = interp1d(x_known, y_known, kind=interpolation_method, fill_value = 'extrapolate')
    y_interp = interp_func(x_interp)
    
    #send to output full: 
    output_x = [round(x,1) for x in x_interp]
    output_y = [round(y,1) for y in y_interp]
    output_df = pd.DataFrame({'x_interp':output_x, 'y_interp':output_y})
    return(output_df)

def export_results(): 
    output_filepath = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    output_df.to_csv(output_filepath)
    
def view_github(): 
    webbrowser.open("https://github.com/MDJonesBYU/Interpolation-App")
    
def show_instructions_popup():
    instructions_window = tk.Toplevel(root)
    instructions_window.title("How to Guide")
    
    #Add label with instructiosn 
    instructions_label = tk.Label(instructions_window, text = "Follow these instructions to interpolate your X,Y data:")
    instructions_label.pack(padx=10, pady=10, anchor ='w')
    
    #Add list of instructions 
    instructions_list = ttk.Treeview(instructions_window, columns=("steps"))
    instructions_list.column("#0", minwidth=0, width=1)
    instructions_list.column("#1", width=325)
    instructions_list.heading("#1", text="Steps")
    instructions_list.insert("", "end", values=("Step 1: Place Known X,Y data in an excel or CSV file",))
    instructions_list.insert("", "end", values=("Step 1A: X should be in the First column only",))
    instructions_list.insert("", "end", values=("Step 1B: Y should be in the Second column only",))
    instructions_list.insert("", "end", values=("Step 1C: Remove any headers -- Just data in both columns ",))
    instructions_list.insert("", "end", values=("Step 2: Save the file ",))
    instructions_list.insert("", "end", values=("Step 3: Click the 'Select File to Interpolate' button",))
    instructions_list.insert("", "end", values=("Step 4: Specify the output file name ",))
    instructions_list.insert("", "end", values=("",))
    instructions_list.insert("", "end", values=("",))
    instructions_list.insert("", "end", values=("Splash Attribution: #Cmglee, CC BY-SA 4.0",))
    instructions_list.pack(expand=True, padx=10, pady=10) 
    instructions_button = tk.Button(instructions_window, text="View Example", command=view_github)
    instructions_button.pack(pady=10)
    
root=tk.Tk()
root.iconbitmap("interp_icon.ico")
root.title("Interpolation Calculator")
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("interp_icon.ico")


canvas1 = tk.Canvas(root, width=300, height =350) 
canvas1.pack()

#Load the image using PhotoImage 
image = tk.PhotoImage(file="interpolator.png")
resized_image = image.subsample(7,7) 

#Create label to display the image 
image_label = tk.Label(root, image=resized_image)
canvas1.create_window(150,92, window=image_label)

def select_file():
    filename = askopenfilename()
    interpolation_method = interpolation_var.get()
    interpolator(filename, interpolation_method)
    
def thank_developer(): 
    webbrowser.open("https://www.paypal.com/donate/?hosted_button_id=QNDWWCN4LB88W")

interpolation_var = tk.StringVar() 
interpolation_options = ["Linear", "Cubic", "Quadratic"]
interpolation_option_menu = tk.OptionMenu(root, interpolation_var, *interpolation_options)
interpolation_var.set(interpolation_options[0])
canvas1.create_window(255, 235, window=interpolation_option_menu) 

button1 = tk.Button(text = "Select File to Interpolate", command=select_file, bg = 'brown', fg='white')
button2 = tk.Button(text = "How to Guide", command=show_instructions_popup, bg = 'brown', fg='white')
button3 = tk.Button(text = "Thank Developer", command=thank_developer, bg = 'brown', fg='white')
button4 = tk.Button(text = "Run Interpolation", command=export_results, bg = 'brown', fg='white')

canvas1.create_window(150, 200, window=button1)
canvas1.create_window(150, 270, window=button2)
canvas1.create_window(150, 305, window=button3)
canvas1.create_window(150, 235, window=button4)

developed_by_label = tk.Label(root, text = "Developed by Matt Jones, August 2023")
developed_by_label2 = tk.Label(root, text = "Contact: MJones@Envirolytica.com | Portfolio: Envirolytica.com/portfolio")
canvas1.create_window(150,340, window=developed_by_label)

root.mainloop()


# In[ ]:




