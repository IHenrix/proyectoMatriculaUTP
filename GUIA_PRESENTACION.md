# 🎓 GUÍA DE PRESENTACIÓN DEL PROYECTO FINAL

**Sistema de Matrículas y Notas - UTP**
**Curso:** Diseño de Patrones (100000SI47)
**Duración Total:** 25 minutos (5 min por persona)

---

## 👥 INTEGRANTES DEL GRUPO

1. **Prada Guerra Ricardo Enrique**
2. **Morales Velásquez Juan José**
3. **Acevedo Huarachi Kelvin Jesús**
4. **Campusanto Solís Ángel**
5. **Saldaña Chávez, Joel Anthony**

---

## 📋 DIVISIÓN DE LA PRESENTACIÓN

| # | Expositor | Tiempo | Tema Principal |
|---|-----------|--------|----------------|
| 1 | Ricardo Prada | 5 min | Introducción + Arquitectura + Patrones Clave |
| 2 | Juan José Morales | 5 min | Funcionalidades del Administrador |
| 3 | Kelvin Acevedo | 5 min | Flujo Completo - Alumno se Matricula |
| 4 | Ángel Campusanto | 5 min | Funcionalidades del Profesor + Notas |
| 5 | Joel Saldaña | 5 min | Alumno ve Notas + GRASP + Reportes |

---

## 🎯 FLUJO VISUAL DE LA PRESENTACIÓN

```
RICARDO (Introducción)
    ↓ Presenta proyecto, tecnologías y arquitectura
    ↓ Muestra los 3 dashboards diferentes
    ↓ Explica patrones principales: Observer, Singleton, Facade

JUAN JOSÉ (Admin crea usuarios)
    ↓ Demuestra gestión de usuarios
    ↓ Crea alumno y profesor para el flujo
    ↓ Muestra gestión académica (cursos, ciclos, secciones)

KELVIN (Alumno se matricula)
    ↓ Login como alumno
    ↓ Proceso completo de matrícula
    ↓ Demuestra Observer Pattern (vacantes se actualizan automáticamente)

ÁNGEL (Profesor gestiona notas)
    ↓ Ve al alumno matriculado
    ↓ Registra notas por componentes
    ↓ Muestra cálculo automático de promedio (Strategy + Singleton)

JOEL (Alumno ve notas + Cierre)
    ↓ Alumno consulta sus notas
    ↓ Ve promedio y estado (APROBADO/DESAPROBADO)
    ↓ Genera reportes (Strategy Pattern)
    ↓ Resumen final de patrones GRASP
```

---

# 👤 1. RICARDO PRADA (5 minutos)

## ROL: Introducción + Arquitectura General + Patrones Clave

### 📝 CONTENIDO DETALLADO

#### A. Introducción del Proyecto (1 minuto)

**Qué decir:**
> "Buenos días/tardes. Somos el grupo [número] y vamos a presentar nuestro Sistema de Matrículas y Notas para la Universidad Tecnológica del Perú."

**Puntos clave:**
- Sistema completo de gestión académica
- **Tecnologías:** Django (Python), MySQL, HTML/CSS/JavaScript
- **Objetivo:** Aplicar 17+ patrones de diseño en un sistema real
- **Cobertura:** 75% de patrones, 100% de GRASP ⭐

**Qué mostrar:**
- Abrir el proyecto en VS Code
- Mostrar estructura de carpetas brevemente

---

#### B. Arquitectura y Patrones Principales (3 minutos)

**Qué decir:**
> "Implementamos una arquitectura en 3 capas siguiendo el patrón MVT de Django y agregamos una capa de servicios para aplicar patrones de diseño."

**Diagrama de capas a explicar:**
```
┌─────────────────────────────────────┐
│         TEMPLATES (Views)           │  ← Presentación
├─────────────────────────────────────┤
│      VIEWS (Controllers)            │  ← GRASP Controller
│      + Decorators (@login_required) │  ← Decorator Pattern
├─────────────────────────────────────┤
│         SERVICES LAYER              │  ← Facade Pattern
│  (UsuarioService, MatriculaService, │  ← Pure Fabrication
│   NotaService, ReporteService)      │  ← Command Pattern
├─────────────────────────────────────┤
│           SIGNALS                   │  ← Observer Pattern ⭐
├─────────────────────────────────────┤
│           MODELS                    │  ← Information Expert
│     (Usuario, Curso, Matrícula...)  │  ← Factory Pattern
├─────────────────────────────────────┤
│         DJANGO ORM                  │  ← Repository Pattern
├─────────────────────────────────────┤
│           MySQL                     │
└─────────────────────────────────────┘
```

**Archivos a mostrar:**

1. **Observer Pattern** - `academic_system/signals.py`
   ```python
   # Líneas 17-42
   @receiver(post_save, sender='academic_system.Matricula')
   def actualizar_vacantes_al_matricular(sender, instance, created, **kwargs):
       """
       OBSERVER PATTERN: Cuando se crea una matrícula,
       automáticamente actualiza las vacantes.
       """
       if created and instance.is_active:
           instance.seccion.vacantes_ocupadas += 1
           instance.seccion.save()
   ```

   **Explicar:**
   > "Este es el Observer Pattern. Cuando se crea una matrícula, el signal se ejecuta automáticamente actualizando las vacantes. La clase Matrícula no necesita saber nada sobre gestión de vacantes. Esto es **desacoplamiento**."

