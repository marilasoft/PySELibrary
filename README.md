PySELibrary
===========
## Una librería de SuitETECSA

PySELibrary fue creada para la [Comunidad Android de Cuba](https://jorgen.cubava.cu/), para facilitar el desarrollo de
aplicaciones Python que interactúen con el [Portal de Usuario](https://www.portal.nauta.cu/)
y el [Portal Cautivo](https://secure.etecsa.net:8443/) de nauta; así como el
[Portal Mi Cubacel](https://mi.cubacel.net), ahorrándoles tiempo, esfuerzos, neuronas y código a los desarrolladores.
 
PySELibrary pretende ser no solo multiplataforma, sino también multilenguaje, échale un vistazo a
[selibrary](https://github.com/marilasoft/selibrary/); la misma librería escrita en Java.
Esta, la versión en Python usa la librería [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/bs4/) para el
procesamiento de páginas web (`los portales de ETECSA`), mientras que la versión en Java usa
[Jsoup](https://jsoup.org/).

Por el momento PySELibrary a logrado implementar 10 funciones que representan el 100% de
las operaciones que permite realizar el [Portal de Usuario](https://www.portal.nauta.cu/) nauta en las cuentas no
asociadas a Nauta Hogar, estas son:
* Iniciar session.
* Obtener la información de la cuenta.
* Recargar la cuenta.
* Transferir saldo a otra cuenta nauta.
* Obtener el histórico de conexiones por meses.
* Obtener el histórico de recargas por meses.
* Obtener el histórico de transferencias por meses.
* Cambiar contraseña de la cuenta logeada.
* Cambiar contraseña de la cuenta de correo asociada.
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

La clase MCPortal es la encargada de interactuar con el [Portal Mi Cubacel](https://mi.cubacel.net),
y hasta el momento solo es capaz de logearse y obtener alguna informacion del usuario.
Acciones que realiza:
* Inicia session.
* Recupera la informacion siguiente:
    * Numero de telefono.
    * Saldo.
    * Fecha de expiracion del saldo.
    * Fecha en la que se utilizo el servicio `Adelanta Saldo` (si aun debe el saldo adelantado).
    * Saldo por pagar (si aun debe el saldo adelantado).
    * Numeros asociados al servicio 'Plan Amigo' (de existir estos).
* Recupera y compra productos (`paquetes`) (`la compra de paquetes no ha sido probada aun.`)

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

if __name__ == '__main__':
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

### Iniciando session con MCPortal

```python
from PySELibrary import MCPortal

if __name__ == '__main__':
    mc_portal = MCPortal()
    # Iniciando session y mostrando informacion de cuenta por pantalla
    mc_portal.login("55555555", "password")
    print(mc_portal.credit)
    print(mc_portal.phone_number)
    print(mc_portal.expire)
    print(mc_portal.date)
    print(mc_portal.payable_balance)
    print(mc_portal.phone_number_one)
    print(mc_portal.phone_number_two)
    print(mc_portal.phone_number_tree)
    # Saber si la tarifa por consumo esta activa (True o False)
    active_bonus_services = mc_portal.active_bonus_services
    # recuperando productos e intentando comprar el primero de la lista
    products = mc_portal.get_products(mc_portal.cookies)
    product = products[0]
    print(product.title)
    print(product.description)
    print(product.price)
    print(product.actions["mostInfo"])
    print(product.actions["buy"])
    mc_portal.buy(product.actions['buy'], mc_portal.cookies)
    print(mc_portal.status["status"].upper() + ": " + mc_portal.status["msg"])
    # Cambiando el estado de la tarifa por consumo
    mc_portal.change_bonus_services(active_bonus_services, mc_portal.url_CMPortal["changeBonusServices"],
                                    mc_portal.cookies)

```

## Dependencias
    python 3.6
    beautifulsoup4-4.6.3
