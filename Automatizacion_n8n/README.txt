# 🤖 Automated LinkedIn Content Creation with GPT-4 and Gemini for Scheduled Posts

## 📌 Descripción General
Este proyecto implementa un **agente automatizado en N8N** que conecta múltiples servicios para crear y publicar contenido en LinkedIn de manera totalmente automática.  
El flujo fue diseñado en el marco de la **Maestría en Ciencia de los Datos (EAFIT)** como parte de la evaluación sobre implementación de agentes con N8N.

---

## 🚀 Funcionalidad Principal
El agente realiza el siguiente proceso:

1. **Lectura de fuentes científicas**  
   - Utiliza un **RSS Feed de Arxiv (cs.AI)** para obtener los artículos más recientes.

2. **Generación de temas de contenido**  
   - Con **GPT-4** se crean ideas y títulos de publicación relevantes para LinkedIn.

3. **Creación de publicaciones**  
   - Expansión de los temas en **posts atractivos en español**.  
   - Generación de una **descripción visual** para acompañar cada post.

4. **Producción de imágenes**  
   - Con **Google Gemini** se crean imágenes tipo infografía, complementando el mensaje del post.

5. **Optimización SEO**  
   - Un agente adicional genera **hashtags relevantes y de tendencia** para aumentar el alcance.

6. **Publicación en LinkedIn**  
   - El contenido final (texto + imagen + hashtags) se publica automáticamente en una cuenta de LinkedIn.

7. **Almacenamiento y trazabilidad**  
   - Los datos procesados (autor, fuente, contenido) se registran en **Supabase**.

---

## 🛠️ Servicios y Herramientas Usadas
- **N8N** → Plataforma de orquestación del flujo.  
- **RSS Feed (Arxiv)** → Fuente de datos científicos.  
- **OpenAI GPT-4** → Generación de temas, textos y posts.  
- **Google Gemini (Imagen)** → Generación de imágenes complementarias.  
- **Supabase** → Registro de datos procesados.  
- **LinkedIn API** → Publicación automática de contenido.  

---

## 🔄 Flujo de Trabajo
```mermaid
flowchart TD
    A[RSS Feed Arxiv] --> B[Generación de temas GPT-4]
    B --> C[Creación de post + descripción de imagen]
    C --> D[Generación de hashtags SEO]
    C --> E[Generación de imagen con Gemini]
    D --> F[Merge contenido]
    E --> F
    F --> G[Publicación automática en LinkedIn]
    B --> H[Registro en Supabase]