2. **Singleton Pattern** - `academic_system/singleton.py`
   ```python
   # Líneas 15-80
   class ConfiguracionSistema:
       _instance = None
       _lock = Lock()

       def __new__(cls):
           if cls._instance is None:
               with cls._lock:
                   if cls._instance is None:
                       cls._instance = super().__new__(cls)
           return cls._instance
   ```

   **Explicar:**
   > "Singleton Pattern garantiza una única instancia de configuración en todo el sistema. Es thread-safe usando Lock. Centraliza valores como nota mínima aprobatoria (11.6), créditos máximos, etc."

3. **Service Layer** (Facade) - Mostrar carpeta `services/`

   **Explicar:**
   > "La capa de servicios implementa Facade Pattern, simplificando operaciones complejas con interfaces limpias. Por ejemplo, `MatriculaService.matricular_alumno()` internamente valida ciclo, vacantes, duplicados, usa transacciones, crea notas... pero el cliente solo llama un método."

---

#### C. Demo Rápida Navegando Dashboards (1 minuto)

**Qué hacer:**
1. Abrir navegador: `http://localhost:8000`
2. Login como admin
3. Mostrar dashboard de admin (estadísticas)
4. Logout
5. Login como profesor
6. Mostrar dashboard de profesor (secciones)
7. Logout
8. Login como alumno
9. Mostrar dashboard de alumno

**Qué decir:**
> "Aquí vemos polimorfismo en acción. El método `Usuario.get_dashboard_url()` retorna diferente dashboard según el rol, sin condicionales en el código cliente."

**Código a mostrar** - `models.py:84-99`
```python
def get_dashboard_url(self):
    """POLYMORPHISM (GRASP): Comportamiento según rol"""
    dashboard_map = {
        'administrador': 'admin_dashboard',
        'profesor': 'profesor_dashboard',
        'alumno': 'alumno_dashboard',
    }
    return dashboard_map.get(self.rol, 'login')
```

---

### 📂 ARCHIVOS A TENER ABIERTOS

- VS Code con:
  - `README.md` (arquitectura)
  - `signals.py`
  - `singleton.py`
  - `models.py` (Usuario)
- Navegador con sistema corriendo

### 🎯 PATRONES A DESTACAR

1. ✅ **Observer Pattern** (Signals)
2. ✅ **Singleton Pattern** (ConfiguracionSistema)
3. ✅ **Facade Pattern** (Service Layer)
4. ✅ **Polymorphism** (get_dashboard_url)

### 💬 FRASE DE CIERRE

> "Ahora Juan José les mostrará las funcionalidades del administrador y cómo se crean los usuarios del sistema."

---

# 👤 2. JUAN JOSÉ MORALES (5 minutos)

## ROL: Funcionalidades del ADMINISTRADOR

### 📝 CONTENIDO DETALLADO

#### A. Dashboard de Administrador (1 minuto)

**Qué hacer:**
1. Login como admin: `admin` / `admin123`
2. Mostrar dashboard

**Qué decir:**
> "Como administrador tengo acceso completo al sistema. El dashboard muestra estadísticas generales."

**Qué señalar:**
- Número total de usuarios
- Cursos, secciones activas
- Estadísticas del ciclo actual
- Menú de navegación con todas las opciones

**Patrón a mencionar:**
> "Este dashboard usa el **GRASP Controller**. La vista actúa como controlador, coordinando entre los modelos y la presentación."

---

#### B. Gestión de Usuarios (2 minutos)

**Qué hacer:**

1. **Crear un Alumno:**
   - Ir a "Gestión de Usuarios" → "Crear Usuario"
   - Llenar formulario:
     - Nombre: "Carlos"
     - Apellidos: "Pérez López"
     - DNI: "75000001"
     - Rol: **Alumno**
   - Click "Crear Usuario"
   - Mostrar que el código se generó automáticamente (ej: U12345678)

2. **Crear un Profesor:**
   - Crear otro usuario
   - Nombre: "María"
   - Apellidos: "García Díaz"
   - DNI: "75000002"
   - Rol: **Profesor**
   - Guardar

3. **Mostrar lista de usuarios**
   - Ver tabla con usuarios creados
   - Mostrar filtros por rol

**Qué decir:**

> "Aquí vemos el **Factory Pattern** en acción. El código único del usuario (U12345678) se genera automáticamente usando el método `generar_codigo()`."

**Código a mostrar** - `models.py:142-152`
```python
@staticmethod
def generar_codigo():
    """
    Factory Method para generar código único de usuario.
    Formato: U + 8 dígitos aleatorios
    """
    while True:
        codigo = 'U' + ''.join(random.choices(string.digits, k=8))
        if not Usuario.objects.filter(codigo=codigo).exists():
            return codigo
```

**Explicar:**
> "El Factory Method garantiza que cada código sea único. Si existe duplicado, genera otro. Esto aplica el principio DRY - Don't Repeat Yourself."

---

#### C. Gestión Académica (2 minutos)

