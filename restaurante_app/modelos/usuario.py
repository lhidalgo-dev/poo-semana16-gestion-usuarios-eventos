class Usuario:
    LONGITUD_MINIMA_CONTRASENA: int = 4
    LONGITUD_MINIMA_IDENTIFICACION: int = 3
    LONGITUD_MAXIMA_IDENTIFICACION: int = 13
    ROL_ADMINISTRADOR: str = "Administrador"
    ROLES_VALIDOS: tuple[str, ...] = ("Administrador", "Empleado", "Cliente")
    # Roles que el administrador puede registrar, actualizar y eliminar.
    ROLES_GESTIONABLES: tuple[str, ...] = ("Empleado", "Cliente")
    DESCRIPCIONES_ROL: dict[str, str] = {
        "Administrador": "Gestiona usuarios, productos y ventas.",
        "Empleado": "Atiende el local: productos y ventas.",
        "Cliente": "Consume en el restaurante, sin gestion interna.",
    }

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        usuario: str,
        contrasena: str,
        rol: str = "Cliente",
    ) -> None:
        self.identificacion = identificacion
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    @staticmethod
    def normalizar_rol(valor: str) -> str:
        # Acepta cualquier combinacion de mayusculas y devuelve el rol oficial.
        texto = (valor or "").strip().lower()
        for rol in Usuario.ROLES_VALIDOS:
            if rol.lower() == texto:
                return rol
        return ""

    @staticmethod
    def describir_rol(valor: str) -> str:
        rol = Usuario.normalizar_rol(valor)
        if not rol:
            return "Seleccione un rol para ver sus alcances."
        return Usuario.DESCRIPCIONES_ROL[rol]

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La identificacion del usuario no puede estar vacia.")
        texto = valor.strip()
        if not texto.isdigit():
            raise ValueError("La identificacion solo puede contener numeros.")
        if not (
            self.LONGITUD_MINIMA_IDENTIFICACION
            <= len(texto)
            <= self.LONGITUD_MAXIMA_IDENTIFICACION
        ):
            raise ValueError(
                "La identificacion debe tener entre "
                f"{self.LONGITUD_MINIMA_IDENTIFICACION} y "
                f"{self.LONGITUD_MAXIMA_IDENTIFICACION} digitos."
            )
        self._identificacion = texto

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del usuario no puede estar vacio.")
        self._nombre = valor.strip()

    @property
    def usuario(self) -> str:
        return self._usuario

    @usuario.setter
    def usuario(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre de usuario no puede estar vacio.")
        texto = valor.strip().lower()
        if " " in texto:
            raise ValueError("El nombre de usuario no puede contener espacios.")
        # Se normaliza a minusculas para que el acceso no dependa de mayusculas.
        self._usuario = texto

    @property
    def contrasena(self) -> str:
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La contrasena del usuario no puede estar vacia.")
        valor_limpio = valor.strip()
        if len(valor_limpio) < self.LONGITUD_MINIMA_CONTRASENA:
            raise ValueError(
                f"La contrasena debe tener al menos {self.LONGITUD_MINIMA_CONTRASENA} caracteres."
            )
        self._contrasena = valor_limpio

    @property
    def rol(self) -> str:
        return self._rol

    @rol.setter
    def rol(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("Debe seleccionar un rol para el usuario.")
        rol_normalizado = Usuario.normalizar_rol(valor)
        if not rol_normalizado:
            opciones = ", ".join(self.ROLES_VALIDOS)
            raise ValueError(f"Rol no valido. Opciones: {opciones}")
        self._rol = rol_normalizado

    def es_administrador(self) -> bool:
        return self._rol == self.ROL_ADMINISTRADOR

    def es_gestionable(self) -> bool:
        # Solo los usuarios Empleado y Cliente se administran desde la interfaz.
        return self._rol in self.ROLES_GESTIONABLES

    def validar_credenciales(self, usuario: str, contrasena: str) -> bool:
        # El modelo conserva la comparacion de sus propios datos de acceso.
        return (
            self._usuario == usuario.strip().lower()
            and self._contrasena == contrasena.strip()
        )

    def convertir_a_diccionario(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    def __str__(self) -> str:
        return (
            f"Identificacion: {self.identificacion} | Nombre: {self.nombre} | "
            f"Usuario: {self.usuario} | Rol: {self.rol}"
        )
