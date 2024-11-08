# Sesiones con Flask y Flask-Session
En esta etapa del proyecto se aplico la autenticación simple con sesiones para usuarios que permite a los usuarios iniciar y cerrar sesión en la API, asi como un sistema de registro de usuarios y el uso de cookies, empleando metodos de seguridad como encriptar las cookies y almacenar contraseñas hasheadas.
### Usar session en Flask para almacenar el estado del usuario autenticado.
![imagen](https://github.com/user-attachments/assets/58775ecb-1ba1-4d37-9692-c2c21e2c63de)

### Implementar ruta para registrar nuevo usuario, se usara posteriormente para el login.
![imagen](https://github.com/user-attachments/assets/2fa77434-ef75-4d9f-adbf-68088677726c)
![imagen](https://github.com/user-attachments/assets/0bb7f836-dd50-4783-a28c-94a0ce2bd4f3)
![imagen](https://github.com/user-attachments/assets/d89fafcd-e1c2-4a9f-b653-ca39241cd5eb)


### Implementar rutas/endpoints para login y logout, donde se establecen sesiones utilizando cookies.
No se hace uso de set_cookie ya que session se ejecuta por encima de las cookies y las firma criptograficamente de tal forma que el usuario no puede leer el contenido de estas a menos que tenga la clave secreta usada (se guarda en las variables de entorno).
![imagen](https://github.com/user-attachments/assets/22f88533-1da8-488a-913c-b9f6b51cd254)
![imagen](https://github.com/user-attachments/assets/b4755ea1-e2c1-459c-84c7-9ad9dd66d1d3)


### Proteger ciertas rutas para que solo sean accesibles si el usuario está autenticado (verificar la sesión).
![imagen](https://github.com/user-attachments/assets/178e2573-b902-48b1-b3ad-81b153c51b7b)

## Ejecucion y pruebas
Empezamos registrandonos en la ruta localhost/register usando Postman:
![imagen](https://github.com/user-attachments/assets/0b711dc2-4458-478b-90ce-c17c52932a73)

Si intento registrarme de nuevo da error ya que solo permite registrarse si el usuario y el email no se repiten (pasa lo mismo si intento enviar datos incompletos).
![imagen](https://github.com/user-attachments/assets/ac87d4ff-fc03-4890-88e0-929a83156df7)

Una vez registrado puedo iniciar sesion en localhost/login enviando mi username y password.
![imagen](https://github.com/user-attachments/assets/bc2b43c6-fca6-48ed-ae63-c11cfdc881e9)

Si cualquiera de estos no coincide con los guardados en la base de datos entonces no podre iniciar sesion.
![imagen](https://github.com/user-attachments/assets/fe58b3a7-ceac-4cb8-89d3-0dc1864a54a1)

Una vez logeado puedo observar en la seccion de cookies, que mi sesion se encuentra encriptada gracias a flask session.
![imagen](https://github.com/user-attachments/assets/77e4743a-d814-481b-8dff-e6f599f7c2f2)

Si intento acceder a la ruta protegida localhost/protected puedo acceder ya que estoy logeado, ademas me devuelve mi nombre de usuario el cual obtiene directo de mis cookies encriptadas.
![imagen](https://github.com/user-attachments/assets/18cf6359-9ed7-4af0-9e37-28fe56fc675d)

Para cerrar sesion accedo a localhost/logout y con esto se borran los datos de mi sesion almacenados en la sesion de flask.
![imagen](https://github.com/user-attachments/assets/585e64e3-63d0-4d1e-80c9-94966b504d77)

Por ultimo si no estoy logeado no puedo acceder a localhost/protected con lo que confirmamos que funciona correctamente.
![imagen](https://github.com/user-attachments/assets/b909589e-b92f-46a5-aa8d-f7ce4c137f89)