**Qué hacer:**
1. Ir a "Django Admin" (o mostrar panel de gestión académica)
2. Mostrar brevemente:
   - **Cursos**: Lista de cursos (Matemática, Programación, etc.)
   - **Ciclos**: Períodos académicos con fechas de matrícula
   - **Secciones**: Secciones de cursos con profesores asignados

**Qué señalar en Ciclos:**
- Campo `matricula_abierta` (Boolean)
- Fechas de inicio y fin de matrícula
- Método `puede_matricularse()` (Information Expert)

**Código a mostrar** - `models.py:152-162`
```python
def puede_matricularse(self):
    """
    Strategy Pattern: Validación de matrícula.
    Information Expert: El ciclo conoce su estado.
    """
    from datetime import date
    hoy = date.today()
    return (
        self.matricula_abierta and
        self.fecha_inicio_matricula <= hoy <= self.fecha_fin_matricula
    )
```

**Qué señalar en Secciones:**
- Vacantes totales y ocupadas
- Profesores asignados (ManyToMany)
- Horarios y modalidad (presencial/virtual)

**Qué decir:**
> "Aquí aplicamos **Information Expert**. El ciclo sabe si permite matrícula, la sección sabe si tiene vacantes. Cada objeto gestiona su propia información."

---

### 📂 ARCHIVOS A TENER ABIERTOS

- VS Code:
  - `views.py` (admin_dashboard, líneas 86-160)
  - `models.py` (Usuario, líneas 20-160)
  - `models.py` (Ciclo, Seccion)
- Navegador: Sistema como admin + Django Admin

### 🎯 PATRONES A DESTACAR

1. ✅ **Factory Pattern** (generar_codigo)
2. ✅ **GRASP Controller** (admin_dashboard)
3. ✅ **Information Expert** (puede_matricularse, tiene_vacantes)
4. ✅ **Decorator Pattern** (@admin_required)

### 💬 FRASE DE CIERRE

> "Con estos usuarios creados, Kelvin va a demostrar el flujo completo de matrícula desde la perspectiva del alumno."

---

# 👤 3. KELVIN ACEVEDO (5 minutos)

## ROL: FLUJO COMPLETO - Alumno se Matricula

### 📝 CONTENIDO DETALLADO

#### A. Login como Alumno (30 segundos)

**Qué hacer:**
1. Logout del admin
2. Login con el alumno creado:
   - Usuario: `U12345678` (el código generado)
   - Contraseña: `75000001` (el DNI por defecto)
3. Mostrar dashboard de alumno

**Qué decir:**
> "Voy a iniciar sesión como el alumno que Juan José acaba de crear. Noten que la contraseña por defecto es el DNI."

**Qué señalar:**
- Dashboard personalizado del alumno
- Menú reducido (solo opciones de alumno)
- Decorator Pattern controlando acceso

**Código a mostrar** - `decorators.py:65-71`
```python
def alumno_required(view_func):
    """Decorator para vistas que requieren rol de alumno."""
    return rol_requerido('alumno')(view_func)

@alumno_required  # Solo alumnos pueden acceder
def matricularse(request, seccion_id):
    ...
```

**Explicar:**
> "El **Decorator Pattern** protege esta vista. Si un profesor intenta acceder, será redirigido. Esto es el principio de **segregación de interfaces**."

---

#### B. Proceso de Matrícula (3 minutos) ⭐ **MÁS IMPORTANTE**

**Qué hacer:**

1. **Ver Secciones Disponibles:**
   - Ir a "Matricularse" o "Buscar Secciones"
   - Mostrar tabla con secciones disponibles
   
2. **Matricularse:**
   - Click en "Matricularme" en una sección
   - Esperar confirmación
   - **IMPORTANTE:** Mostrar que las vacantes cambiaron automáticamente

3. **Después de Matricularse:**
   > "Ahora tiene 24 vacantes disponibles. ¿Qué pasó? El **Observer Pattern** actualizó automáticamente las vacantes cuando me matriculé."

**Qué decir (CLAVE):**

> "Este es el **Observer Pattern** en acción. Cuando me matriculo:
> 1. Se crea un objeto Matrícula
> 2. Django emite un signal `post_save`
> 3. El observer `actualizar_vacantes_al_matricular` se ejecuta automáticamente
> 4. Actualiza las vacantes sin que Matrícula sepa cómo
>
> Esto es **desacoplamiento**. Si mañana queremos enviar un email de bienvenida, solo agregamos otro observer. No modificamos la matrícula."

**Código a mostrar en pantalla dividida:**

*Lado izquierdo* - `views.py:299-340` (matricularse):
```python
@alumno_required
@login_required
def matricularse(request, seccion_id):
    try:
        # Command Pattern: Ejecuta comando de matrícula
        matricula = MatriculaService.matricular_alumno(
            alumno_id=request.user.id,
            seccion_id=seccion_id
        )
        messages.success(request, '¡Te has matriculado exitosamente!')
    except Exception as e:
        messages.error(request, str(e))
```

*Lado derecho* - `signals.py:17-42`:
```python
@receiver(post_save, sender='academic_system.Matricula')
def actualizar_vacantes_al_matricular(sender, instance, created, **kwargs):
    """
    OBSERVER PATTERN: Reacciona cuando se crea matrícula.
    """
    if created and instance.is_active:
        # Incrementar vacantes ocupadas
        instance.seccion.vacantes_ocupadas += 1
        instance.seccion.save(update_fields=['vacantes_ocupadas'])
```

