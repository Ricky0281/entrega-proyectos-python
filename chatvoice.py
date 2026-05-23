import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import requests
import threading
from urllib.parse import quote

# =========================
# CONFIGURAR VOZ
# =========================
engine = pyttsx3.init()
engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)

def hablar(texto):
    try:
        engine.say(texto)
        engine.runAndWait()
    except:
        pass

def hablar_en_hilo(texto):
    hilo = threading.Thread(target=hablar, args=(texto,))
    hilo.daemon = True
    hilo.start()

# =========================
# LIMPIAR PREGUNTA
# =========================
def limpiar_pregunta(mensaje):
    mensaje = mensaje.lower().strip()

    frases = [
        "quien es", "quién es",
        "que es", "qué es",
        "cual es", "cuál es",
        "dime", "busca", "buscar",
        "informacion de", "información de",
        "sobre", "por favor", "?"
    ]

    for frase in frases:
        mensaje = mensaje.replace(frase, "")

    return mensaje.strip()

# =========================
# RESPUESTAS DIRECTAS
# =========================
def respuestas_directas(pregunta):
    pregunta = pregunta.lower()

    if "capital del valle" in pregunta or "capital de valle" in pregunta:
        return "La capital del Valle del Cauca es Cali."

    if "capital de colombia" in pregunta:
        return "La capital de Colombia es Bogotá."

    if "capital de argentina" in pregunta:
        return "La capital de Argentina es Buenos Aires."

    return None

# =========================
# BUSCAR EN WIKIPEDIA
# =========================
def buscar_wikipedia(pregunta):
    directa = respuestas_directas(pregunta)

    if directa:
        return directa

    tema = limpiar_pregunta(pregunta)

    if tema == "":
        return "Escribe una pregunta clara para poder ayudarte."

    try:
        url_busqueda = "https://es.wikipedia.org/w/api.php"

        parametros = {
            "action": "query",
            "list": "search",
            "srsearch": tema,
            "format": "json",
            "utf8": 1
        }

        respuesta = requests.get(
            url_busqueda,
            params=parametros,
            timeout=10,
            headers={"User-Agent": "RickyAI/1.0"}
        )

        datos = respuesta.json()
        resultados = datos["query"]["search"]

        if len(resultados) == 0:
            return f"No encontré información sobre: {tema}"

        titulo = resultados[0]["title"]
        titulo_url = quote(titulo)

        url_resumen = f"https://es.wikipedia.org/api/rest_v1/page/summary/{titulo_url}"

        respuesta_resumen = requests.get(
            url_resumen,
            timeout=10,
            headers={"User-Agent": "RickyAI/1.0"}
        )

        datos_resumen = respuesta_resumen.json()
        resumen = datos_resumen.get("extract")

        if not resumen:
            return f"Encontré el tema {titulo}, pero no hay resumen disponible."

        return (
            f"Resultado encontrado sobre: {titulo}\n\n"
            f"{resumen}\n\n"
            "Información obtenida desde Wikipedia."
        )

    except Exception as e:
        return f"No pude consultar Wikipedia en este momento. Error: {e}"

# =========================
# MOSTRAR MENSAJE
# =========================
def mostrar_chat(pregunta, respuesta):
    area_chat.config(state="normal")

    area_chat.insert(tk.END, "👤 TÚ:\n" + pregunta + "\n\n")
    area_chat.insert(tk.END, "🧠 RICKY AI:\n" + respuesta + "\n\n")
    area_chat.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")

    area_chat.config(state="disabled")
    area_chat.see(tk.END)

# =========================
# ENVIAR
# =========================
def enviar():
    pregunta = entrada.get().strip()

    if pregunta == "":
        messagebox.showwarning("Campo vacío", "Escribe o dicta una pregunta.")
        return

    estado_label.config(text="🔎 Buscando respuesta...")
    ventana.update()

    respuesta = buscar_wikipedia(pregunta)

    mostrar_chat(pregunta, respuesta)

    estado_label.config(text="🔊 Respondiendo con voz...")
    ventana.update()

    hablar_en_hilo(respuesta)

    estado_label.config(text="✅ Listo para otra pregunta")
    entrada.delete(0, tk.END)
    entrada.focus()

# =========================
# ESCUCHAR VOZ
# =========================
def escuchar():
    hilo = threading.Thread(target=escuchar_proceso)
    hilo.daemon = True
    hilo.start()

