PySELibrary
===========
## Una librería de SuitETECSA

PySELibrary fue creada para la [Comunidad Android de Cuba](https://jorgen.cubava.cu/), para facilitar el desarrollo de
aplicaciones Python que interactúen con el [Portal de Usuario](https://www.portal.nauta.cu/)
y el [Portal Cautivo](https://secure.etecsa.net:8443/) de nauta; así como el
[Portal Mi Cubacel](https://mi.cubacel.net), ahorrándoles tiempo, esfuerzos, neuronas y código a los desarrolladores.
 
PySELibrary pretende ser no solo multiplataforma, sino también multilenguaje, échale un vistazo a
[SELibrary](https://github.com/marilasoft/selibrary/); la misma librería escrita en Java.
Esta, la versión en Python usa la librería [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/bs4/) para el
procesamiento de páginas web (`los portales de ETECSA`), mientras que la versión en Java usa
[Jsoup](https://jsoup.org/).

Por el momento PySELibrary a logrado implementar 8 funciones que representan el 100% de
las operaciones que permite realizar el [Portal de Usuario](https://www.portal.nauta.cu/) nauta en las cuentas no
asociadas a Nauta Hogar, estas son:
* Iniciar session.
* Obtener la información de la cuenta.
* Recargar la cuenta.
* Transferir saldo a otra cuenta nauta.
* Obtener el histórico de conexiones por meses.
* Obtener el histórico de recargas por meses.
* Obtener el histórico de transferencias por meses.
* Cerrar session.

Aún falta por implementar:
* Pagar servicio de Nauta Hogar (`en cuentas asociadas a este servicio`).

Mientras que la clase CaptivePortal, la encargada de interactuar con el 
[Portal Cautivo](https://secure.etecsa.net:8443/) de nauta, provee las siguientes funciones:
* Iniciar Session.
* Actualizar tiempo disponible.
* Cerrar session.
* Obtener informacion del usuario.
* Acceder a los terminos de uso.

## Ejemplos:

### Iniciando session con UserPortal

```python
from PySELibrary import UserPortal

user_portal = UserPortal()

# Cargamos la informacion necesaria para iniciar session
user_portal.pre_login()
cookies = user_portal.cookies

# Guardamos la imagen Captcha para poder ver el codigo
captcha_img = open("captcha_img.png", "wb")
captcha_img.write(user_portal.captcha_img)
captcha_img.close()

# Iniciamos session con la informacion que se nos pide
user_portal.login(input("Usuario: "),
                input("Contrasena: "),
                input("Codigo Captcha: "),
                cookies)

# Mostramos por pantalla informacion del usuario
print(user_portal.user_name)
print(user_portal.credit)
print(user_portal.block_date)
print(user_portal.delete_date)
print(user_portal.mail_account)

```

### Iniciando session con CaptivePortal

```python
from PySELibrary import CaptivePortal

captive_portal = CaptivePortal()

# Cargamos la informacion necesaria para iniciar session
captive_portal.pre_login()
cookies = captive_portal.cookies

# Iniciamos session con la informacion que se nos pide
captive_portal.login(input("Usuario: "),
                input("Contrasena: "),
                cookies)

# Mostramos por pantalla el tiempo disponible
print(captive_portal.update_available_time(cookies))

# cerrando session
captive_portal.logout(cookies)

```

## Dependencias
    python 3.6
    beautifulsoup4-4.6.3
