import streamlit as st
import math
import pandas as pd
import sympy as sp
# ====================
# Import libraries

# Fungsi untuk mengevaluasi f(x)
def eval_function(expr, x):
    try:
        return eval(expr, {"x": x, "math": math})
    except Exception as e:
        st.error(f"Error dalam evaluasi fungsi: {e}")
        return None

# Bisection Method
def bisection(a, b, tol, max_iter, fx):
    if eval_function(fx, a) * eval_function(fx, b) >= 0:
        return "Metode gagal: f(a) dan f(b) harus beda tanda.", None

    results = []
    for i in range(max_iter):
        x = (a + b) / 2
        fx_val = eval_function(fx, x)
        results.append([i + 1, f"{a:.6f}", f"{b:.6f}", f"{x:.6f}", f"{fx_val:.6f}"])

        if abs(fx_val) < tol or abs(b - a) < tol:
            return pd.DataFrame(results, columns=["Iterasi", "a", "b", "x", "f(x)"]), f"{x:.6f}"

        if eval_function(fx, a) * fx_val < 0:
            b = x
        else:
            a = x

    return "Akar tidak ditemukan dalam iterasi maksimum.", None

# Fixed Point Iteration
def fixed_point_iteration_auto(g_expression, x0, epsilon=1e-6, Nmaks=30):
    def g(x):
        return eval(g_expression, {"x": x, "math": math})

    results = []
    x_sebelumnya = x0
    for i in range(Nmaks):
        try:
            x_baru = g(x_sebelumnya)
        except Exception as e:
            return f"❌ Error: {e}", None

        error = abs(x_baru - x_sebelumnya)
        results.append([i + 1, f"{x_baru:.6f}", f"{error:.6f}"])

        if error < epsilon:
            return pd.DataFrame(results, columns=["Iterasi", "x", "|x_(r+1) - x_r|"]), x_baru

        x_sebelumnya = x_baru

    return "Lelaran divergen atau belum konvergen.", None


# Secant Method
def secant_method(x0, x1, tol=1e-6, max_iter=100, fx=""):
    results = []
    for i in range(max_iter):
        f0, f1 = eval_function(fx, x0), eval_function(fx, x1)
        if f1 - f0 == 0:
            return "Terjadi pembagian dengan nol.", None
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        results.append([i + 1, f"{x2:.6f}", f"{abs(x2 - x1):.6f}"])

        if abs(x2 - x1) < tol:
            return pd.DataFrame(results, columns=["Iterasi", "xr", "|xr - xr-1|"]), f"{x2:.6f}"
        x0, x1 = x1, x2
    return "Tidak konvergen dalam iterasi maksimum.", None

# Newton-Raphson
def newton_raphson(x0, epsilon=1e-6, max_iter=100, fx=""):
    def f_prime(x):
        delta = 1e-6
        return (eval_function(fx, x + delta) - eval_function(fx, x)) / delta

    results = []
    for i in range(max_iter):
        fx_val = eval_function(fx, x0)
        fpx = f_prime(x0)

        if fpx == 0:
            return "Turunan nol. Metode gagal.", None

        x1 = x0 - fx_val / fpx
        error = abs(x1 - x0)
        results.append([i + 1, f"{x0:.6f}", f"{error:.6f}"])

        if error < epsilon:
            return pd.DataFrame(results, columns=["Iterasi", "x_r", "|x_(r+1) - x_r|"]), f"{x1:.6f}"

        x0 = x1

    return "Tidak konvergen setelah iterasi maksimum.", None

# Regula Falsi
def regula_falsi(a, b, tol=1e-6, max_iter=100, fx=""):
    fa = eval_function(fx, a)
    fb = eval_function(fx, b)

    if fa * fb > 0:
        return "Fungsi tidak memiliki akar yang dijamin di interval tersebut.", None

    results = []
    for i in range(1, max_iter + 1):
        c = b - fb * (b - a) / (fb - fa)
        fc = eval_function(fx, c)
        lebar = abs(b - a)
        results.append([i, f"{a:.6f}", f"{fa:.6f}", f"{b:.6f}", f"{fb:.6f}", f"{c:.6f}", f"{fc:.6f}", f"{lebar:.6f}"])

        if abs(fc) < tol or lebar < tol:
            return pd.DataFrame(results, columns=["Iterasi", "a", "f(a)", "b", "f(b)", "c", "f(c)", "|b - a|"]), f"{c:.6f}"

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return "Metode tidak konvergen dalam iterasi maksimum.", None