**Explicar técnicamente:**
> "El servicio usa **Command Pattern** - encapsula toda la operación de matrícula. Internamente valida ciclo, vacantes, duplicados, usa transacciones. Es **Facade** también - oculta complejidad."

---

#### C. Ver Cursos Matriculados (1.5 minutos)

**Qué hacer:**
1. Volver al dashboard
2. Ir a "Mis Cursos" o "Cursos Matriculados"
3. Mostrar tabla con el curso recién matriculado

**Qué señalar:**
- Información del curso
- Sección, horario
- Créditos del curso
- Estado de la matrícula (Activa)

**Qué decir:**
> "Aquí vemos **Information Expert** nuevamente. La matrícula conoce sus propios créditos."

**Código a mostrar** - `models.py:415-417`
```python
@property
def creditos(self):
    """Information Expert: La matrícula conoce sus créditos"""
    return self.seccion.curso.creditos
```

---

### 📂 ARCHIVOS A TENER ABIERTOS

- VS Code:
  - `decorators.py:65-71` (alumno_required)
  - `signals.py:17-42` (Observer actualizar vacantes)
  - `views.py:299-340` (matricularse)
  - `matricula_service.py:60-110` (matricular_alumno)
- Navegador: Sistema como alumno
- Notepad: Anotar vacantes antes/después para mostrar diferencia

### 🎯 PATRONES A DESTACAR

1. ✅ **Observer Pattern** ⭐ (el más importante)
2. ✅ **Command Pattern** (MatriculaService.matricular_alumno)
3. ✅ **Decorator Pattern** (@alumno_required)
4. ✅ **Facade Pattern** (servicio oculta complejidad)
5. ✅ **Information Expert** (matrícula conoce créditos)

### 💬 FRASES CLAVE

**Al matricularse:**
> "Observer Pattern: La matrícula NO sabe que las vacantes se van a actualizar. El signal lo hace automáticamente. Esto es desacoplamiento."

**Al mostrar cursos:**
> "Information Expert: Cada objeto conoce su propia información. La matrícula sabe sus créditos, la sección sabe si tiene vacantes."

### 💬 FRASE DE CIERRE

> "Ahora que estoy matriculado, Ángel va a mostrar cómo el profesor me ve en su lista de alumnos y registra mis notas."

---

# 👤 4. ÁNGEL CAMPUSANTO (5 minutos)

## ROL: Funcionalidades del PROFESOR + Registro de Notas

### 📝 CONTENIDO DETALLADO

#### A. Login como Profesor (30 segundos)

**Qué hacer:**
1. Logout del alumno
2. Login con el profesor creado:
   - Usuario: `U87654321` (el código del profesor)
   - Contraseña: `75000002` (DNI)
3. Mostrar dashboard de profesor

**Qué decir:**
> "Como profesor, mi dashboard es diferente. Puedo ver mis secciones asignadas y gestionar notas."

**Qué señalar:**
- Lista de secciones asignadas
- Accesos disponibles (ver alumnos, registrar notas)

---

#### B. Ver Alumnos de la Sección (1 minuto)

**Qué hacer:**
1. Seleccionar la sección donde se matriculó el alumno
2. Ver lista de alumnos matriculados
3. **Confirmar que el alumno aparece** (el que Kelvin matriculó)

**Qué decir:**
> "Aquí está el alumno que se acaba de matricular. El sistema muestra todos los alumnos en tiempo real."

**Qué señalar:**
- Nombre del alumno
- Código del alumno
- Estado de matrícula
- Botón para registrar notas

**Patrón a mencionar:**
> "El servicio `NotaService.obtener_alumnos_seccion()` usa **Facade Pattern**, simplificando una consulta compleja de base de datos con joins múltiples."

---

#### C. Registrar Notas (2.5 minutos) ⭐ **MÁS IMPORTANTE**

**Qué hacer:**

1. **Acceder a Registro de Notas:**
   - Click en "Registrar Notas" del alumno
   - Mostrar formulario con componentes de evaluación
   - Ejemplo: PC1 (20%), PC2 (20%), PC3 (20%), Proyecto Final (40%)

2. **Registrar Primera Nota:**
   - PC1: **16.5**
   - Guardar
   - Mostrar que promedio aún está en cálculo

3. **Registrar Más Notas:**
   - PC2: **14.0**
   - PC3: **15.5**
   - Mostrar que el promedio se actualiza automáticamente

4. **Registrar Nota Final:**
   - Proyecto Final: **18.0**
   - Guardar
   - **Mostrar:**
     - Promedio ponderado calculado automáticamente (ej: 16.10)
     - Estado: **APROBADO** (porque ≥ 11.6)

**Qué decir (CLAVE):**

> "Aquí vemos dos patrones trabajando juntos:
>
> **1. Strategy Pattern:** El cálculo del promedio ponderado usa un algoritmo específico:
> `(16.5 * 0.20) + (14.0 * 0.20) + (15.5 * 0.20) + (18.0 * 0.40) = 16.10`
>
> **2. Singleton Pattern:** La nota mínima aprobatoria (11.6) NO está hardcodeada. Viene del ConfiguracionSistema. Si necesitamos cambiarla a 12.0, solo modificamos el Singleton y todo el sistema se actualiza."

