import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from modelos.producto import Producto
from modelos.usuario import Usuario


class MainView(tk.Frame):
    def __init__(self, master, restaurante_servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master, bg="#fff8f4")
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion

        self.contenido = None
        self.etiqueta_estado = None
        self.botones_menu = {}
        self.iconos = {}
        self.logo_encabezado = None

        self.producto_codigo_entry = None
        self.producto_nombre_entry = None
        self.producto_precio_entry = None
        self.producto_categoria_combo = None
        self.producto_stock_spin = None
        self.tabla_productos = None

        self.usuario_identificacion_entry = None
        self.usuario_nombre_entry = None
        self.usuario_acceso_entry = None
        self.usuario_contrasena_entry = None
        self.usuario_rol_combo = None
        self.usuario_rol_info = None
        self.tabla_usuarios = None

        self.usuario_venta_combo = None
        self.producto_venta_combo = None
        self.tabla_ventas = None
        self.opciones_usuarios_venta = {}
        self.opciones_productos_venta = {}

        self.definir_estilos()
        self.construir_interfaz()

    # -------------------------------------------------------------------
    # Carga de recursos graficos desde la carpeta assets/ del proyecto.
    # -------------------------------------------------------------------
    def cargar_icono(self, nombre_archivo):
        if nombre_archivo in self.iconos:
            return self.iconos[nombre_archivo]

        ruta_base = Path(__file__).resolve().parent.parent
        ruta_icono = ruta_base / "assets" / "icons" / nombre_archivo

        if not ruta_icono.exists():
            return None

        icono = tk.PhotoImage(file=str(ruta_icono))
        self.iconos[nombre_archivo] = icono
        return icono

    def cargar_logo_encabezado(self):
        ruta_base = Path(__file__).resolve().parent.parent
        ruta_logo = ruta_base / "assets" / "logo" / "icono.png"

        if not ruta_logo.exists():
            return None

        self.logo_encabezado = tk.PhotoImage(file=str(ruta_logo))
        return self.logo_encabezado

    def crear_boton_con_icono(self, contenedor, texto, comando, estilo, icono=None):
        imagen = self.cargar_icono(icono) if icono else None

        if imagen is not None:
            return ttk.Button(
                contenedor,
                text=texto,
                command=comando,
                style=estilo,
                image=imagen,
                compound="left",
            )
        return ttk.Button(contenedor, text=texto, command=comando, style=estilo)

    # -------------------------------------------------------------------
    # Colores y estilos reutilizables de toda la vista.
    # -------------------------------------------------------------------
    def definir_estilos(self):
        self.color_fondo = "#fff8f4"
        self.color_panel = "#ffffff"
        self.color_encabezado = "#5c2c1d"
        self.color_texto = "#4a3428"
        self.color_secundario = "#f6d9c9"
        self.color_resaltado = "#c0392b"

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "MenuApp.TButton",
            background=self.color_secundario,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("MenuApp.TButton", background=[("active", "#f0c4ac")])
        estilo.configure(
            "MenuActivo.TButton",
            background=self.color_resaltado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("MenuActivo.TButton", background=[("active", "#a5281b")])
        estilo.configure(
            "CerrarSesion.TButton",
            background="#8b1e1e",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("CerrarSesion.TButton", background=[("active", "#6f1717")])
        estilo.configure(
            "Accion.TButton",
            background=self.color_resaltado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Accion.TButton", background=[("active", "#a5281b")])
        estilo.configure(
            "Secundario.TButton",
            background="#7a6a63",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Secundario.TButton", background=[("active", "#5f5249")])
        estilo.configure(
            "Eliminar.TButton",
            background="#8b1e1e",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Eliminar.TButton", background=[("active", "#6f1717")])
        estilo.configure(
            "Treeview.Heading",
            background=self.color_secundario,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
        )
        estilo.configure("Treeview", rowheight=24, font=("Arial", 10))
        estilo.map(
            "Treeview",
            background=[("selected", self.color_resaltado)],
            foreground=[("selected", "#ffffff")],
        )

    # -------------------------------------------------------------------
    # Estructura principal: encabezado, navegacion, contenido y estado.
    # -------------------------------------------------------------------
    def construir_interfaz(self):
        encabezado = tk.Frame(self, bg=self.color_encabezado, padx=28, pady=14)
        encabezado.pack(fill="x")

        bloque_titulo = tk.Frame(encabezado, bg=self.color_encabezado)
        bloque_titulo.pack(anchor="w")

        logo = self.cargar_logo_encabezado()
        if logo is not None:
            tk.Label(bloque_titulo, image=logo, bg=self.color_encabezado).pack(
                side="left", padx=(0, 12)
            )

        bloque_texto = tk.Frame(bloque_titulo, bg=self.color_encabezado)
        bloque_texto.pack(side="left")

        tk.Label(
            bloque_texto,
            text="RESTAURANTE",
            bg=self.color_encabezado,
            fg="#ffffff",
            font=("Arial", 19, "bold"),
        ).pack(anchor="w")

        tk.Label(
            bloque_texto,
            text=f"Bienvenido, {self.usuario_actual.nombre} | Rol: {self.usuario_actual.rol}",
            bg=self.color_encabezado,
            fg="#f6d9c9",
            font=("Arial", 11),
        ).pack(anchor="w", pady=(4, 0))

        barra = tk.Frame(self, bg=self.color_secundario, padx=18, pady=10)
        barra.pack(fill="x")

        self.crear_boton_menu(barra, "Inicio", self.mostrar_inicio, "home.png")
        self.crear_boton_menu(barra, "Productos", self.mostrar_productos, "productos.png")
        self.crear_boton_menu(barra, "Usuarios", self.mostrar_usuarios, "users.png")
        self.crear_boton_menu(barra, "Ventas", self.mostrar_ventas, "ventas.png")

        self.crear_boton_con_icono(
            barra,
            "Cerrar sesion",
            self.cerrar_sesion,
            "CerrarSesion.TButton",
            "logout.png",
        ).pack(side="right")

        self.contenido = tk.Frame(self, bg=self.color_fondo, padx=28, pady=22)
        self.contenido.pack(fill="both", expand=True)

        self.crear_barra_estado()
        self.mostrar_inicio()

    def crear_boton_menu(self, contenedor, texto, comando, icono=None):
        boton = self.crear_boton_con_icono(contenedor, texto, comando, "MenuApp.TButton", icono)
        boton.pack(side="left", padx=(0, 8))
        self.botones_menu[texto] = boton

    def marcar_seccion(self, seccion):
        # Resalta visualmente la opcion de navegacion activa.
        for texto, boton in self.botones_menu.items():
            estilo = "MenuActivo.TButton" if texto == seccion else "MenuApp.TButton"
            boton.configure(style=estilo)

    def limpiar_contenido(self):
        assert self.contenido is not None

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def crear_barra_estado(self):
        barra_estado = tk.Frame(self, bg=self.color_secundario, padx=18, pady=8)
        barra_estado.pack(fill="x", side="bottom")

        self.etiqueta_estado = tk.Label(
            barra_estado,
            bg=self.color_secundario,
            fg=self.color_texto,
            font=("Arial", 10),
        )
        self.etiqueta_estado.pack(side="left")
        self.actualizar_barra_estado()

    def actualizar_barra_estado(self):
        assert self.etiqueta_estado is not None

        self.etiqueta_estado.config(
            text=(
                f"Sesion: {self.usuario_actual.usuario} ({self.usuario_actual.rol}) | "
                f"Productos: {self.restaurante_servicio.cantidad_productos()} | "
                f"Usuarios: {self.restaurante_servicio.cantidad_usuarios()} | "
                f"Ventas: {self.restaurante_servicio.cantidad_ventas()} | "
                "Datos JSON locales"
            )
        )

    # -------------------------------------------------------------------
    # Seccion Inicio: resumen general mediante tarjetas informativas.
    # -------------------------------------------------------------------
    def mostrar_inicio(self):
        self.marcar_seccion("Inicio")
        self.limpiar_contenido()
        self.actualizar_barra_estado()

        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text="Panel principal",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 18, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            self.contenido,
            text="Gestione productos, ventas y, si su rol es Administrador, "
            "los usuarios del restaurante desde las opciones superiores.",
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 12),
        ).pack(anchor="w", pady=(0, 22))

        resumen = tk.Frame(self.contenido, bg=self.color_fondo)
        resumen.pack(fill="x")

        self.crear_tarjeta_resumen(
            resumen, "Productos registrados", self.restaurante_servicio.cantidad_productos()
        )
        self.crear_tarjeta_resumen(
            resumen, "Usuarios registrados", self.restaurante_servicio.cantidad_usuarios()
        )
        self.crear_tarjeta_resumen(
            resumen, "Ventas registradas", self.restaurante_servicio.cantidad_ventas()
        )

    def crear_tarjeta_resumen(self, contenedor, titulo, valor):
        tarjeta = tk.Frame(contenedor, bg=self.color_panel, padx=18, pady=16)
        tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 14))

        tk.Label(
            tarjeta,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).pack(anchor="w")
        tk.Label(
            tarjeta,
            text=str(valor),
            bg=self.color_panel,
            fg=self.color_resaltado,
            font=("Arial", 24, "bold"),
        ).pack(anchor="w", pady=(8, 0))

    # -------------------------------------------------------------------
    # Seccion Usuarios (Semana 16): CRUD administrativo guiado por eventos.
    # Los botones usan command=; la tabla, el teclado y el combobox usan
    # bind(). Ningun callback valida ni persiste: todo se delega al servicio.
    # -------------------------------------------------------------------
    def mostrar_usuarios(self):
        self.marcar_seccion("Usuarios")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Gestion de usuarios")

        if not self.restaurante_servicio.puede_gestionar_usuarios(self.usuario_actual):
            self.mostrar_acceso_restringido()
            return

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            cuerpo,
            text="Datos del usuario",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.usuario_identificacion_entry = self.crear_campo(formulario, "Identificacion", 0)
        self.usuario_nombre_entry = self.crear_campo(formulario, "Nombre", 1)
        self.usuario_acceso_entry = self.crear_campo(formulario, "Usuario", 2)
        self.usuario_contrasena_entry = self.crear_campo(formulario, "Contrasena", 3)
        self.usuario_contrasena_entry.config(show="*")
        self.usuario_rol_combo = self.crear_campo_combo(
            formulario, "Rol", 4, Usuario.ROLES_GESTIONABLES
        )

        self.usuario_rol_info = tk.Label(
            formulario,
            text=Usuario.describir_rol(""),
            bg=self.color_panel,
            fg=self.color_resaltado,
            font=("Arial", 9, "bold"),
            wraplength=270,
            justify="left",
        )
        self.usuario_rol_info.grid(row=5, column=0, columnspan=2, sticky="w", pady=(2, 6))

        tk.Label(
            formulario,
            text="Enter registra | Esc limpia el formulario.\n"
            "Al actualizar, una contrasena vacia conserva la actual.",
            bg=self.color_panel,
            fg="#7a6a63",
            font=("Arial", 9),
            wraplength=270,
            justify="left",
        ).grid(row=6, column=0, columnspan=2, sticky="w")

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        acciones.grid_columnconfigure((0, 1), weight=1)

        botones = (
            ("Registrar", self.registrar_usuario, "Accion.TButton", "add.png"),
            ("Actualizar", self.actualizar_usuario, "Accion.TButton", "edit.png"),
            ("Eliminar", self.eliminar_usuario, "Eliminar.TButton", "delete.png"),
            ("Limpiar", self.limpiar_formulario_usuario, "Secundario.TButton", "clean.png"),
        )

        # command= asocia cada boton directamente con su callback.
        for posicion, (texto, comando, estilo, icono) in enumerate(botones):
            self.crear_boton_con_icono(acciones, texto, comando, estilo, icono).grid(
                row=posicion // 2,
                column=posicion % 2,
                sticky="ew",
                padx=(0 if posicion % 2 == 0 else 6, 6 if posicion % 2 == 0 else 0),
                pady=(0, 7),
            )

        listado = self.crear_panel_listado(cuerpo, "Usuarios registrados", usar_grid=True)
        self.tabla_usuarios = self.crear_tabla(
            listado,
            ("identificacion", "nombre", "usuario", "rol"),
            ("Identificacion", "Nombre", "Usuario", "Rol"),
            anchos=(110, 190, 110, 110),
        )
        self.tabla_usuarios.configure(selectmode="browse")

        self.configurar_eventos_usuarios()
        self.refrescar_usuarios()

    def mostrar_acceso_restringido(self):
        assert self.contenido is not None

        panel = tk.LabelFrame(
            self.contenido,
            text="Acceso restringido",
            bg=self.color_panel,
            fg=self.color_resaltado,
            font=("Arial", 10, "bold"),
            padx=18,
            pady=18,
        )
        panel.pack(fill="x")

        tk.Label(
            panel,
            text="La gestion de usuarios es exclusiva del rol Administrador.",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 12, "bold"),
        ).pack(anchor="w")
        tk.Label(
            panel,
            text=f"Su sesion actual tiene el rol {self.usuario_actual.rol}. "
            "Puede seguir usando Productos y Ventas.",
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10),
        ).pack(anchor="w", pady=(6, 0))

    def configurar_eventos_usuarios(self):
        assert self.tabla_usuarios is not None
        assert self.usuario_rol_combo is not None

        campos = self.campos_formulario_usuario()

        # Eventos virtuales de ttk asociados mediante bind().
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.al_seleccionar_usuario)
        self.usuario_rol_combo.bind("<<ComboboxSelected>>", self.al_cambiar_rol)

        # Atajos de teclado: Return registra y Escape limpia.
        for campo in campos:
            campo.bind("<Return>", self.al_presionar_enter)
        for campo in campos + [self.tabla_usuarios]:
            campo.bind("<Escape>", self.al_presionar_escape)

    def campos_formulario_usuario(self):
        return [
            self.usuario_identificacion_entry,
            self.usuario_nombre_entry,
            self.usuario_acceso_entry,
            self.usuario_contrasena_entry,
            self.usuario_rol_combo,
        ]

    # Callbacks de eventos: reciben el evento y reutilizan metodos existentes.
    def al_seleccionar_usuario(self, evento):
        assert self.tabla_usuarios is not None

        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        # El iid de cada fila es la identificacion; el objeto lo entrega el servicio.
        usuario = self.restaurante_servicio.buscar_usuario_por_identificacion(seleccion[0])
        if usuario is not None:
            self.cargar_usuario_en_formulario(usuario)

    def al_cambiar_rol(self, evento):
        assert self.usuario_rol_combo is not None
        assert self.usuario_rol_info is not None

        rol = self.usuario_rol_combo.get()
        self.usuario_rol_info.config(text=f"{rol}: {Usuario.describir_rol(rol)}")

    def al_presionar_enter(self, evento):
        self.registrar_usuario()

    def al_presionar_escape(self, evento):
        self.limpiar_formulario_usuario()

    def obtener_datos_usuario(self):
        assert self.usuario_identificacion_entry is not None
        assert self.usuario_nombre_entry is not None
        assert self.usuario_acceso_entry is not None
        assert self.usuario_contrasena_entry is not None
        assert self.usuario_rol_combo is not None

        return (
            self.usuario_identificacion_entry.get(),
            self.usuario_nombre_entry.get(),
            self.usuario_acceso_entry.get(),
            self.usuario_contrasena_entry.get(),
            self.usuario_rol_combo.get(),
        )

    def registrar_usuario(self):
        try:
            nuevo = self.restaurante_servicio.registrar_usuario(
                self.usuario_actual, *self.obtener_datos_usuario()
            )
            self.limpiar_formulario_usuario()
            self.refrescar_usuarios()
            messagebox.showinfo("Usuarios", f"Usuario {nuevo.usuario} registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def actualizar_usuario(self):
        try:
            actualizado = self.restaurante_servicio.actualizar_usuario(
                self.usuario_actual, *self.obtener_datos_usuario()
            )
            self.refrescar_usuarios()
            self.seleccionar_usuario_en_tabla(actualizado.identificacion)
            messagebox.showinfo("Usuarios", f"Usuario {actualizado.usuario} actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def eliminar_usuario(self):
        assert self.usuario_identificacion_entry is not None

        identificacion = self.usuario_identificacion_entry.get()
        try:
            usuario = self.restaurante_servicio.validar_eliminacion_usuario(
                self.usuario_actual, identificacion
            )
            if not messagebox.askyesno(
                "Confirmar eliminacion",
                f"Desea eliminar a {usuario.nombre} ({usuario.usuario})?",
            ):
                return
            self.restaurante_servicio.eliminar_usuario(self.usuario_actual, identificacion)
            self.limpiar_formulario_usuario()
            self.refrescar_usuarios()
            messagebox.showinfo("Usuarios", "Usuario eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def cargar_usuario_en_formulario(self, usuario):
        assert self.usuario_identificacion_entry is not None
        assert self.usuario_nombre_entry is not None
        assert self.usuario_acceso_entry is not None
        assert self.usuario_rol_combo is not None
        assert self.usuario_rol_info is not None

        self.vaciar_campos_usuario()
        self.usuario_identificacion_entry.insert(0, usuario.identificacion)
        self.usuario_nombre_entry.insert(0, usuario.nombre)
        self.usuario_acceso_entry.insert(0, usuario.usuario)
        self.usuario_rol_combo.set(usuario.rol)

        texto = f"{usuario.rol}: {Usuario.describir_rol(usuario.rol)}"
        if not usuario.es_gestionable():
            texto += " Cuenta protegida: solo consulta."
        self.usuario_rol_info.config(text=texto)

    def vaciar_campos_usuario(self):
        assert self.usuario_rol_combo is not None

        for entrada in self.campos_formulario_usuario()[:4]:
            assert entrada is not None
            entrada.delete(0, tk.END)
        self.usuario_rol_combo.set("")

    def limpiar_formulario_usuario(self):
        assert self.tabla_usuarios is not None
        assert self.usuario_identificacion_entry is not None
        assert self.usuario_rol_info is not None

        self.vaciar_campos_usuario()
        seleccion = self.tabla_usuarios.selection()
        if seleccion:
            self.tabla_usuarios.selection_remove(*seleccion)
        self.usuario_rol_info.config(text=Usuario.describir_rol(""))
        self.usuario_identificacion_entry.focus_set()

    def seleccionar_usuario_en_tabla(self, identificacion):
        assert self.tabla_usuarios is not None

        if self.tabla_usuarios.exists(identificacion):
            self.tabla_usuarios.selection_set(identificacion)
            self.tabla_usuarios.see(identificacion)

    def refrescar_usuarios(self):
        assert self.tabla_usuarios is not None

        self.limpiar_tabla(self.tabla_usuarios)
        for usuario in self.restaurante_servicio.listar_usuarios():
            # La contrasena nunca se muestra en la tabla.
            self.tabla_usuarios.insert(
                "",
                tk.END,
                iid=usuario.identificacion,
                values=(usuario.identificacion, usuario.nombre, usuario.usuario, usuario.rol),
            )

        self.actualizar_barra_estado()

    # -------------------------------------------------------------------
    # Seccion Productos: formulario + tabla + operaciones CRUD.
    # -------------------------------------------------------------------
    def mostrar_productos(self):
        self.marcar_seccion("Productos")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Gestion de productos")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            cuerpo,
            text="Datos del producto",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.producto_codigo_entry = self.crear_campo(formulario, "Codigo", 0)
        self.producto_nombre_entry = self.crear_campo(formulario, "Nombre", 1)
        self.producto_precio_entry = self.crear_campo(formulario, "Precio", 2)
        self.producto_categoria_combo = self.crear_campo_categoria(formulario, "Categoria", 3)
        self.producto_stock_spin = self.crear_campo_stock(formulario, "Stock", 4)

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        botones = (
            ("Registrar", self.registrar_producto, "Accion.TButton", "add.png"),
            ("Cargar / Consultar", self.cargar_producto_en_formulario, "Secundario.TButton", "search.png"),
            ("Actualizar", self.actualizar_producto, "Accion.TButton", "edit.png"),
            ("Eliminar", self.eliminar_producto, "Eliminar.TButton", "delete.png"),
            ("Limpiar", self.limpiar_formulario_producto, "Secundario.TButton", "clean.png"),
        )

        for texto, comando, estilo, icono in botones:
            self.crear_boton_con_icono(acciones, texto, comando, estilo, icono).pack(
                fill="x", pady=(0, 7)
            )

        listado = self.crear_panel_listado(cuerpo, "Productos registrados", usar_grid=True)
        self.tabla_productos = self.crear_tabla(
            listado,
            ("codigo", "nombre", "precio", "categoria", "stock"),
            ("Codigo", "Nombre", "Precio", "Categoria", "Stock"),
            anchos=(70, 170, 90, 130, 70),
        )
        self.refrescar_productos()

    def obtener_datos_producto(self):
        assert self.producto_codigo_entry is not None
        assert self.producto_nombre_entry is not None
        assert self.producto_precio_entry is not None
        assert self.producto_categoria_combo is not None
        assert self.producto_stock_spin is not None

        return (
            self.producto_codigo_entry.get(),
            self.producto_nombre_entry.get(),
            self.producto_precio_entry.get(),
            self.producto_categoria_combo.get(),
            self.producto_stock_spin.get(),
        )

    def registrar_producto(self):
        try:
            self.restaurante_servicio.registrar_producto(*self.obtener_datos_producto())
            self.limpiar_formulario_producto()
            self.refrescar_productos()
            messagebox.showinfo("Productos", "Producto registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Productos", str(error))

    def cargar_producto_en_formulario(self):
        assert self.producto_codigo_entry is not None

        producto = self.restaurante_servicio.buscar_producto_por_codigo(
            self.producto_codigo_entry.get()
        )
        if producto is None:
            messagebox.showerror("Productos", "No existe un producto con ese codigo.")
            return

        self.limpiar_formulario_producto()
        self.producto_codigo_entry.insert(0, producto.codigo)
        self.producto_nombre_entry.insert(0, producto.nombre)
        self.producto_precio_entry.insert(0, f"{producto.precio:.2f}")
        self.producto_categoria_combo.set(producto.categoria)
        self.producto_stock_spin.insert(0, str(producto.stock))

    def actualizar_producto(self):
        try:
            self.restaurante_servicio.actualizar_producto(*self.obtener_datos_producto())
            self.refrescar_productos()
            messagebox.showinfo("Productos", "Producto actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Productos", str(error))

    def eliminar_producto(self):
        assert self.producto_codigo_entry is not None

        try:
            self.restaurante_servicio.eliminar_producto(self.producto_codigo_entry.get())
            self.limpiar_formulario_producto()
            self.refrescar_productos()
            messagebox.showinfo("Productos", "Producto eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Productos", str(error))

    def limpiar_formulario_producto(self):
        for entrada in (
            self.producto_codigo_entry,
            self.producto_nombre_entry,
            self.producto_precio_entry,
            self.producto_stock_spin,
        ):
            assert entrada is not None
            entrada.delete(0, tk.END)

        assert self.producto_categoria_combo is not None
        self.producto_categoria_combo.set("")
        self.producto_stock_spin.insert(0, "0")

    def refrescar_productos(self):
        assert self.tabla_productos is not None

        self.limpiar_tabla(self.tabla_productos)
        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.codigo,
                    producto.nombre,
                    f"${producto.precio:.2f}",
                    producto.categoria,
                    producto.stock,
                ),
            )

        self.actualizar_barra_estado()

    # -------------------------------------------------------------------
    # Seccion Ventas: relaciona un usuario con un producto (Semana 15).
    # El boton usa command= para disparar el callback de venta, que
    # obtiene la seleccion de la interfaz y delega todo el registro,
    # la validacion y la persistencia a RestauranteServicio.
    # -------------------------------------------------------------------
    def mostrar_ventas(self):
        self.marcar_seccion("Ventas")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Gestion de ventas")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            cuerpo,
            text="Registrar venta",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.usuario_venta_combo = self.crear_campo_seleccion(
            formulario, "Usuario", 0, self.obtener_opciones_usuarios_venta()
        )
        self.producto_venta_combo = self.crear_campo_seleccion(
            formulario, "Producto", 1, self.obtener_opciones_productos_venta()
        )

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        # command= asocia el boton con el callback registrar_venta.
        self.crear_boton_con_icono(
            acciones, "Registrar venta", self.registrar_venta, "Accion.TButton", "add.png"
        ).pack(fill="x")

        listado = self.crear_panel_listado(cuerpo, "Ventas registradas", usar_grid=True)
        self.tabla_ventas = self.crear_tabla(
            listado,
            ("identificador", "usuario", "producto", "fecha"),
            ("Venta", "Usuario", "Producto", "Fecha"),
            anchos=(60, 190, 170, 85),
        )
        self.refrescar_ventas()

    def crear_campo_seleccion(self, contenedor, etiqueta, fila, opciones):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        combo = ttk.Combobox(
            contenedor,
            width=28,
            font=("Arial", 10),
            state="readonly",
            values=list(opciones.keys()),
        )
        combo.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return combo

    def obtener_opciones_usuarios_venta(self):
        # Relaciona cada texto visible del combo con la identificacion real del usuario.
        self.opciones_usuarios_venta = {
            f"{usuario.identificacion} - {usuario.nombre}": usuario.identificacion
            for usuario in self.restaurante_servicio.listar_usuarios()
        }
        return self.opciones_usuarios_venta

    def obtener_opciones_productos_venta(self):
        # Relaciona cada texto visible del combo con el codigo real del producto.
        self.opciones_productos_venta = {
            f"{producto.codigo} - {producto.nombre}": producto.codigo
            for producto in self.restaurante_servicio.listar_productos()
        }
        return self.opciones_productos_venta

    def registrar_venta(self):
        assert self.usuario_venta_combo is not None
        assert self.producto_venta_combo is not None

        usuario_identificacion = self.opciones_usuarios_venta.get(
            self.usuario_venta_combo.get(), ""
        )
        producto_codigo = self.opciones_productos_venta.get(
            self.producto_venta_combo.get(), ""
        )

        try:
            # El callback solo recolecta la seleccion; RestauranteServicio
            # valida la existencia del usuario y del producto y persiste la venta.
            self.restaurante_servicio.registrar_venta(usuario_identificacion, producto_codigo)
            self.limpiar_formulario_venta()
            self.refrescar_ventas()
            messagebox.showinfo("Ventas", "Venta registrada correctamente.")
        except ValueError as error:
            messagebox.showerror("Ventas", str(error))

    def limpiar_formulario_venta(self):
        assert self.usuario_venta_combo is not None
        assert self.producto_venta_combo is not None

        self.usuario_venta_combo.set("")
        self.producto_venta_combo.set("")

    def refrescar_ventas(self):
        assert self.tabla_ventas is not None

        self.limpiar_tabla(self.tabla_ventas)
        for venta in self.restaurante_servicio.listar_ventas():
            usuario = self.restaurante_servicio.buscar_usuario_por_identificacion(
                venta.usuario_identificacion
            )
            producto = self.restaurante_servicio.buscar_producto_por_codigo(
                venta.producto_codigo
            )
            texto_usuario = (
                venta.usuario_identificacion if usuario is None else f"{usuario.identificacion} - {usuario.nombre}"
            )
            texto_producto = (
                venta.producto_codigo if producto is None else f"{producto.codigo} - {producto.nombre}"
            )
            self.tabla_ventas.insert(
                "",
                tk.END,
                values=(venta.identificador, texto_usuario, texto_producto, venta.fecha),
            )

        # Actualiza la barra de estado para reflejar de inmediato la nueva venta.
        self.actualizar_barra_estado()

    # -------------------------------------------------------------------
    # Utilidades de interfaz compartidas por las secciones.
    # -------------------------------------------------------------------
    def crear_titulo_seccion(self, texto):
        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text=texto,
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 17, "bold"),
        ).pack(anchor="w", pady=(0, 14))

    def crear_campo(self, contenedor, etiqueta, fila):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        entrada = tk.Entry(contenedor, width=24, font=("Arial", 10))
        entrada.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return entrada

    def crear_campo_categoria(self, contenedor, etiqueta, fila):
        return self.crear_campo_combo(contenedor, etiqueta, fila, Producto.CATEGORIAS_VALIDAS)

    def crear_campo_combo(self, contenedor, etiqueta, fila, valores):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        combo = ttk.Combobox(
            contenedor,
            width=21,
            font=("Arial", 10),
            state="readonly",
            values=valores,
        )
        combo.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return combo

    def crear_campo_stock(self, contenedor, etiqueta, fila):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        spin = ttk.Spinbox(contenedor, from_=0, to=999, width=22, font=("Arial", 10))
        spin.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        spin.delete(0, tk.END)
        spin.insert(0, "0")
        return spin

    def crear_panel_listado(self, contenedor, titulo, usar_grid=False):
        listado = tk.LabelFrame(
            contenedor,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=12,
        )

        if usar_grid:
            listado.grid(row=0, column=1, sticky="nsew")
        else:
            listado.pack(fill="both", expand=True)

        return listado

    def crear_tabla(self, contenedor, columnas, encabezados, anchos=None):
        frame_tabla = tk.Frame(contenedor, bg=self.color_panel)
        frame_tabla.pack(fill="both", expand=True)

        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
        barra = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)

        anchos = anchos or [130] * len(columnas)
        for columna, encabezado, ancho in zip(columnas, encabezados, anchos):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=ancho, anchor="w")

        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabla

    def limpiar_tabla(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)

    def cerrar_sesion(self):
        self.al_cerrar_sesion()
