# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 22:11:11 2024

@author: FernandaAvillo

Trabajo Final. 
Este proyecto nace a partir de una de las tareas que realizo en mi trabajo,
valorizar stocks options.

"""
import numpy as np
from scipy.stats import norm
import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf

def black_scholes(S, K, T, r, sigma, option_type):
    """
    Calcula el precio de una opción utilizando el modelo de Black-Scholes.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        option_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        option_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    return option_price

def calculate_price():
    try:
        S = float(entry_S.get())
        K = float(entry_K.get())
        T = float(entry_T.get())
        r = float(entry_r.get())
        sigma = float(entry_sigma.get())
        option_type = option_var.get()

        if K == 0 or sigma == 0 or T == 0:
            messagebox.showerror("Error", "K, sigma, y T deben ser mayores que 0.")
            return

        price = black_scholes(S, K, T, r, sigma, option_type)
        messagebox.showinfo("Resultado", f"El precio de la opción {option_type} es: {price:.2f}")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

def calculate_volatility():
    try:
        symbol = entry_symbol.get()
        start_date = entry_start_date.get()
        end_date = entry_end_date.get()
        
        data = yf.download(symbol, start=start_date, end=end_date)
        
        if data.empty:
            messagebox.showerror("Error", "No se pudieron obtener datos para el símbolo proporcionado o las fechas son incorrectas.")
            return
        
        data['Log Return'] = np.log(data['Adj Close'] / data['Adj Close'].shift(1))
        volatility = data['Log Return'].std() * np.sqrt(252)  # 252 días de trading en un año
        
        messagebox.showinfo("Resultado", f"La volatilidad anualizada de {symbol} del {start_date} al {end_date} es: {volatility:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error: {e}")

# Crear la aplicación principal
app = tk.Tk()
app.title("Aplicación Financiera")

# Crear las pestañas
tab_control = ttk.Notebook(app)

# Pestaña 1: Valorización de opciones
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Valorización de Opciones")

# Pestaña 2: Cálculo de Volatilidad
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text="Cálculo de Volatilidad")

tab_control.pack(expand=1, fill='both')

# Contenido de la Pestaña 1
entry_S = tk.Entry(tab1)
entry_K = tk.Entry(tab1)
entry_T = tk.Entry(tab1)
entry_r = tk.Entry(tab1)
entry_sigma = tk.Entry(tab1)
option_var = tk.StringVar(value='call')

tk.Label(tab1, text="Precio de la acción (S):").grid(row=0, column=0)
tk.Label(tab1, text="Precio de ejercicio (K):").grid(row=1, column=0)
tk.Label(tab1, text="Tiempo hasta expiración (T, en años):").grid(row=2, column=0)
tk.Label(tab1, text="Tasa de interés libre de riesgo (r):").grid(row=3, column=0)
tk.Label(tab1, text="Volatilidad (σ):").grid(row=4, column=0)
tk.Label(tab1, text="Tipo de opción:").grid(row=5, column=0)

entry_S.grid(row=0, column=1)
entry_K.grid(row=1, column=1)
entry_T.grid(row=2, column=1)
entry_r.grid(row=3, column=1)
entry_sigma.grid(row=4, column=1)

tk.Radiobutton(tab1, text="Call", variable=option_var, value='call').grid(row=5, column=1, sticky='w')
tk.Radiobutton(tab1, text="Put", variable=option_var, value='put').grid(row=5, column=1, sticky='e')

tk.Button(tab1, text="Calcular", command=calculate_price).grid(row=6, column=0, columnspan=2)

# Contenido de la Pestaña 2
tk.Label(tab2, text="Símbolo de la acción:").grid(row=0, column=0)
entry_symbol = tk.Entry(tab2)
entry_symbol.grid(row=0, column=1)

tk.Label(tab2, text="Fecha de inicio (YYYY-MM-DD):").grid(row=1, column=0)
entry_start_date = tk.Entry(tab2)
entry_start_date.grid(row=1, column=1)

tk.Label(tab2, text="Fecha de término (YYYY-MM-DD):").grid(row=2, column=0)
entry_end_date = tk.Entry(tab2)
entry_end_date.grid(row=2, column=1)

tk.Button(tab2, text="Calcular Volatilidad", command=calculate_volatility).grid(row=3, column=0, columnspan=2)

app.mainloop()