**Código a mostrar - SPLIT SCREEN:**

*Izquierda* - `models.py:495-515` (cálculo de promedio):
```python
@staticmethod
def calcular_promedio_ponderado(matricula):
    """
    Strategy Pattern: Cálculo de promedio ponderado.
    Information Expert: Las notas conocen cómo calcularse.
    """
    componentes = ComponenteEvaluacion.objects.filter(
        curso=matricula.seccion.curso
    ).order_by('orden')

    total_ponderado = Decimal('0')
    for componente in componentes:
        nota = Nota.objects.filter(
            matricula=matricula,
            componente=componente,
            valor__isnull=False
        ).first()

        if nota and nota.valor is not None:
            # Promedio ponderado
            total_ponderado += (nota.valor * componente.porcentaje) / Decimal('100')

    return round(total_ponderado, 2)
```

*Derecha* - `models.py:532-539` (estado de aprobación):
```python
@staticmethod
def estado_aprobacion(promedio):
    """
    Strategy Pattern: Determina estado de aprobación.
    SINGLETON PATTERN: Usa configuración única del sistema.
    """
    if promedio is None:
        return 'PENDIENTE'

    # SINGLETON PATTERN: Obtiene configuración
    from .singleton import ConfiguracionSistema
    config = ConfiguracionSistema()

    if promedio >= config.nota_minima_aprobacion:  # 11.6
        return 'APROBADO'
    else:
        return 'DESAPROBADO'
```

**Explicar técnicamente:**

> "Noten que `config.nota_minima_aprobacion` retorna 11.6. Este valor está en el Singleton. En cualquier parte del sistema que pregunten por la configuración, obtendrán LA MISMA instancia.
>
> Esto es **centralización de configuración** - un principio clave de arquitectura de software."

**Mostrar el Singleton** - `singleton.py:66-73`:
```python
def _cargar_configuracion(self):
    # Configuración académica
    self.nota_minima_aprobacion = Decimal('11.6')
    self.nota_maxima = Decimal('20.0')
    self.max_creditos_por_ciclo = 24
    # ...
```

---

#### D. Estadísticas y Gráficos (1 minuto)

**Qué hacer:**
1. Ir a "Estadísticas de la Sección"
2. Mostrar:
   - Gráfico de distribución de notas
   - Promedio general de la sección
   - Top 5 alumnos
   - Alumnos con bajo rendimiento

**Qué decir:**
> "Estas estadísticas usan queries complejas optimizadas en el servicio. Otro ejemplo de **Facade Pattern**."

---

### 📂 ARCHIVOS A TENER ABIERTOS

- VS Code:
  - `views.py:162-220` (profesor_dashboard)
  - `models.py:495-539` (cálculo promedio + estado)
  - `singleton.py:66-80` (configuración)
  - `nota_service.py` (métodos de servicio)
- Navegador: Sistema como profesor
- Calculadora: Para mostrar cálculo manual del promedio

### 🎯 PATRONES A DESTACAR

1. ✅ **Strategy Pattern** ⭐ (cálculo de promedio)
2. ✅ **Singleton Pattern** ⭐ (nota mínima aprobatoria)
3. ✅ **Facade Pattern** (servicio de notas)
4. ✅ **Information Expert** (nota se calcula a sí misma)
5. ✅ **Decorator Pattern** (@profesor_required)

### 💬 FRASES CLAVE

**Al registrar notas:**
> "Strategy Pattern permite cambiar el algoritmo de cálculo sin afectar el resto del código. Hoy es promedio ponderado, mañana podría ser promedio simple o con redondeo especial."

**Al mostrar estado:**
> "Singleton garantiza que todos en el sistema usen la misma configuración. Una única fuente de verdad. No hay inconsistencias."

**Al mostrar estadísticas:**
> "Facade Pattern oculta 10 líneas de queries SQL complejos detrás de un método simple: `obtener_estadisticas(seccion_id)`"

### 💬 FRASE DE CIERRE

> "Con las notas registradas, Joel va a mostrar cómo el alumno las visualiza en su dashboard, y cerrará explicando todos los patrones GRASP que implementamos."

---

# 👤 5. JOEL SALDAÑA (5 minutos)

## ROL: Alumno ve Notas + Patrones GRASP + Reportes + Cierre

### 📝 CONTENIDO DETALLADO

#### A. Login como Alumno (30 segundos)

**Qué hacer:**
1. Logout del profesor
2. Login como el alumno (el mismo que se matriculó)
3. Ir al dashboard

**Qué decir:**
> "Volvemos al alumno para ver cómo visualiza las notas que el profesor acaba de registrar."

---

#### B. Ver Notas del Curso (2 minutos)

**Qué hacer:**

1. **Ir a "Mis Cursos"**
2. **Seleccionar el curso matriculado**
3. **Mostrar tabla de notas:**
   - Componente | Porcentaje | Nota | Contribución
   - PC1 (20%) | 16.5 | 3.30
   - PC2 (20%) | 14.0 | 2.80
   - PC3 (20%) | 15.5 | 3.10
   - Proyecto (40%) | 18.0 | 7.20
   - **Promedio Final:** 16.10
   - **Estado:** APROBADO ✅

