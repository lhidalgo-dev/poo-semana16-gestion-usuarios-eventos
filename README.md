# restaurante_app — Semana 16

**Estudiante:** Leython Josue Hidalgo Valdez  
**Asignatura:** Programación Orientada a Objetos  
**Tema:** Manejo de eventos en Tkinter aplicado a la gestión de usuarios  

---

## Propósito de esta semana

Esta entrega continúa la evolución de `restaurante_app` a partir de la versión
de la Semana 15 (ventas con `command=` y recursos de `assets/`). El objetivo es
aplicar el **manejo de eventos** en una situación real del sistema: la
**gestión de usuarios**. Una selección en una tabla, una tecla o un cambio de
opción activan *callbacks* que coordinan la interfaz, mientras las reglas de
negocio y la persistencia permanecen en `RestauranteServicio`.

Se conservan el inicio de sesión, la navegación, la gestión de productos, el
registro de ventas y los recursos gráficos. La evolución se concentra en la
sección **Usuarios**, que pasa de ser una tabla de solo lectura a un CRUD
completo con roles.

## Evolución respecto a la Semana 15

| Archivo | Cambio realizado |
|---------|------------------|
| `modelos/usuario.py` | Nuevo atributo `rol` (Administrador, Empleado, Cliente) con validación, normalización y persistencia. Validación de identificación numérica y de nombre de usuario sin espacios. |
| `servicios/restaurante_servicio.py` | Nuevos métodos `registrar_usuario`, `actualizar_usuario`, `validar_eliminacion_usuario`, `eliminar_usuario`, `guardar_usuarios`, `puede_gestionar_usuarios` y búsqueda por nombre de acceso. Control de acceso y reglas de negocio centralizados. |
| `ui/main_view.py` | Sección **Usuarios** con formulario, `Treeview`, `Combobox` de rol y eventos `bind()`. Encabezado y barra de estado muestran el rol de la sesión. |
| `ui/login_view.py` | El atajo `<Return>` del acceso usa ahora un callback nombrado en lugar de una expresión `lambda`. |
| `datos/usuarios.json` | Cada usuario incluye el campo `rol`; se agregan un Empleado y un Cliente de demostración. |
| `main.py` | Ventana principal un poco más amplia para alojar el formulario y la tabla de usuarios. |

`productos.json`, `ventas.json`, `modelos/producto.py`, `modelos/venta.py` y
`servicios/archivo_servicio.py` se mantienen sin cambios.

## Estructura del proyecto

```
restaurante_app/
├── assets/
│   ├── icons/          (íconos de navegación y de acciones, PNG)
│   └── logo/           (logo.png y icono.png del sistema)
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

## Responsabilidad de cada capa

| Capa | Responsabilidad |
|------|------------------|
| `modelos/` | `Usuario` representa los datos de acceso y el rol, y valida cada atributo mediante `@property`. `Producto` y `Venta` no cambian. |
| `servicios/archivo_servicio.py` | Lee y escribe los JSON de `datos/`. Es la única clase que abre archivos. |
| `servicios/restaurante_servicio.py` | Convierte los JSON en objetos, decide quién puede gestionar usuarios, valida duplicados y protege cuentas. Persiste los cambios en `usuarios.json`. |
| `ui/` | `LoginView` y `MainView` responden a eventos, leen los campos y muestran el resultado. No leen ni escriben JSON y no contienen reglas de negocio. |
| `main.py` | Crea la ventana, el ícono del sistema, los servicios y controla el cambio entre vistas. |

## Gestión de usuarios

La sección **Usuarios** muestra un formulario (identificación, nombre, usuario,
contraseña y rol) junto a una tabla `Treeview` con las columnas
**Identificación, Nombre, Usuario y Rol**. La contraseña nunca se muestra en la
tabla ni se carga en el formulario al seleccionar una fila.

Operaciones disponibles:

- **Registrar:** crea un usuario nuevo. Rechaza identificaciones o nombres de
  acceso repetidos y datos inválidos.
- **Consultar:** al seleccionar una fila, sus datos se cargan en el formulario.
- **Actualizar:** modifica nombre, usuario, rol y, opcionalmente, la
  contraseña. Si el campo contraseña queda vacío, se conserva la actual.
- **Eliminar:** pide confirmación antes de borrar. No permite eliminar la cuenta
  con la que se inició sesión.
- **Limpiar:** deja el formulario y la selección en estado inicial.

### Roles

| Rol | Alcance en el sistema |
|-----|-----------------------|
| `Administrador` | Accede a la gestión de usuarios, además de productos y ventas. |
| `Empleado` | Usa productos y ventas. No accede a la gestión de usuarios. |
| `Cliente` | Usa productos y ventas. No accede a la gestión de usuarios. |

Reglas de acceso aplicadas:

- Solo el **Administrador** ve el formulario y la tabla de usuarios; un
  Empleado o un Cliente recibe un aviso de acceso restringido.
- El control no depende solo de la interfaz: `RestauranteServicio` verifica el
  rol del solicitante en cada operación de registro, actualización y baja.
- El administrador gestiona usuarios **Empleado** y **Cliente**. Las cuentas
  Administrador aparecen en la tabla, pero son de solo consulta y no se pueden
  editar ni eliminar desde esta pantalla. El `Combobox` de rol ofrece
  únicamente Empleado y Cliente.
- Si un `usuarios.json` antiguo no trae el campo `rol`, el usuario se carga
  como `Cliente` (el rol con menos alcance).

## Eventos implementados

| Componente | Evento | Mecanismo | Callback | Respuesta |
|------------|--------|-----------|----------|-----------|
| `Treeview` de usuarios | `<<TreeviewSelect>>` | `bind()` | `al_seleccionar_usuario(evento)` | Toma el identificador de la fila, pide el usuario a `RestauranteServicio` y carga el formulario. |
| Campos del formulario | `<Return>` | `bind()` | `al_presionar_enter(evento)` | Reutiliza `registrar_usuario()`, el mismo método del botón Registrar. |
| Campos del formulario y `Treeview` | `<Escape>` | `bind()` | `al_presionar_escape(evento)` | Reutiliza `limpiar_formulario_usuario()`: vacía campos y quita la selección. |
| `Combobox` de rol | `<<ComboboxSelected>>` | `bind()` | `al_cambiar_rol(evento)` | Muestra bajo el campo la descripción del rol elegido. |
| Botones Registrar, Actualizar, Eliminar, Limpiar | clic | `command=` | `registrar_usuario`, `actualizar_usuario`, `eliminar_usuario`, `limpiar_formulario_usuario` | Delegan la operación en `RestauranteServicio` y refrescan la tabla. |

### `command=` frente a `bind()`

- **`command=`** es la opción propia de los botones: asocia el clic con un
  método sin recibir información del evento. Se escribe sin paréntesis
  (`command=self.registrar_usuario`); con paréntesis la función se ejecutaría
  al construir la interfaz.
- **`bind()`** asocia cualquier evento (teclado o virtual de `ttk`) con un
  *callback* que recibe el objeto `evento`. Se usa donde `command=` no existe:
  seleccionar una fila, pulsar una tecla o cambiar la opción de un combobox.
- Un **callback** es la función que Tkinter invoca cuando ocurre el evento. Aquí
  solo recolecta datos de la interfaz y llama a un método existente; no repite
  lógica. Por eso `<Return>` ejecuta el mismo método que el botón Registrar.

## Flujo de eventos aplicado

```
Administrador abre "Usuarios"
        ↓
