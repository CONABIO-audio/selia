# Selia

Web App to access, manage and upload data to Irekua database.


## Estructura a gran escala

- App base (selia-templates):
    - Contiene la definicion de las vista base
    - Templetes base
    - Componentes reutilizables (botones, modales, cartas, etc...)
    - Tags personalizados
    - Archivos estáticos que sean útiles en toda la plataforma
    - Widgets personalizados
    - Definición de estilo de formas

- Registro y manejo de usuarios (selia-registration):
    - Vistas de login/recuperacion de contraseña/invitación a selia/..

- Página principal (selia-home)

- Páginas de ayuda e información (selia-about)

- User home (selia-user)
    - Información de perfil
    - Resumen de actividad
    - Visualizar los datos de un usuario

- Colecciones (selia-collections)
    - Visualización de colecciones
    - Creación y edicion de metadatos

- Visualización de archivos (selia-visualizers)
    - Vista de visualización de items

- Anotación de archivos (selia-annotator)
    - Vistas de anotación de items

- Administración de colecciones (selia-managers)
    - Para que los administradores de tipo de colección (managers) puedan
    crear, editar, borrar colecciones, y asignar administradores.

- Mapas (selia-maps)
    - Define algunos tags de templete de django que facilita la inserción de
      mapas.

- Formas (selia-forms) [OBSOLETO] -> selia-templates
    - Contiene widgets personalizados
    - Definir el estilo de las formas


## selia-templates

#### Vistas base

1. Vista de detalle
2. Vista de listado
3. Vista de creacion
    3.1 Creación con forma
    3.2 Selección de opción
    3.3 Manager de creación