**Qué señalar:**
- Desglose por componente
- Contribución al promedio
- Promedio ponderado total
- Estado en verde/rojo según aprobación

**Qué decir:**

> "Aquí aplicamos **Information Expert**. La nota conoce cómo calcularse. El modelo Nota tiene toda la información necesaria (valor, porcentaje del componente) y ejecuta su propio cálculo.
>
> No necesitamos preguntarle a otros objetos. Este es el principio de **Information Expert de GRASP**: asignar responsabilidad al objeto que tiene la información."

**Código a mostrar** - `models.py:495-515`:
```python
@staticmethod
def calcular_promedio_ponderado(matricula):
    """
    Information Expert: Las notas conocen cómo calcularse.
    """
    # La nota tiene valor y porcentaje
    # No necesita preguntarle a otros objetos
    total_ponderado = (nota.valor * componente.porcentaje) / 100
    return total_ponderado
```

---

#### C. Reportes - Strategy Pattern Mejorado (1.5 minutos)

**Qué hacer:**

1. **Volver al profesor** (logout/login rápido)
2. **Generar Reporte de Notas:**
   - Click en "Exportar Notas"
   - Opciones: Excel | PDF
   - Seleccionar Excel
   - Descargar archivo
   - **Abrir el archivo** para mostrar contenido

3. **Generar en PDF:**
   - Exportar en PDF
   - Mostrar archivo PDF

**Qué decir (CLAVE):**

> "Este es el **Strategy Pattern refactorizado**. Antes teníamos if-else anidados. Ahora tenemos clases estrategia independientes:
>
> - `ListaAlumnosExcelStrategy`
> - `ListaAlumnosPDFStrategy`
> - `NotasSeccionExcelStrategy`
> - `NotasSeccionPDFStrategy`
>
> ¿Ventaja? **Open/Closed Principle**: Puedo agregar un nuevo formato (Word, CSV) sin modificar el código existente, solo registro una nueva estrategia."

**Código a mostrar - SPLIT:**

*Izquierda* - `reporte_service.py:48-74` (clases Strategy):
```python
class ReporteStrategy:
    """Interfaz base para estrategias"""
    def generar(self, **kwargs):
        raise NotImplementedError

class ListaAlumnosExcelStrategy(ReporteStrategy):
    def generar(self, **kwargs):
        return ReporteBuilder.build_lista_alumnos_excel(...)

class ListaAlumnosPDFStrategy(ReporteStrategy):
    def generar(self, **kwargs):
        return ReporteBuilder.build_lista_alumnos_pdf(...)
```

*Derecha* - `reporte_service.py:90-95` (registro de estrategias):
```python
# Registro de estrategias disponibles
_estrategias = {
    ('lista_alumnos', 'excel'): ListaAlumnosExcelStrategy(),
    ('lista_alumnos', 'pdf'): ListaAlumnosPDFStrategy(),
    ('notas_seccion', 'excel'): NotasSeccionExcelStrategy(),
    ('notas_seccion', 'pdf'): NotasSeccionPDFStrategy(),
}
```

**Explicar:**
> "Para agregar reporte en Word, solo hago:
> ```python
> _estrategias[('lista_alumnos', 'word')] = ListaAlumnosWordStrategy()
> ```
> Sin tocar nada más. Eso es **extensibilidad** sin **modificación**."

---

#### D. Resumen de Patrones GRASP (1 minuto) ⭐ **CIERRE FUERTE**

**Qué hacer:**
- Volver a VS Code
- Abrir `README.md` sección GRASP (líneas 271-284)
- Mostrar en pantalla completa

**Qué decir (con energía):**

> "Para cerrar, quiero destacar que implementamos **100% de patrones GRASP**. Los 8 patrones:
>
> **1. Controller** ✅ - Las vistas actúan como controladores en MVT
>
> **2. Information Expert** ✅ - Cada modelo gestiona su propia información
>    - Sección conoce si tiene vacantes
>    - Ciclo sabe si permite matrícula
>    - Nota conoce cómo calcularse
>
> **3. Creator** ✅ - Objetos crean lo que contienen
>    - Matrícula crea sus Notas asociadas
>    - Usuario genera su propio código
>
> **4. Low Coupling** ✅ - Capas separadas: Models → Services → Views
>    - Cambios en modelos no afectan vistas
>    - Services desacoplan lógica de negocio
>
> **5. High Cohesion** ✅ - Cada clase tiene responsabilidad única
>    - UsuarioService solo maneja usuarios
>    - NotaService solo maneja notas
>
> **6. Pure Fabrication** ✅ - Clases service no representan entidades del dominio
>    - ReporteService, MatriculaService = fabricaciones puras
>
> **7. Polymorphism** ✅ - Comportamiento según tipo
>    - `Usuario.get_dashboard_url()` varía según rol
>    - `Usuario.puede_gestionar_*()` retorna diferente por rol
>
> **8. Protected Variations** ✅ - Servicios protegen cambios
>    - Si cambio ORM de Django a SQLAlchemy, solo modifico servicios
>    - Las vistas no se enteran
>
> **Además implementamos:**
> - 5/5 Principios SOLID ✅
> - 3 Patrones Creacionales (Factory, Builder, Singleton)
> - 2 Patrones Estructurales (Facade, Decorator)
> - 3 Patrones de Comportamiento (Strategy, Command, Observer)
> - **Total: 17+ patrones en un sistema funcional real**"

