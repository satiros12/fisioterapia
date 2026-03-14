# Escenario de Uso (User Case) - Aplicación de Fisioterapia

## UC1: Definición del Plan de Tratamiento por el Fisioterapeuta

**Actor:** Fisioterapeuta  
**Precondición:** El fisioterapeuta ha iniciado sesión en el sistema.  
**Flujo:**

1. **Selección de la Patología**  
   - Desde el panel de control, el fisioterapeuta elige la patología que se quiere tratar (por ejemplo *Epicondilitis*).  

2. **Filtrado por Segmento Corporal y Zona**  
   - Selecciona el segmento anatómico relevante (ejemplo: **Hombro/Derecha**).  
   - El sistema muestra el segmento en un **Atlas Anatómico** con las áreas visibles.

3. **Selección de Ejercicios**  
   - System muestra todas las categorías de ejercicios disponibles (estiramientos, movilidad activa, fuerza) para la zona seleccionada.  
   - Cada ejercicio incluye su nombre, una breve descripción y una imagen de referencia.  

4. **Asignación de Levels (Niveles)**  
   - Para cada ejercicio, el fisioterapeuta puede asignar el nivel inicial (Nivel 1, Nivel 2, etc.) según el estado del paciente.  
   - Se pueden activar/desactivar niveles según la progresión previa del paciente.

5. **Creación de Plan**  
   - Con un botón **“Asignar al Paciente”**, el fisioterapeuta agrega los ejercicios seleccionados a la **Planilla de Tratamiento** del paciente.  
   - El plan queda registrado con:  
     - Nombre del ejercicio  
     - Nivel asignado  
     - Fecha de asignación  
     - Instrucciones de referencia  
     - Imagen de ejecución  

6. **Confirmación**  
   - El sistema muestra un mensaje de confirmación y lista los ejercicios asignados.  
   - El fisioterapeuta puede revisar o modificar el plan antes de enviarlo al paciente.

---

## UC2: Ejecución de Ejercicios por el Paciente

**Actor:** Paciente  
**Precondición:** El paciente ha recibido un plan de ejercicios asignado por el fisioterapeuta.  
**Flujo:**

1. **Acceso al Dashboard**  
   - El paciente ingresa al sitio y se dirige al **Panel Personal** donde aparecen sus ejercicios asignados.

2. **Selección de Ejercicio**  
   - En el panel, el paciente ve un árbol jerárquico: **Segmento → Subsegmento → Categoria → Nivel**.  
   - Elige una categoría (por ejemplo **Estiramientos – Nivel 1**).  

3. **Visualización de la Imagen de Referencia**  
   - El sistema muestra la **Imagen de referencia** del ejercicio.  
   - También se visualiza el atlas anatómico del segmento (por ejemplo, cervical) para contextualizar la zona a tratar.

4. **Registro de EVA**  
   - Antes de ejecutar el ejercicio, el paciente ingresa **un valor en la Escala Visual Analógica (EVA) de dolor** (0‑10).  
   - El sistema guarda este registro como “EVA anterior”.  

5. **Ejecución del Ejercicio**  
   - El paciente sigue la **Instrucción paso‑a‑paso** (texto breve y/o audio).  
   - Se pueden reproducir imágenes o videos de ejecución si están disponibles.

6. **Marca de Completitud**  
   - Al terminar, marca el **checkbox** del ejercicio como **“Completado”**.

7. **Registro de EVA posterior**  
   - Después de la ejecución, el paciente registra nuevamente el valor de EVA.  
   - El sistema guarda “EVA posterior” y permite comparar con el valor preliminar.

8. **Desbloqueo del Nivel Siguiente**  
   - Si **EVA ≤ 6** en todas las tareas de la fase actual, el sistema despliega automáticamente el **Nivel 2**.  
   - Si **EVA > 6** en alguna tarea, el sistema muestra un mensaje indicando que el progreso está bloqueado hasta que el dolor disminuya.  
   - El paciente puede repetir el ejercicio o seguir con el mismo nivel si lo desea.

9. **Registro de Progreso**  
   - Cada sesión queda guardada en el historial del paciente:  
     - Ejercicio  
     - EVA antes y después  
     - Fecha y hora  
     - Comentario opcional del paciente  
   - El fisioterapeuta, al revisar el historial, puede ver gráficos de evolución del dolor y ajustar el plan.

---

## UC3: Revisión del Historial por el Fisioterapeuta

**Actor:** Fisioterapeuta  
**Precondición:** El fisioterapeuta tiene acceso a un historial de sesiones del paciente.  
**Flujo:**

1. **Acceso al Historial del Paciente**  
   - En el panel de gestión del fisioterapeuta, selecciona el paciente.  

2. **Visualización de Informe de Progreso**  
   - Se muestra un gráfico **de evolución del dolor** con valores de EVA antes y después de cada sesión.  
   - Se indica el porcentaje de ejercicios completados y el nivel actual alcanzado.  

3. **Ajuste del Plan**  
   - El fisioterapeuta puede **dar de baja** ejercicios que ya no son apropiados o **asignar nuevos ejercicios** en niveles superiores según la tendencia de la EVA.  
   - Se puede modificar el plan sin necesidad de crear uno nuevo desde cero.

---

## Notas de Implementación

- **Interfaz:** Se utilizará Bootstrap 5 para garantizar responsividad y claridad visual.  
- **Imágenes:** Todas las imágenes de referencia y atlas serán almacenadas en la carpeta `static/` del proyecto y servidas con rutas estáticas.  
- **Persistencia:** Los datos se guardarán en una base SQLite (modo MVP) mediante SQLAlchemy (Flask).  
- **Flujo de Desbloqueo:** La lógica de desbloqueo será manejada en la capa backend con una regla simple: *solo avanzar si todas las EVA registradas ≤ 6*.  

Este escenario de uso sirve como guía para la arquitectura y la implementación de la parte funcional de la aplicación.