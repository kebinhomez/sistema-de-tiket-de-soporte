import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def conectar():
    return sqlite3.connect("helpdesk.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario TEXT NOT NULL,
                        descripcion TEXT NOT NULL,
                        estado TEXT DEFAULT 'Abierto'
                    )''')
    conn.commit()
    conn.close()


def crear_ticket():
    usuario = entry_usuario.get()
    descripcion = entry_descripcion.get("1.0", tk.END).strip()

    if usuario == "" or descripcion == "":
        messagebox.showwarning("⚠️ Error", "Debe llenar todos los campos")
        return

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tickets (usuario, descripcion) VALUES (?, ?)", (usuario, descripcion))
    conn.commit()
    conn.close()
    messagebox.showinfo("✅ Éxito", "Ticket creado correctamente")
    entry_usuario.delete(0, tk.END)
    entry_descripcion.delete("1.0", tk.END)
    ver_tickets()

def ver_tickets():
    for item in tree.get_children():
        tree.delete(item)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    conn.close()

    
    for i, t in enumerate(tickets):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", "end", values=t, tags=(tag,))

def actualizar_estado():
    try:
        item = tree.selection()[0]
        ticket_id = tree.item(item, "values")[0]
        nuevo_estado = combo_estado.get()

        if nuevo_estado == "":
            messagebox.showwarning("⚠️ Error", "Debe seleccionar un estado")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE tickets SET estado = ? WHERE id = ?", (nuevo_estado, ticket_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("🔄 Éxito", f"Estado del ticket {ticket_id} actualizado a {nuevo_estado}")
        ver_tickets()
    except:
        messagebox.showwarning("⚠️ Error", "Debe seleccionar un ticket")

def eliminar_ticket():
    try:
        item = tree.selection()[0]
        ticket_id = tree.item(item, "values")[0]

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("🗑️ Eliminado", f"Ticket {ticket_id} eliminado")
        ver_tickets()
    except:
        messagebox.showwarning("⚠️ Error", "Debe seleccionar un ticket")


crear_tabla()

root = tk.Tk()
root.title("🎫 Mini HelpDesk")
root.geometry("800x400")


frame1 = tk.Frame(root, padx=10, pady=10)
frame1.pack(fill="x")

tk.Label(frame1, text="Usuario:").grid(row=0, column=0, sticky="w")
entry_usuario = tk.Entry(frame1, width=56)
entry_usuario.grid(row=0, column=1, padx=5)

tk.Label(frame1, text="Descripción:").grid(row=1, column=0, sticky="nw")
entry_descripcion = tk.Text(frame1, width=42, height=3)
entry_descripcion.grid(row=1, column=1, padx=5)

btn_crear = tk.Button(frame1, text="➕ Crear Ticket", command=crear_ticket)
btn_crear.grid(row=2, column=1, sticky="e", pady=5)


frame2 = tk.Frame(root, padx=10, pady=10)
frame2.pack(fill="both", expand=True)

columns = ("ID", "Usuario", "Descripción", "Estado")
tree = ttk.Treeview(frame2, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    ancho = 100 if col in ["ID", "Usuario", "Estado"] else 250
    tree.column(col, width=ancho, anchor="center")  # centrado

tree.pack(fill="both", expand=True)


style = ttk.Style()
style.configure("Treeview", rowheight=25, font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))


tree.tag_configure("oddrow", background="white")
tree.tag_configure("evenrow", background="#ffffff")


frame3 = tk.Frame(root, padx=10, pady=10)
frame3.pack(fill="x")

tk.Label(frame3, text="Nuevo Estado:").grid(row=0, column=0, padx=5)
combo_estado = ttk.Combobox(frame3, values=["Abierto", "En proceso", "Cerrado"], width=15)
combo_estado.grid(row=0, column=1, padx=5)

btn_estado = tk.Button(frame3, text="🔄 Cambiar Estado", command=actualizar_estado)
btn_estado.grid(row=0, column=2, padx=5)

btn_eliminar = tk.Button(frame3, text="🗑️ Eliminar Ticket", command=eliminar_ticket)
btn_eliminar.grid(row=0, column=3, padx=5)


ver_tickets()

root.mainloop()