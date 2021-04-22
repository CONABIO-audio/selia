# Selia

Web App to access, manage and upload data to Irekua database.

## Estructura a gran escala de Selia

Hemos pensado en dividir las componentes de Selia en distintas *apps* de Django
por tres motivos:

1. Mantener una estructura lógica y relativamente ordenada en el código.
2. Facilitar el reuso y uso independiente de cada aplicación, de modo que se
   puedan crear instancias únicamente con los componentes deseados.
3. Facilitar el reemplazo de cada *app* por otra aplicación personalizada.

Se deberá procurar mantener la mayor independencia posible entre las distintas
*apps*, salvo por *selia-templates*.

### Selia Templates

Este módulo deberá contener todos los elementos reutilizables de las páginas
públicas de Selia. En particular deberá definir tanto el estilo general de la
interfaz gráfica (UI) como el comportamiento y flujo general (UX).

Este módulo no deberá de exponer ningún endpoint y su propósito es proveer a
todos los otros módulos con los bloques básicos de construcción y así garantizar
un estilo y comportamiento homogéneo a lo largo de todo Selia.

**Templetes**
En este modulo se deberán de incluir todos los templetes de HTML que tengan que
ver con la disposición y estructura de las páginas de Selia, y también aquellos
que correspondan a los diferentes componentes de UI (encabezado, footer, panel,
etc...)

**Template Tag**
En algunas ocasiones tiene sentido definir tags personalizados para facilitar la
construcción de los templetes. En particular muchas componentes de UI simples
pueden convertirse en tags:

    {% button 'Enter' color='warning' %}

en vez de

    {% include 'selia_templates/button.html' with text='Enter' color='warning' %}

**Static Files**
En este modulo se deberá de colocar todos los archivos estáticos (js, css) que
se usen para complementar tanto el estilo como el comportamiento de los
componentes de UI.

**Widgets y Formas**
Si se utiliza un widget especial para los campos de fecha o de selección se
deberán de incluir en este módulo. En general este módulo deberá de definir el
estilo y comportamiento de las formas y sus campos.

**Views**
Muchas vistas tienden a cumplir una (o varias) de las siguientes funciones:
1) Crear un objeto
2) Detallar un objecto
3) Enlistar objetos
En este módulo se deberán de definir las vistas base sobre las que se construyen
todas las vistas de Selia.

### Selia Registration
Esta app de selia deberá proveer vistas para los usuarios puedan:

1) Hacer login
2) Pedir cambiar la contraseña en caso de olvido
3) Cambiar de contraseña
4) Registrarse
5) Mandar invitaciones a Selia

### Selia Home Page
Esta app deberá de proveer la página principal.

### Selia About
Esta *app* deberá de proveer páginas que contengan la información básica de
Selia.

### Selia User Home
En esta *app* el usuario deberá de poder ingresar a ver la información de su
perfil y de su actividad en la plataforma.

En particular deberá de poder enlistar y buscar sobre toda la información que ha
ingresado al sistema.

1) Ver perfil
2) Cambiar detalles de usuario
3) Enlistar:
    a) Las colecciones del usuario
    b) Los artículos cargados
    c) Los sitios declarados
    d) Los dispositivos registrados
    e) Los eventos de muestreo realizados
    f) etc...

### Selia Collections
En esta *app* los usuarios podrán explorar y administrar los datos cargados a
una colección. En particular deberá de exponer endpoints para:

1) Enlistar las colecciones abiertas y del usuario
2) Ver y Editar los metadatos de las colecciones
3) Enlistar y ver los usuarios de una colección
4) Enlistar y ver las licencias de una colección
5) Ver, Editar y Crear:
    a) Sitios de Colección
    b) Dispositivos de Colección
    c) Eventos de muestreo
    d) Despliegues de dispositivos
    e) Artículos


### Selia Upload
Esta *app* deberá de exponer la aplicación de upload de artículos.

### Selia Visualizers
Esta *app* deberá de exponer la aplicación de visualización de artículos.

### Selia Annotators
Esta *app* deberá de exponer la aplicación de anotado de artículos.

### Selia Managers
Esta *app* servirá para que los usuarios con permisos especiales administren
colecciones. En particular un *manager* deberá de poder:

1) Enlistar todas las colecciones que "maneja".
2) Crear nuevas colecciones.
3) Asignar administradores a colecciones.
4) Invitar nuevos usuarios a Selia
5) Ver y descargar estadísticas de la actividad en las colecciones que "maneja".

### Selia Maps
Esta *app* contendrá todas las aplicaciones de visualización con mapas.

### Otros
- Formas (selia-forms) [OBSOLETO] -> selia-templates
    - Contiene widgets personalizados
    - Definir el estilo de las formas
