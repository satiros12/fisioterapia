# IDEAS.md - Preguntas Pendientes

## Preguntas Pendientes por Resolver
- **Tecnología Base**: 
  - ¿Qué stack elegir entre Django/Flask/React para el frontend/backend? ¿Usar Vue para UI ligera?
- **Datos de Pruebas**: 
  - ¿Cómo estructurar `sample_patients.json` y `sample_exercises.json` para cubrir casos de uso reales?
  - ¿Cómo probar validaciones de EVA y progreso sin datos del mundo real?
- **Seguridad**: 
  - ¿Cómo proteger datos sensibles (historial clínico, EVA scores) según GDPR/HIPAA?
  - ¿Usar JWT o OAuth 2.0 para autenticación de API?
- **Escalabilidad**: 
  - ¿Cómo optimizar consultas de progreso por paciente si el dataset crece?
  - ¿Cómo manejar múltiples sesiones de terapia para un mismo paciente?
- **UX/UX**: 
  - ¿Cómo diseñar transiciones entre segmentos corporales (cervical/lumbar) en la UI?
  - ¿Cómo visualizar el "desbloqueo" de nuevos ejercicios tras cumplir EVA <6?
  - ¿Cómo mostrar imágenes de ejercicios con etiquetas ALT accesibles?
- **Extensibilidad**: 
  - ¿Cómo permitir que fisioterapeutas añadan nuevos ejercicios sin código?
  - ¿Cómo integrar recomendaciones AI (ej. basado en historial de EVA)? 
