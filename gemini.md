# 🤖 Instrucciones para el Asistente de IA (Gemini)

Hola Gemini. Este archivo te proporciona el contexto esencial sobre este proyecto para que puedas ayudarme de la manera más efectiva posible. Por favor, lee y ten en cuenta esta información en tus respuestas.

## 1. Resumen del Proyecto

* **Nombre del Proyecto:** [Ej: "Plataforma de E-commerce 'Tienda Veloz'"]
* **Propósito Principal:** [Ej: "Crear una API RESTful para gestionar productos, pedidos y clientes de una tienda online."]
* **Objetivos Clave:**
    * Ofrecer un rendimiento rápido en las consultas de productos.
    * Garantizar la seguridad en el proceso de pago.
    * Ser fácilmente escalable para soportar un alto tráfico de usuarios.

## 2. Pila Tecnológica (Tech Stack)

* **Lenguaje Principal:** [Ej: TypeScript]
* **Backend:** [Ej: Node.js con NestJS]
* **Frontend:** [Ej: React con Next.js]
* **Base de Datos:** [Ej: PostgreSQL con Prisma ORM]
* **Testing:** [Ej: Jest para pruebas unitarias, Cypress para E2E]
* **Contenedores / DevOps:** [Ej: Docker, GitHub Actions para CI/CD]
* **Otros servicios clave:** [Ej: Stripe para pagos, S3 para almacenamiento de imágenes]

## 3. Estructura del Repositorio

La organización de las carpetas es la siguiente:

```
/
├── .github/              # Flujos de trabajo de CI/CD y plantillas de PR
├── dist/                 # Archivos de la compilación para producción
├── src/                  # Código fuente principal
│   ├── modules/          # Módulos de la aplicación (usuarios, productos, etc.)
│   │   ├── users/
│   │   │   ├── users.controller.ts
│   │   │   ├── users.service.ts
│   │   │   └── users.module.ts
│   ├── common/           # Lógica compartida (decoradores, guards, etc.)
│   └── main.ts           # Punto de entrada de la aplicación
├── test/                 # Pruebas (unitarias, integración, E2E)
├── prisma/               # Esquema y migraciones de la base de datos
├── .env.example          # Plantilla de variables de entorno
├── .eslintrc.js          # Configuración de ESLint
├── nest-cli.json         # Configuración de NestJS CLI
└── tsconfig.json         # Configuración de TypeScript
```
* **Lógica de negocio principal:** Se encuentra en los archivos `*.service.ts` dentro de `src/modules`.
* **Endpoints de la API:** Se definen en los archivos `*.controller.ts`.
* **Esquema de la base de datos:** Se gestiona en `prisma/schema.prisma`.

## 4. Comandos Clave y Flujo de Trabajo

* **Instalar dependencias:**
    ```bash
    npm install
    ```
* **Ejecutar en modo desarrollo (con auto-recarga):**
    ```bash
    npm run start:dev
    ```
* **Ejecutar todas las pruebas:**
    ```bash
    npm run test
    ```
* **Aplicar migraciones de la base de datos:**
    ```bash
    npx prisma migrate dev
    ```
* **Crear una build para producción:**
    ```bash
    npm run build
    ```

## 5. Estándares de Código y Convenciones

* **Estilo de Código:** Seguimos las reglas de `ESLint` con el plugin de `Prettier`. El formateo es automático al guardar.
* **Nomenclatura:**
    * Variables y funciones: `camelCase`.
    * Clases e Interfaces: `PascalCase`.
    * Nombres de archivo: `kebab-case.ts` (ej: `user-profile.service.ts`).
* **Mensajes de Commit:** Usamos **Conventional Commits**.
    * `feat(scope):` para nuevas características.
    * `fix(scope):` para corrección de errores.
    * `docs(scope):` para documentación.
    * Ejemplo: `feat(auth): implementar inicio de sesión con JWT`

## 6. Objetivos Actuales y Tareas Comunes

* **Objetivo Actual:** [Ej: "Implementar el módulo de gestión de carritos de compra."]
* **Tareas comunes para las que necesito ayuda:**
    * Generar pruebas unitarias para los servicios.
    * Optimizar consultas de Prisma.
    * Refactorizar código para mejorar la legibilidad y el rendimiento.
    * Documentar funciones complejas usando el formato JSDoc.
    * Sugerir mejoras de seguridad en los controladores.

## 7. Restricciones y "No Hacer"

* **No usar la librería `moment.js`**. Preferimos usar `date-fns` por su modularidad.
* **Evitar la lógica de negocio en los controladores**. Toda la lógica debe residir en los servicios.
* **No hacer `push` directamente a la rama `main` o `develop`**. Todo cambio debe pasar por un Pull Request.
* **No introducir dependencias nuevas sin consultarlo primero.**

---
Gracias por tu ayuda.

Esturctura del proyecto agente 

Claro, aquí tienes un resumen de cada archivo en el directorio src de tu proyecto Proyecto_Agente:

__init__.py: Este archivo está vacío. Su presencia le indica a Python que el directorio src debe ser tratado como un paquete, lo que permite importar los otros archivos (módulos) desde cualquier parte del proyecto.

agent.py: Este archivo contiene la lógica central del agente de inteligencia artificial.

Define la clase ProteinAnalysisAgent.
Utiliza la librería litellm para conectarse a un modelo de lenguaje de Gemini (LLM).
Tiene un método chat que recibe un contexto (un resumen del análisis de datos) y una pregunta del usuario.
Envía esta información al modelo de Gemini, con un prompt que le instruye para que actúe como un experto en biología molecular, y devuelve la respuesta generada por la IA.
app.py: Es la aplicación web principal construida con Streamlit. Se encarga de la interfaz de usuario y de orquestar todo el proceso.

Crea la interfaz donde puedes cargar un archivo, introducir tu API key y una dirección de correo.
Gestiona el flujo: Carga el dataset, valida que tenga las columnas necesarias, y si todo es correcto, activa el chat.
Implementa una interfaz de chat para que puedas hacerle preguntas al ProteinAnalysisAgent.
Muestra los resultados de un Análisis Exploratorio de Datos (EDA) básico en una pestaña separada.
Permite generar y enviar un reporte por correo electrónico.
eda.py: Contiene una función de validación simple.

La función validate_eda comprueba si el archivo cargado contiene un conjunto mínimo de columnas requeridas (seq, sst3, sst8, etc.) para asegurar que el análisis se puede realizar correctamente.
io_utils.py: Proporciona utilidades para la entrada/salida de datos.

La función read_any está diseñada para leer de forma flexible diferentes tipos de archivos (CSV, Excel). Es inteligente porque intenta detectar automáticamente el separador en los archivos CSV, lo que evita errores de lectura.
mail.py: Gestiona el envío de correos electrónicos.

La función send_email utiliza las credenciales de un servidor SMTP (host, usuario, contraseña) guardadas en variables de entorno para enviar los resultados del análisis a la dirección de correo que especifiques.
report.py: Se encarga de generar el reporte final.

La función generate_report crea un resumen en formato de texto con los resultados clave del análisis, como las dimensiones del dataset y si la validación (EDA) fue exitosa. Este texto es lo que se descarga o se envía por correo.
En resumen, tu proyecto es una aplicación web interactiva que permite a un usuario cargar datos de proteínas, realizar una validación básica y luego conversar con un agente de IA para obtener análisis e insights sobre esos datos.