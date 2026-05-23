import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import requests

# ====================================
# LIMPIAR PREGUNTA
# ====================================
def limpiar_pregunta(mensaje):
    mensaje = mensaje.lower().strip()

    frases = [
        "cual es", "cuál es",
        "quien es", "quién es",
        "que es", "qué es",
        "dime", "busca", "buscar",
        "informacion de", "información de",
        "sobre", "por favor", "?"
    ]

    for frase in frases:
        mensaje = mensaje.replace(frase, "")

    return mensaje.strip()

# ====================================
# RESPUESTAS DIRECTAS
# ====================================
def respuestas_directas(pregunta):
    pregunta = pregunta.lower()

    if "capital de argentina" in pregunta:
        return "La capital de Argentina es Buenos Aires."

    if "capital de colombia" in pregunta:
        return "La capital de Colombia es Bogotá."

    if "capital de brasil" in pregunta:
        return "La capital de Brasil es Brasilia."

    if "capital de peru" in pregunta or "capital de perú" in pregunta:
        return "La capital de Perú es Lima."

    if "capital de chile" in pregunta:
        return "La capital de Chile es Santiago."

    return None

# ====================================
# BUSCAR EN WIKIPEDIA CON REQUESTS
# ====================================
def buscar_wikipedia(pregunta):
    directa = respuestas_directas(pregunta)

    if directa:
        return (
            "✅ Respuesta directa:\n\n"
            f"{directa}"
        )

    tema = limpiar_pregunta(pregunta)

    if tema == "":
        return "Escribe una pregunta clara para poder ayudarte."

    try:
        url_busqueda = "https://es.wikipedia.org/w/api.php"

        parametros_busqueda = {
            "action": "query",
            "list": "search",
            "srsearch": tema,
            "format": "json",
            "utf8": 1
        }

        respuesta = requests.get(
            url_busqueda,
            params=parametros_busqueda,
            timeout=10,
            headers={"User-Agent": "RickyAI/1.0"}
        )

        datos = respuesta.json()

        resultados = datos["query"]["search"]

        if len(resultados) == 0:
            return (
                "No encontré información relacionada con:\n\n"
                f"{tema}\n\n"
                "Intenta escribirlo de otra forma."
            )

        titulo = resultados[0]["title"]

        url_resumen = f"https://es.wikipedia.org/api/rest_v1/page/summary/{titulo}"

        respuesta_resumen = requests.get(
            url_resumen,
            timeout=10,
            headers={"User-Agent": "RickyAI/1.0"}
        )

        datos_resumen = respuesta_resumen.json()

        resumen = datos_resumen.get("extract", "No encontré un resumen disponible.")

        return (
            f"🔍 Resultado encontrado sobre: {titulo}\n\n"
            f"{resumen}\n\n"
            "✅ Información obtenida desde Wikipedia."
        )

    except Exception as e:
        return (
            "⚠️ No pude consultar Wikipedia en este momento.\n\n"
            "Posibles causas:\n"
            "- No hay internet.\n"
            "- Wikipedia no respondió.\n"
            "- La búsqueda no encontró datos claros.\n\n"
            f"Detalle técnico: {e}"
        )

# ====================================
# ENVIAR MENSAJE
# ====================================
def enviar():
    pregunta = entrada.get()

    if pregunta.strip() == "":
        messagebox.showwarning("Campo vacío", "Escribe una pregunta.")
        return

    respuesta = buscar_wikipedia(pregunta)

    area_chat.config(state="normal")

    area_chat.insert(tk.END, "👤 TÚ:\n" + pregunta + "\n\n")
    area_chat.insert(tk.END, "🧠 RICKY AI ASISTENTE:\n" + respuesta + "\n\n")
    area_chat.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")

    area_chat.config(state="disabled")
    area_chat.see(tk.END)

    entrada.delete(0, tk.END)
    entrada.focus()