Selecciona una fila del Treeview
        ↓
<<TreeviewSelect>> → bind() → al_seleccionar_usuario(evento)
        ↓
Obtiene el identificador (iid) de la fila seleccionada
        ↓
RestauranteServicio.buscar_usuario_por_identificacion()
        ↓
Los datos se cargan en el formulario (sin contraseña)
        ↓
Actualizar / Eliminar / Limpiar  (command=)
        ↓
RestauranteServicio valida, aplica reglas y llama a guardar_usuarios()
        ↓
ArchivoServicio escribe usuarios.json
        ↓
MainView.refrescar_usuarios() actualiza el Treeview y la barra de estado
        ↓
Mensaje de confirmación o de error al usuario
```

## Persistencia

Los usuarios se guardan en `datos/usuarios.json` mediante
`RestauranteServicio.guardar_usuarios()`, que delega la escritura en
`ArchivoServicio`. Cada registro conserva `identificacion`, `nombre`,
`usuario`, `contrasena` y `rol`. Al volver a ejecutar la aplicación, los
usuarios y sus roles se recuperan desde ese archivo.

## Recursos gráficos (`assets/`)

- `assets/logo/logo.png`: logotipo de la pantalla de inicio de sesión.
- `assets/logo/icono.png`: ícono de la ventana y del encabezado principal.
- `assets/icons/`: íconos de la navegación y de los botones. En Usuarios se
  usan `add.png`, `edit.png`, `delete.png` y `clean.png`.

## Credenciales de demostración

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `leython` | `rest2026` | Administrador |
| `admin` | `admin123` | Administrador |
| `mtorres` | `mesera2026` | Empleado |
| `cmendoza` | `cliente2026` | Cliente |

> El acceso es una **simulación pedagógica**: las contraseñas se guardan en
> texto plano en el JSON solo con fines didácticos, lo cual no es una práctica
> segura en un sistema real.

## Requisitos

- Python 3.10 o superior
- Tkinter incluido en la instalación de Python (sin dependencias externas)

## Cómo ejecutar

```bash
cd restaurante_app
python main.py
```

En Windows, si `python` no está disponible en la terminal:

```bash
py main.py
```

## Pruebas realizadas

Se probó con Python 3.12 y Tkinter 8.6 siguiendo la comprobación mínima de la
guía de la Semana 16:

1. `main.py` inicia sin errores.
2. El inicio de sesión, la navegación, Productos y Ventas siguen funcionando.
3. El Administrador accede a la sección **Usuarios**.
4. Un Empleado y un Cliente ven un aviso de acceso restringido, y el servicio
   rechaza sus intentos de registrar, actualizar o eliminar usuarios.
5. Se registra un usuario Cliente y un usuario Empleado.
6. El usuario nuevo aparece en el `Treeview` con su rol.
7. Al seleccionar una fila, `<<TreeviewSelect>>` carga sus datos en el
   formulario; la contraseña queda vacía.
8. Al modificar un dato y pulsar **Actualizar**, el cambio se conserva.
9. **Eliminar** pide confirmación; si se cancela, el usuario permanece.
10. La cuenta con la que se inició sesión no se puede eliminar, y las cuentas
    Administrador están protegidas.
11. `Enter` registra el usuario mediante `<Return>`, y con datos inválidos
    muestra el error del servicio.
12. `Escape` limpia el formulario y la selección, tanto desde un campo como
    desde la tabla.
13. El `Combobox` de rol responde a `<<ComboboxSelected>>`.
14. Al cerrar y volver a ejecutar la aplicación, los usuarios se recuperan
    desde `usuarios.json`.
15. La interfaz mantiene distribución, estilos, íconos y logotipo coherentes.
16. Se verificaron además: identificación o nombre de acceso repetidos,
    identificación no numérica, contraseña corta, rol vacío o inválido, e
    intento de crear un Administrador desde el formulario. En todos los casos
    el servicio rechaza la operación con un mensaje claro.