def escuchar_proceso():
    recognizer = sr.Recognizer()

    try:
        estado_label.config(text="🎤 Preparando micrófono...")
        ventana.update()

        with sr.Microphone() as source:
            estado_label.config(text="🎤 Escuchando... habla ahora")
            ventana.update()

            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=7)

        estado_label.config(text="🔎 Procesando voz...")
        ventana.update()

        texto = recognizer.recognize_google(audio, language="es-ES")

        entrada.delete(0, tk.END)
        entrada.insert(0, texto)

        estado_label.config(text="✅ Voz reconocida. Presiona ENVIAR.")
        ventana.update()

    except sr.WaitTimeoutError:
        estado_label.config(text="⏱️ No detecté voz. Intenta hablar más cerca.")

    except sr.UnknownValueError:
        estado_label.config(text="❌ Te escuché, pero no entendí la frase.")

    except sr.RequestError:
        estado_label.config(text="🌐 Error de internet o servicio de voz.")

    except Exception as e:
        estado_label.config(text="⚠️ Error: " + str(e))

# =========================
# LIMPIAR
# =========================
def limpiar_chat():
    area_chat.config(state="normal")
    area_chat.delete("1.0", tk.END)
    area_chat.config(state="disabled")
    estado_label.config(text="🎙️ Chat limpio. Listo para preguntar.")
    entrada.focus()

def nueva_pregunta():
    entrada.delete(0, tk.END)
    entrada.focus()
    estado_label.config(text="✍️ Escribe o dicta una nueva pregunta.")

# =========================
# VENTANA
# =========================
ventana = tk.Tk()
ventana.title("RICKY AI CHATVOICE")
ventana.geometry("950x690")
ventana.configure(bg="#050816")
ventana.resizable(False, False)

# =========================
# HEADER
# =========================
header = tk.Frame(ventana, bg="#050816")
header.pack(pady=12)

try:
    imagen = Image.open("avatar.png")
    imagen = imagen.resize((115, 115))
    avatar_img = ImageTk.PhotoImage(imagen)

    avatar = tk.Label(header, image=avatar_img, bg="#050816")
except:
    avatar = tk.Label(
        header,
        text="🧠",
        font=("Arial", 65),
        fg="#00e5ff",
        bg="#050816"
    )

avatar.grid(row=0, column=0, rowspan=2, padx=20)

titulo = tk.Label(
    header,
    text="RICKY AI CHATVOICE",
    font=("Arial", 30, "bold"),
    fg="#00e5ff",
    bg="#050816"
)
titulo.grid(row=0, column=1, sticky="w")

subtitulo = tk.Label(
    header,
    text="Asistente inteligente con voz y Wikipedia",
    font=("Arial", 13),
    fg="white",
    bg="#050816"
)
subtitulo.grid(row=1, column=1, sticky="w")

# =========================
# CHAT
# =========================
frame_chat = tk.Frame(ventana, bg="#00e5ff", bd=2)
frame_chat.pack(pady=8)

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

# =========================
# ESTADO
# =========================
estado_label = tk.Label(
    ventana,
    text="🎙️ Listo. Puedes escribir o usar el micrófono.",
    font=("Arial", 12),
    fg="#00e5ff",
    bg="#050816"
)
estado_label.pack(pady=5)

# =========================
# ENTRADA
# =========================
entrada = tk.Entry(
    ventana,
    width=60,
    font=("Arial", 14),
    bg="#10182f",
    fg="white",
    insertbackground="white",
    justify="center"
)
entrada.pack(pady=8, ipady=8)
entrada.focus()

# =========================
# BOTONES
# =========================
frame_botones = tk.Frame(ventana, bg="#050816")
frame_botones.pack(pady=12)

btn_voz = tk.Button(
    frame_botones,
    text="🎤 HABLAR",
    width=16,
    bg="#ff9800",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    command=escuchar
)
btn_voz.grid(row=0, column=0, padx=6)

btn_enviar = tk.Button(
    frame_botones,
    text="🚀 ENVIAR",
    width=16,
    bg="#00c853",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    command=enviar
)
btn_enviar.grid(row=0, column=1, padx=6)

btn_limpiar = tk.Button(
    frame_botones,
    text="🧹 LIMPIAR",
    width=16,
    bg="#0091ea",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    command=limpiar_chat
)
btn_limpiar.grid(row=0, column=2, padx=6)

btn_nueva = tk.Button(
    frame_botones,
    text="🔄 NUEVA",
    width=16,
    bg="#651fff",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    command=nueva_pregunta
)
btn_nueva.grid(row=0, column=3, padx=6)

btn_salir = tk.Button(
    frame_botones,
    text="❌ SALIR",
    width=16,
    bg="#ff1744",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    command=ventana.destroy
)
btn_salir.grid(row=0, column=4, padx=6)

footer = tk.Label(
    ventana,
    text="Desarrollado por Ricky | Python + Voz + Wikipedia API",
    bg="#050816",
    fg="#7d7d7d",
    font=("Arial", 10)
)
footer.pack(pady=5)

entrada.bind("<Return>", lambda event: enviar())

ventana.mainloop()