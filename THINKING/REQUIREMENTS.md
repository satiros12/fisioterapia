# Software Requirements Specification

## 1. Functional Requirements

### FR1: Anatomical Segmentation Navigation
- The system shall display a hierarchical anatomical navigation menu: major body segment → specific joint/area.
- Example: Columna → Cervical, Lumbar, Torácica, Sacra.

### FR2: Exercise Category Filtering
- For each selected body segment/area, the system shall list exercise types: estiramientos, movilidad activa, fuerza.

### FR3: Protocol-Based Exercise Presentation
- The system shall present exercises organized by therapeutic levels (e.g., Nivel 1, Nivel 2) for each category.
- Exercises within each level shall include detailed instructions and reference images.

### FR4: Pain Assessment (EVA) Integration
- For each exercise, the user shall be able to record a pain value on the EVA scale (0–10).
- The system shall enforce progression logic: if EVA > 6, the user cannot advance to the next level in that exercise category.

### FR5: Checkpoint Completion & Unlocking
- Each exercise shall have a checkbox to mark completion.
- Upon successful, pain-free completion of all checks in a given level, the next level shall unlock automatically.

### FR6: Pathology-Focused Treatment Planning
- The system shall allow filtering exercises by pathology (e.g., epicondilitis) to present relevant protocols.
- A physiotherapist shall be able to select exercises appropriate for a patient’s condition and stage of evolution from the filtered list.

### FR7: Visual Atlas Integration
- Upon opening a body segment, the system shall display an anatomical atlas image highlighting the treatment area.

### FR8: Detailed Exercise Instructions
- Each exercise shall include:
  - Reference pose/execution image(s)
  - Step-by-step instructions (text)
  - Optional: muscle activation illustration
- Instructions shall be clear enough for patient self-administration.

### FR9: Pain Tracking & Comparison
- The system shall store EVA scores per exercise (before and after if applicable) and allow comparison across sessions.

### FR10: User Roles
- Role: Fisioterapeuta (therapist): can prescribe exercises, set treatment plans, unlock levels, view progress.
- Role: Paciente (patient): can view prescribed exercises, execute them, record EVA, mark completions.

## 2. Use Cases

### UC1: Browse Exercises by Body Segment
- Actor: Fisioterapeuta or Paciente
- Precondition: User is authenticated.
- Flow:
  1. User selects major body segment (e.g., “Columna”).
  2. System displays subsegments (Cervical, Lumbar, Torácica, Sacra) and possibly an atlas image.
  3. User selects subsegment.
  4. System presents exercise categories (estiramientos, movilidad activa, fuerza) for that subsegment.
  5. User selects a category.
  6. System shows exercises in current level (starting with Nivel 1).
- Postcondition: Exercises are displayed with instructions and images; EVA and check-in fields available.

### UC2: Progression Through Levels with EVA Check
- Actor: Paciente (executing exercises)
- Precondition: Exercise category is selected and displayed.
- Flow:
  1. For each exercise in current level, user marks completion via checkbox.
  2. Before/after performing the exercise, user records EVA pain score.
  3. If EVA > 6, the system retains the current level and notifies user that advancement is blocked until pain is manageable.
  4. If all exercises in current level are completed with EVA ≤ 6, the system unlocks the next level.
- Postcondition: Next level becomes accessible; progress is logged.

### UC3: Select Exercises for a Specific Pathology
- Actor: Fisioterapeuta
- Precondition: User is authenticated and in treatment planning mode.
- Flow:
  1. User selects “Filtrar por patología.”
  2. User chooses a pathology from a list (e.g., epicondilitis).
  3. System displays all exercises applicable to that pathology.
  4. Therapist selects exercises deemed appropriate for the patient’s current stage.
  5. Therapist assigns selected exercises to the patient’s treatment plan.
- Postcondition: Assigned exercises appear in patient’s dashboard under appropriate levels.

### UC4: View Anatomical Atlas for Segment
- Actor: Fisioterapeuta or Paciente
- Precondition: Body segment list is displayed.
- Flow:
  1. User selects a major segment (e.g., Columna).
  2. System shows an anatomical atlas image highlighting the vertebrae or region relevant to the segment.
- Postcondition: Visual reference is visible; user can proceed to subsegments.

### UC5: Record and Compare Pain Scores
- Actor: Paciente
- Precondition: Exercise is performed.
- Flow:
  1. User records EVA value before exercise.
  2. After completing the exercise, user records EVA value again.
  3. System stores both values and, over time, shows comparison chart or list.
- Postcondition: Pain trend data is saved and available for review by therapist and patient.

## 3. Non-Functional Requirements

### NFR1: Performance
- Page loads for exercise categories should be < 2 seconds on standard broadband.
- Not applicable for early local version.

### NFR2: Usability
- Exercise screens must be legible and intuitive; images must be clear, instructions in Spanish.
- Progress unlocking must be unambiguous.

### NFR3: Maintainability
- Codebase should follow modular structure (backend/API, frontend, data models).
- Requirements may evolve; implement using a framework like Flask (per plan) with clear separation of concerns.

## 4. Data Requirements

- Exercises: ID, title, description, images, instructions (step-by-step), associated body segment(s), category (estiramiento/movilidad/fuerza), level, associated muscles, applicable pathologies.
- Patients: name, age, condition, assigned treatment plan, exercise schedule/completion history, EVA records.
- Treatment Plans: list of exercises per patient, progression status (current level per category), therapist notes.

## 5. External Interfaces

- UI: Web application (responsive, Bootstrap 5 suggested).
- Data source: Internal database (likely SQLite or SQLAlchemy for MVP).
- Optional: Export reports (PDF/CSV) of patient progress.