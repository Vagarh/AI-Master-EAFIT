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