---

### 📂 ARCHIVOS A TENER ABIERTOS

- VS Code:
  - `README.md:271-321` (sección GRASP + resumen)
  - `reporte_service.py:24-148` (Strategy Pattern)
  - `views.py:259-295` (alumno notas)
  - `PATRONES_IMPLEMENTADOS.md` (resumen técnico)
- Navegador: Sistema como alumno
- Archivos descargados: Excel y PDF para mostrar

### 🎯 PATRONES A DESTACAR

1. ✅ **Information Expert** (notas se calculan solas)
2. ✅ **Strategy Pattern refactorizado** (reportes)
3. ✅ **Todos los GRASP** (8/8) ⭐
4. ✅ **Open/Closed Principle** (extensión sin modificación)

### 💬 FRASES CLAVE

**Al mostrar notas:**
> "Information Expert: La nota tiene la información y ejecuta la lógica. No necesita pedir ayuda."

**Al mostrar reportes:**
> "Strategy Pattern con Open/Closed Principle: agregar formatos sin romper código existente."

**Al cerrar:**
> "100% de GRASP. 75% de cobertura total. 17+ patrones. Sistema funcional. Este proyecto demuestra comprensión profunda de patrones de diseño aplicados a la realidad."

### 💬 FRASE DE CIERRE FINAL

> "Esto concluye nuestra presentación. ¿Alguna pregunta sobre los patrones implementados?"

---

## 🎬 SCRIPT DE TRANSICIONES

**Ricardo → Juan José:**
> "Ahora Juan José les mostrará las funcionalidades del administrador y cómo se crean los usuarios del sistema."

**Juan José → Kelvin:**
> "Con los usuarios creados, Kelvin va a demostrar el flujo completo de matrícula desde la perspectiva del alumno."

**Kelvin → Ángel:**
> "Ahora que estoy matriculado, Ángel mostrará cómo el profesor me ve en su lista y registra mis notas."

**Ángel → Joel:**
> "Con las notas registradas, Joel mostrará cómo el alumno las visualiza y cerrará con el resumen de patrones GRASP."

---

## 📊 TABLA DE PATRONES POR PERSONA

| Expositor | Patrones a Explicar | Tiempo Dedicado |
|-----------|---------------------|-----------------|
| **Ricardo** | Observer, Singleton, Facade, Polymorphism | 3 min patrones |
| **Juan José** | Factory, Controller, Information Expert, Decorator | 2 min patrones |
| **Kelvin** | Observer ⭐, Command, Facade, Decorator, Information Expert | 3.5 min patrones |
| **Ángel** | Strategy ⭐, Singleton ⭐, Facade, Information Expert | 3 min patrones |
| **Joel** | Strategy ⭐, Information Expert, TODOS los GRASP | 2.5 min patrones |

---

## 🎯 CHECKLIST ANTES DE PRESENTAR

### Para Ricardo:
- [ ] Servidor Django corriendo (`python manage.py runserver`)
- [ ] VS Code abierto con archivos relevantes
- [ ] Navegador en `localhost:8000`
- [ ] Login admin preparado
- [ ] `README.md`, `signals.py`, `singleton.py` abiertos

### Para Juan José:
- [ ] Datos de usuario alumno preparados (nombre, DNI)
- [ ] Datos de usuario profesor preparados
- [ ] Django Admin accesible
- [ ] `models.py` en generar_codigo() abierto

### Para Kelvin:
- [ ] Credenciales del alumno anotadas
- [ ] Vacantes actuales anotadas (para mostrar cambio)
- [ ] `signals.py` y `views.py` en split screen
- [ ] Notepad con vacantes antes/después

### Para Ángel:
- [ ] Credenciales del profesor anotadas
- [ ] Notas a registrar decididas (16.5, 14.0, 15.5, 18.0)
- [ ] Calculadora para mostrar promedio manual
- [ ] `models.py` y `singleton.py` en split screen

### Para Joel:
- [ ] Credenciales del alumno
- [ ] `README.md` en sección GRASP abierto
- [ ] `reporte_service.py` abierto
- [ ] `PATRONES_IMPLEMENTADOS.md` como backup

---

## 💡 TIPS GENERALES PARA TODOS

### Durante la Presentación:

1. **Hablar claro y pausado** - Estás explicando conceptos técnicos
2. **Señalar código mientras explicas** - Usar el mouse para indicar líneas específicas
3. **Usar términos técnicos con confianza:**
   - "Desacoplamiento"
   - "Open/Closed Principle"
   - "Thread-safe"
   - "Lazy initialization"
   - "Encapsulamiento"

4. **Mostrar y decir:**
   - No solo leer código
   - Explicar QUÉ hace y POR QUÉ ese patrón

5. **Conectar con el sílabo:**
   - Mencionar "Como vimos en la unidad 4..."
   - "Esto cumple con el principio SOLID de..."

### Si algo sale mal:

