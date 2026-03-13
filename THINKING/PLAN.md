# PLAN DE DESARROLLO - Fisioterapeut App

## Fase 1: Entorno de Trabajo
1. **Configuración del entorno**:
   - Instalar Python 3.12.3 y entorno virtual (UV).
   - Configurar base de datos (ej. SQLite para pruebas, PostgreSQL para producción).
   - Instalar dependencias (Django/Flask para framework, Pillow para imágenes).

2. **Base de datos**:
   - Crear tablas: `Pacientes`, `Ejercicios`, `EjesDelCuerpo`, `Patologias`, `PlanTratamiento`.

## Fase 2: Funcionalidades Básicas
3. **Registro de pacientes**:
   - Formulario para capturar datos clínicos y dolor tipo EVA.
4. **Catálogo de ejercicios**:
   - Subir imágenes y descripciones por segmento corporal o patología.

## Fase 3: Planificación de Tratamientos
5. **Crear planes personalizados**:
   - Interfaz para seleccionar ejercicios por área afectada.
6. **Lógica de niveles**:
   - Sistema que bloquea ejercicios hasta que se cumpla una EVA <6.

## Fase 4: Interfaz y UX
7. **Frontend**:
   - Diseño simple para navegación por segmentos y ejercicios.
8. **Backend**:
   - API REST para gestión de datos y planes.

## Fase 5: Imágenes y Recursos
8. **Integración de imágenes**:
   - Archivos estáticos en `/static/ejercicios/`.
9. **Atlas interactivo**:
   - Próximo objetivo: Mostrar imágenes anatómicas al seleccionar un segmento.

## Fase 6: Pruebas y Despliegue
9. **Pruebas unitarias**:
   - Validar que el sistema de niveles funcione correctamente.
10. **Despliegue**:
    - Usar Gunicorn + Nginx o Flask-Yacht para alto rendimiento.
