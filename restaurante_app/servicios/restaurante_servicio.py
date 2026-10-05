from datetime import date

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(self, archivo_servicio) -> None:
        self.archivo_servicio = archivo_servicio
        self.usuarios: list[Usuario] = []
        self.productos: list[Producto] = []
        self.ventas: list[Venta] = []
        self.cargar_datos()

    def cargar_datos(self) -> None:
        # Carga los datos persistidos en JSON y los convierte en objetos del dominio.
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        productos_json = self.archivo_servicio.leer_json("productos.json")
        ventas_json = self.archivo_servicio.leer_json("ventas.json")

        self.usuarios = []
        for datos in usuarios_json:
            try:
                usuario = Usuario(
                    datos.get("identificacion", ""),
                    datos.get("nombre", ""),
                    datos.get("usuario", ""),
                    datos.get("contrasena", ""),
                    datos.get("rol", "Cliente"),
                )
                self.usuarios.append(usuario)
            except ValueError as error:
                print(f"Se encontro un usuario con datos invalidos: {error}")

        self.productos = []
        for datos in productos_json:
            try:
                producto = Producto(
                    datos.get("codigo", ""),
                    datos.get("nombre", ""),
                    datos.get("precio", 0),
                    datos.get("categoria", ""),
                    datos.get("stock", 0),
                )
                self.productos.append(producto)
            except ValueError as error:
                print(f"Se encontro un producto con datos invalidos: {error}")

        # Semana 15: carga las ventas persistidas para reconstruir el historial.
        self.ventas = []
        for datos in ventas_json:
            try:
                venta = Venta(
                    datos.get("identificador", ""),
                    datos.get("usuario_identificacion", ""),
                    datos.get("producto_codigo", ""),
                    datos.get("fecha", ""),
                )
                self.ventas.append(venta)
            except ValueError as error:
                print(f"Se encontro una venta con datos invalidos: {error}")

    def validar_acceso(self, usuario: str, contrasena: str) -> Usuario | None:
        # Recorre los usuarios cargados y delega la comparacion a cada objeto.
        for usuario_registrado in self.usuarios:
            if usuario_registrado.validar_credenciales(usuario, contrasena):
                return usuario_registrado
        return None

    def listar_usuarios(self) -> list[Usuario]:
        # Entrega los usuarios cargados para que la interfaz los muestre.
        return self.usuarios.copy()

    def listar_productos(self) -> list[Producto]:
        # Entrega los productos cargados para que la interfaz los muestre.
        return self.productos.copy()

    def listar_ventas(self) -> list[Venta]:
        # Entrega las ventas cargadas para que la interfaz las muestre.
        return self.ventas.copy()

    def cantidad_usuarios(self) -> int:
        return len(self.usuarios)

    def cantidad_productos(self) -> int:
        return len(self.productos)

    def cantidad_ventas(self) -> int:
        return len(self.ventas)

    def buscar_producto_por_codigo(self, codigo: str) -> Producto | None:
        # Localiza un producto ya cargado a partir de su codigo.
        codigo_normalizado = Producto.normalizar_codigo(codigo)
        for producto in self.productos:
            if producto.codigo == codigo_normalizado:
                return producto
        return None

    def buscar_usuario_por_identificacion(self, identificacion: str) -> Usuario | None:
        # Localiza un usuario ya cargado a partir de su identificacion.
        identificacion_normalizada = identificacion.strip()
        for usuario in self.usuarios:
            if usuario.identificacion == identificacion_normalizada:
                return usuario
        return None

    def buscar_usuario_por_nombre_usuario(self, nombre_usuario: str) -> Usuario | None:
        # El nombre de usuario se guarda en minusculas, igual que en el modelo.
        usuario_normalizado = nombre_usuario.strip().lower()
        for usuario in self.usuarios:
            if usuario.usuario == usuario_normalizado:
                return usuario
        return None

    def guardar_productos(self) -> None:
        # Persiste el estado actual de productos en productos.json.
        datos = [producto.convertir_a_diccionario() for producto in self.productos]
        self.archivo_servicio.escribir_json("productos.json", datos)

    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int,
    ) -> Producto:
        # Valida los datos mediante el modelo antes de agregar el producto.
        nuevo_producto = Producto(codigo, nombre, precio, categoria, stock)

        if self.buscar_producto_por_codigo(nuevo_producto.codigo) is not None:
            raise ValueError("Ya existe un producto registrado con ese codigo.")

        self.productos.append(nuevo_producto)
        self.guardar_productos()
        return nuevo_producto

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int,
    ) -> Producto:
        # El codigo identifica al producto existente; el resto se actualiza.
        producto_actual = self.buscar_producto_por_codigo(codigo)

        if producto_actual is None:
            raise ValueError("No existe un producto registrado con ese codigo.")

        datos_validados = Producto(codigo, nombre, precio, categoria, stock)
        producto_actual.nombre = datos_validados.nombre
        producto_actual.precio = datos_validados.precio
        producto_actual.categoria = datos_validados.categoria
        producto_actual.stock = datos_validados.stock

        self.guardar_productos()
        return producto_actual

    def eliminar_producto(self, codigo: str) -> Producto:
        # Quita el producto de la lista en memoria y actualiza el archivo.
        producto_actual = self.buscar_producto_por_codigo(codigo)

        if producto_actual is None:
            raise ValueError("No existe un producto registrado con ese codigo.")

        self.productos.remove(producto_actual)
        self.guardar_productos()
        return producto_actual

    # -----------------------------------------------------------------
    # Semana 15: gestion de ventas (fundamentos de manejo de eventos).
    # El callback de la interfaz solo recolecta la seleccion del usuario;
    # toda la validacion y la persistencia de la venta ocurre aqui.
    # -----------------------------------------------------------------
    def guardar_ventas(self) -> None:
        # Persiste el estado actual de ventas en ventas.json.
        datos = [venta.convertir_a_diccionario() for venta in self.ventas]
        self.archivo_servicio.escribir_json("ventas.json", datos)

    def generar_identificador_venta(self) -> str:
        # Genera un identificador secuencial simple para la nueva venta.
        siguiente = len(self.ventas) + 1
        return f"V{siguiente:03d}"

    def registrar_venta(self, usuario_identificacion: str, producto_codigo: str) -> Venta:
        # Relaciona un usuario existente con un producto existente.
        if not usuario_identificacion or not usuario_identificacion.strip():
            raise ValueError("Debe seleccionar un usuario para registrar la venta.")
        if not producto_codigo or not producto_codigo.strip():
            raise ValueError("Debe seleccionar un producto para registrar la venta.")

        usuario_encontrado = self.buscar_usuario_por_identificacion(usuario_identificacion)
        if usuario_encontrado is None:
            raise ValueError("El usuario seleccionado no existe.")

        producto_encontrado = self.buscar_producto_por_codigo(producto_codigo)
        if producto_encontrado is None:
            raise ValueError("El producto seleccionado no existe.")

        nueva_venta = Venta(
            self.generar_identificador_venta(),
            usuario_encontrado.identificacion,
            producto_encontrado.codigo,
            date.today().isoformat(),
        )

        self.ventas.append(nueva_venta)
        self.guardar_ventas()
        return nueva_venta

    # -----------------------------------------------------------------
    # Semana 16: gestion de usuarios con roles.
    # Las reglas de acceso, las validaciones y la persistencia viven aqui;
    # los callbacks de la interfaz solo reaccionan a eventos y delegan.
    # -----------------------------------------------------------------
    def puede_gestionar_usuarios(self, solicitante: Usuario | None) -> bool:
        return solicitante is not None and solicitante.es_administrador()

    def exigir_administrador(self, solicitante: Usuario | None) -> None:
        if not self.puede_gestionar_usuarios(solicitante):
            raise ValueError("Solo el Administrador puede gestionar usuarios.")

    def guardar_usuarios(self) -> None:
        # Persiste el estado actual de usuarios en usuarios.json.
        datos = [usuario.convertir_a_diccionario() for usuario in self.usuarios]
        self.archivo_servicio.escribir_json("usuarios.json", datos)

    def verificar_usuario_unico(self, nombre_usuario: str, identificacion: str) -> None:
        # Ningun otro usuario puede compartir el mismo nombre de acceso.
        existente = self.buscar_usuario_por_nombre_usuario(nombre_usuario)
        if existente is not None and existente.identificacion != identificacion:
            raise ValueError("Ya existe un usuario con ese nombre de acceso.")

    def exigir_rol_gestionable(self, usuario: Usuario) -> None:
        if not usuario.es_gestionable():
            raise ValueError(
                "Las cuentas de Administrador no se gestionan desde esta pantalla."
            )

    def registrar_usuario(
        self,
        solicitante: Usuario,
        identificacion: str,
        nombre: str,
        usuario: str,
        contrasena: str,
        rol: str,
    ) -> Usuario:
        self.exigir_administrador(solicitante)

        # El modelo valida cada dato antes de aceptar el registro.
        nuevo_usuario = Usuario(identificacion, nombre, usuario, contrasena, rol)
        self.exigir_rol_gestionable(nuevo_usuario)

        if self.buscar_usuario_por_identificacion(nuevo_usuario.identificacion) is not None:
            raise ValueError("Ya existe un usuario registrado con esa identificacion.")
        self.verificar_usuario_unico(nuevo_usuario.usuario, nuevo_usuario.identificacion)

        self.usuarios.append(nuevo_usuario)
        self.guardar_usuarios()
        return nuevo_usuario

    def actualizar_usuario(
        self,
        solicitante: Usuario,
        identificacion: str,
        nombre: str,
        usuario: str,
        contrasena: str,
        rol: str,
    ) -> Usuario:
        self.exigir_administrador(solicitante)

        usuario_actual = self.buscar_usuario_por_identificacion(identificacion)
        if usuario_actual is None:
            raise ValueError("No existe un usuario registrado con esa identificacion.")
        self.exigir_rol_gestionable(usuario_actual)

        # Una contrasena vacia conserva la actual: la tabla nunca la muestra.
        contrasena_final = contrasena if contrasena and contrasena.strip() else usuario_actual.contrasena
        datos_validados = Usuario(identificacion, nombre, usuario, contrasena_final, rol)
        self.exigir_rol_gestionable(datos_validados)
        self.verificar_usuario_unico(datos_validados.usuario, usuario_actual.identificacion)

        usuario_actual.nombre = datos_validados.nombre
        usuario_actual.usuario = datos_validados.usuario
        usuario_actual.contrasena = datos_validados.contrasena
        usuario_actual.rol = datos_validados.rol

        self.guardar_usuarios()
        return usuario_actual

    def validar_eliminacion_usuario(self, solicitante: Usuario, identificacion: str) -> Usuario:
        # Permite a la interfaz pedir confirmacion solo cuando la baja es posible.
        self.exigir_administrador(solicitante)

        usuario_actual = self.buscar_usuario_por_identificacion(identificacion)
        if usuario_actual is None:
            raise ValueError("No existe un usuario registrado con esa identificacion.")
        if usuario_actual.identificacion == solicitante.identificacion:
            raise ValueError("No puede eliminar la cuenta con la que inicio sesion.")
        self.exigir_rol_gestionable(usuario_actual)
        return usuario_actual

    def eliminar_usuario(self, solicitante: Usuario, identificacion: str) -> Usuario:
        usuario_actual = self.validar_eliminacion_usuario(solicitante, identificacion)

        self.usuarios.remove(usuario_actual)
        self.guardar_usuarios()
        return usuario_actual