# ====================
# Streamlit Interface
# ====================

st.title("Aplikasi Metode Numerik")

method = st.selectbox("Pilih Metode", ["Bisection", "Fixed Point Iteration", "Secant", "Newton-Raphson", "Regula Falsi"])

# Input fungsi sesuai metode
if method == "Fixed Point Iteration":
    gx = st.text_area("Masukkan ekspresi fungsi g(x)", "math.sqrt(math.exp(x)/5)")
else:
    fx = st.text_area("Masukkan ekspresi fungsi f(x)", "math.exp(x) - 5 * x**2")

# Pilihan metode dan input
if method == "Bisection":
    a = st.number_input("Masukkan a", value=0.0)
    b = st.number_input("Masukkan b", value=1.0)
    tol = st.number_input("Masukkan toleransi", value=1e-6, format="%.6f")
    max_iter = st.number_input("Masukkan jumlah iterasi maksimum", value=50, min_value=1)
    if st.button("Run Bisection"):
        results, root = bisection(a, b, tol, max_iter, fx)
        if isinstance(results, str):
            st.error(results)
        else:
            st.write("Tabel Iterasi:")
            st.table(results)
            st.success(f"Akar ditemukan: x = {root}")

elif method == "Fixed Point Iteration":
    x0 = st.number_input("Masukkan tebakan awal x₀", value=0.0)
    epsilon = st.number_input("Masukkan toleransi galat", value=1e-6, format="%.6f")
    Nmaks = st.number_input("Masukkan jumlah iterasi maksimum", value=30, min_value=1)
    if st.button("Run Fixed Point Iteration"):
        results, root = fixed_point_iteration_auto(gx, x0, epsilon, Nmaks)
        if isinstance(results, str):
            st.error(results)
        else:
            st.write("Tabel Iterasi:")
            st.table(results)
            st.success(f"Akar ditemukan: x ≈ {root:.6f}")

elif method == "Secant":
    x0 = st.number_input("Masukkan x₀", value=-1.0)
    x1 = st.number_input("Masukkan x₁", value=0.0)
    tol = st.number_input("Masukkan toleransi", value=1e-6, format="%.6f")
    max_iter = st.number_input("Masukkan jumlah iterasi maksimum", value=100, min_value=1)
    if st.button("Run Secant Method"):
        results, root = secant_method(x0, x1, tol, max_iter, fx)
        if isinstance(results, str):
            st.error(results)
        else:
            st.write("Tabel Iterasi:")
            st.table(results)
            st.success(f"Akar ditemukan: x = {root}")

elif method == "Newton-Raphson":
    x0 = st.number_input("Masukkan tebakan awal x₀", value=0.5)
    epsilon = st.number_input("Masukkan toleransi galat", value=1e-6, format="%.6f")
    max_iter = st.number_input("Masukkan jumlah iterasi maksimum", value=100, min_value=1)
    if st.button("Run Newton-Raphson"):
        results, root = newton_raphson(x0, epsilon, max_iter, fx)
        if isinstance(results, str):
            st.error(results)
        else:
            st.write("Tabel Iterasi:")
            st.table(results)
            st.success(f"Akar ditemukan: x = {root}")

elif method == "Regula Falsi":
    a = st.number_input("Masukkan a", value=0.0)
    b = st.number_input("Masukkan b", value=1.0)
    tol = st.number_input("Masukkan toleransi", value=1e-6, format="%.6f")
    max_iter = st.number_input("Masukkan jumlah iterasi maksimum", value=100, min_value=1)
    if st.button("Run Regula Falsi"):
        results, root = regula_falsi(a, b, tol, max_iter, fx)
        if isinstance(results, str):
            st.error(results)
        else:
            st.write("Tabel Iterasi:")
            st.table(results)
            st.success(f"Akar ditemukan: x ≈ {root}")
