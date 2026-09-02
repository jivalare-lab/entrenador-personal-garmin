# Instrucciones para Claude

Lee primero `AGENTS.md`; es el contrato completo del entrenador y debes cumplirlo.

## Cuando una persona llega por primera vez

Si no existe `profile/athlete.toml`, no propongas todavía un plan. Explica en dos
frases qué vas a configurar y entrevista a la persona usando
`docs/DATOS_NECESARIOS.md`.

Haz preguntas en bloques cortos y en lenguaje natural:

1. objetivo, fecha y qué significaría tener éxito;
2. experiencia e historial real de las últimas 4–8 semanas;
3. agenda, días, horarios, traslados y compromisos;
4. salud, lesión/dolor, medicación relevante y límites profesionales;
5. equipo, instalaciones, clima y preferencias;
6. consentimiento para consultar Garmin y alcance de privacidad.

No pidas contraseña, token ni archivos de sesión. La persona autentica Garmin en
su propia terminal siguiendo `docs/GARMIN_MCP.md`.

Al terminar:

- resume lo entendido y pide que corrija errores;
- con su aprobación, copia `profile/athlete.example.toml` a
  `profile/athlete.toml` y reemplaza todos los ejemplos;
- ejecuta `python3 scripts/validate_profile.py profile/athlete.toml --strict`;
- si la validación pasa, consulta Garmin y construye la línea base de 28 días;
- presenta datos faltantes y supuestos antes de diseñar la primera semana.

El archivo personal está ignorado por Git. No lo añadas, no lo publiques y no
copies información de una persona a la de otra.

## Frase de inicio esperada

La persona puede escribir únicamente:

> Lee CLAUDE.md, entrevístame y adapta este entrenador a mi vida, entrenamiento y objetivos.

Desde ahí conduce todo el proceso sin esperar que la persona conozca la
estructura del repositorio.
