# Entrenador Personal Garmin

Kit para construir un entrenador personal asistido por IA que se adapta a la
vida real, el historial, la disponibilidad y los objetivos de cada atleta.
Garmin aporta datos; el perfil humano aporta el contexto que el reloj no conoce.

El proyecto no incluye datos, contraseñas ni tokens de nadie. Cada persona crea
su propio perfil y autentica su propia cuenta Garmin en su computadora.

## Qué resuelve

- Convierte objetivos y disponibilidad real en un plan semanal ajustable.
- Consulta actividad, sueño, HRV, estrés, carga y recuperación mediante Garmin MCP.
- Separa claramente datos medidos, datos declarados, estimaciones e inferencias.
- Compara lo planificado con lo ejecutado y cierra el ciclo cada semana.
- Empieza con Garmin en modo de solo lectura. Escribir entrenamientos requiere
  una aprobación explícita del atleta.

## Inicio rápido

Requisitos: Git, Python 3.11 o posterior, `uv`/`uvx` y un cliente compatible con
MCP como Codex o Claude Desktop.

```bash
git clone https://github.com/jivalare-lab/entrenador-personal-garmin.git
cd entrenador-personal-garmin
cp profile/athlete.example.toml profile/athlete.toml
python3 scripts/validate_profile.py profile/athlete.toml --strict
```

Después:

1. Completa `profile/athlete.toml` con tu realidad. La lista completa está en
   [Datos necesarios](docs/DATOS_NECESARIOS.md).
2. Configura Garmin siguiendo [Garmin MCP](docs/GARMIN_MCP.md). La contraseña se
   escribe una sola vez en una terminal local y nunca se guarda en este repo.
3. Abre el proyecto con tu asistente. `AGENTS.md` contiene el contrato del entrenador.
4. Pide: `Haz mi evaluación inicial usando mi perfil y los últimos 28 días de Garmin`.

Con Claude también puedes empezar sin editar el TOML a mano. Abre el proyecto y
escribe:

```text
Lee CLAUDE.md, entrevístame y adapta este entrenador a mi vida, entrenamiento y objetivos.
```

Claude hará el onboarding, confirmará el resumen contigo, creará el perfil local
ignorado por Git y lo validará antes de consultar Garmin.

## Flujo recomendado

```text
perfil + agenda + restricciones
              │
              ▼
  28 días de Garmin ──► línea base
              │
              ▼
      plan semanal realista
              │
       check-in diario
              │
              ▼
   ejecutar y registrar sesión
              │
              ▼
 plan vs. realidad ──► ajuste siguiente semana
```

Los datos del wearable son señales, no diagnósticos. El proyecto no sustituye a
un médico, fisioterapeuta ni entrenador acreditado.

## Estructura

- `AGENTS.md`: reglas que debe seguir el entrenador de IA.
- `CLAUDE.md`: inicio guiado para que Claude entreviste a una persona nueva.
- `profile/`: perfil editable y privado de cada atleta.
- `templates/`: formatos de check-in, plan y revisión.
- `docs/`: método, datos requeridos, seguridad y configuración Garmin.
- `mcp/`: ejemplos seguros para Codex y Claude Desktop.
- `scripts/validate_profile.py`: comprueba que el perfil sea coherente.
- `tests/`: pruebas del validador y de las reglas críticas.

## Verificación

```bash
python3 scripts/validate_profile.py profile/athlete.example.toml
python3 -m unittest discover -s tests -v
```

Consulta [Cómo compartir](docs/COMPARTIR.md) antes de invitar a otra persona.
Las decisiones técnicas y de seguridad están respaldadas en [Fuentes](docs/FUENTES.md).