- **Si el sistema falla:** Mostrar código mientras se reinicia
- **Si olvidas algo:** Tus compañeros pueden complementar
- **Si te preguntan:** Ser honesto. "Esa parte la implementó [nombre], él puede responder mejor"

### Lenguaje corporal:

- Mantener contacto visual con el profesor/evaluadores
- Gestos con las manos al explicar
- Pararse derecho/a
- Sonreír al empezar y cerrar

---

## 🎤 RESPUESTAS A PREGUNTAS FRECUENTES

### P1: ¿Por qué usaron Singleton para configuración?

**R (Joel o Ricardo):**
> "Porque queremos garantizar que todo el sistema use la misma configuración. Si cada parte tuviera su propia instancia con valores diferentes, tendríamos inconsistencias. El Singleton asegura una única fuente de verdad. Además, es thread-safe, importante para aplicaciones concurrentes."

### P2: ¿Qué diferencia hay entre llamar métodos directamente y usar Observer?

**R (Kelvin):**
> "Sin Observer, Matrícula tendría que saber sobre vacantes y llamar `seccion.actualizar_vacantes()` directamente. Con Observer, Matrícula solo se crea, y los observers reaccionan automáticamente. Ventajas:
> 1. Desacoplamiento - Matrícula no depende de Sección
> 2. Extensibilidad - Podemos agregar más observers (emails, logs) sin modificar Matrícula
> 3. Single Responsibility - Matrícula solo se preocupa de ser matrícula"

### P3: ¿Por qué no solo usar if-else en lugar de Strategy?

**R (Joel):**
> "Tres razones técnicas:
> 1. **Open/Closed Principle**: Con if-else, para agregar un formato debo modificar la función. Con Strategy, solo registro una nueva estrategia.
> 2. **Testeable**: Cada estrategia se testea independientemente. Con if-else todo está mezclado.
> 3. **Mantenible**: 10 formatos con if-else = código ilegible. 10 estrategias = 10 clases limpias."

### P4: ¿Todos los patrones GOF están implementados?

**R (Ricardo, ser honesto):**
> "No todos, pero sí los más importantes y relevantes para este tipo de sistema:
> - **Implementados:** Factory, Builder, Singleton, Facade, Decorator, Strategy, Command, Observer
> - **No implementados:** Prototype, Abstract Factory (tenemos Factory simple), Adapter, Proxy, Bridge, Memento
>
> Cubrimos 60% de patrones creacionales, 33% estructurales, 60% comportamiento, pero 100% de GRASP que son los más fundamentales."

### P5: ¿Cómo demuestra que cumple SOLID?

**R (Cualquiera):**
> "Cada principio SOLID:
> - **S**RP: UsuarioService solo usuarios, NotaService solo notas
> - **O**CP: Strategy permite extensión sin modificación
> - **L**SP: Usuario hereda AbstractUser correctamente, puede usarse en cualquier lugar que espere AbstractUser
> - **I**SP: Cada servicio tiene solo métodos relevantes a su dominio
> - **D**IP: Las vistas dependen de servicios (abstracciones), no de modelos directamente. El service layer invierte la dependencia."

### P6: ¿Esto funciona en producción o solo es educativo?

**R (Ricardo):**
> "Es completamente funcional. Usa Django, framework usado por Instagram, Pinterest, Spotify. Tiene:
> - Base de datos MySQL real
> - Transacciones ACID
> - Autenticación y autorización
> - Validaciones de negocio
> - Manejo de errores
>
> Con ajustes de seguridad (HTTPS, variables de entorno, etc.), podría desplegarse en producción. Los patrones implementados son exactamente los que se usan en sistemas empresariales reales."

---

## 📋 CHECKLIST FINAL DEL DÍA DE LA PRESENTACIÓN

### 30 minutos antes:

- [ ] Todos los miembros presentes
- [ ] Laptop principal con sistema funcionando
- [ ] Backup laptop (si es posible)
- [ ] Proyector/pantalla probados
- [ ] Internet funcionando (si se necesita)
- [ ] VS Code con todos los archivos abiertos
- [ ] Navegador con pestañas necesarias
- [ ] Notas/guía impresa (este documento)

### 10 minutos antes:

- [ ] Ensayo rápido de transiciones
- [ ] Confirmar quién habla primero, segundo...
- [ ] Verificar que sistema responde rápido
- [ ] Preparar login de cada usuario
- [ ] Respirar profundo 😊

### Durante:

- [ ] Cronometrar tiempos (tener reloj visible)
- [ ] Apoyarse entre todos
- [ ] Mantener energía positiva
- [ ] Sonreír y disfrutar

---

## 🏆 MENSAJE FINAL

Este proyecto es sólido. Han implementado:
- ✅ 17+ patrones de diseño
- ✅ 100% de GRASP (8/8)
- ✅ 100% de SOLID (5/5)
- ✅ Sistema funcional real
- ✅ Código bien documentado
- ✅ Arquitectura limpia

**Presenten con confianza. Saben de qué están hablando.**

¡Éxito en su presentación! 🚀

---

**Documento generado:** 2025-11-26
**Proyecto:** Sistema de Matrículas UTP
**Curso:** Diseño de Patrones
**Grupo:** Ricardo Prada, Juan José Morales, Kelvin Acevedo, Ángel Campusanto, Joel Saldaña