# ====================================
# LIMPIAR CHAT
# ====================================
def limpiar_chat():
    area_chat.config(state="normal")
    area_chat.delete("1.0", tk.END)
    area_chat.config(state="disabled")
    entrada.focus()

# ====================================
# NUEVA PREGUNTA
# ====================================
def nueva_pregunta():
    entrada.delete(0, tk.END)
    entrada.focus()

# ====================================
# VENTANA PRINCIPAL
# ====================================
ventana = tk.Tk()
ventana.title("RICKY AI")
ventana.geometry("950x680")
ventana.configure(bg="#050816")
ventana.resizable(False, False)

# ====================================
# HEADER
# ====================================
header = tk.Frame(ventana, bg="#050816")
header.pack(pady=15)

# ====================================
# AVATAR
# ====================================
try:
    imagen = Image.open("avatar.png")
    imagen = imagen.resize((120, 120))
    avatar_img = ImageTk.PhotoImage(imagen)

    avatar = tk.Label(
        header,
        image=avatar_img,
        bg="#050816"
    )
except:
    avatar = tk.Label(
        header,
        text="🧠",
        font=("Arial", 70),
        fg="#00e5ff",
        bg="#050816"
    )

avatar.grid(row=0, column=0, rowspan=2, padx=20)

# ====================================
# TITULO
# ====================================
titulo = tk.Label(
    header,
    text="RICKY AI",
    font=("Arial", 32, "bold"),
    fg="#00e5ff",
    bg="#050816"
)
titulo.grid(row=0, column=1, sticky="w")

subtitulo = tk.Label(
    header,
    text="Tu asistente inteligente con RICKY IA",
    font=("Arial", 13),
    fg="white",
    bg="#050816"
)
subtitulo.grid(row=1, column=1, sticky="w")

# ====================================
# FRAME CHAT
# ====================================
frame_chat = tk.Frame(
    ventana,
    bg="#00e5ff",
    bd=2
)
frame_chat.pack(pady=10)

# ====================================
# AREA CHAT
# ====================================
area_chat = scrolledtext.ScrolledText(
    frame_chat,
    width=90,
    height=17,
    bg="#0b1023",
    fg="white",
    font=("Consolas", 11),
    insertbackground="white",
    wrap=tk.WORD
)
area_chat.pack(padx=3, pady=3)
area_chat.config(state="disabled")

# ====================================
# ENTRADA
# ====================================
entrada = tk.Entry(
    ventana,
    width=60,
    font=("Arial", 14),
    bg="#10182f",
    fg="white",
    insertbackground="white",
    justify="center"
)
entrada.pack(pady=10, ipady=8)
entrada.focus()

# ====================================
# BOTONES
# ====================================
frame_botones = tk.Frame(ventana, bg="#050816")
frame_botones.pack(pady=15)

btn_enviar = tk.Button(
    frame_botones,
    text="🚀 ENVIAR",
    width=18,
    bg="#00c853",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    command=enviar
)
btn_enviar.grid(row=0, column=0, padx=8)

btn_limpiar = tk.Button(
    frame_botones,
    text="🧹 LIMPIAR CHAT",
    width=18,
    bg="#0091ea",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    command=limpiar_chat
)
btn_limpiar.grid(row=0, column=1, padx=8)

btn_nueva = tk.Button(
    frame_botones,
    text="🔄 NUEVA PREGUNTA",
    width=20,
    bg="#651fff",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    command=nueva_pregunta
)
btn_nueva.grid(row=0, column=2, padx=8)

btn_salir = tk.Button(
    frame_botones,
    text="❌ SALIR",
    width=15,
    bg="#ff1744",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    command=ventana.destroy
)
btn_salir.grid(row=0, column=3, padx=8)

footer = tk.Label(
    ventana,
    text="Desarrollado por Ricky | Python + IA",
    bg="#050816",
    fg="#7d7d7d",
    font=("Arial", 10)
)
footer.pack(pady=10)

entrada.bind("<Return>", lambda event: enviar())

ventana.mainloop()