# Garmin MCP: instalación prudente

## Qué opción usa este proyecto

Para uso personal se utiliza el servidor comunitario
[`Taxuspt/garmin_mcp`](https://github.com/Taxuspt/garmin_mcp). No es una API
oficial de Garmin y entra a Garmin Connect con una biblioteca no oficial. Para
una aplicación multiusuario o comercial, usa el
[Garmin Connect Developer Program](https://developer.garmin.com/gc-developer-program/):
sus APIs oficiales cubren salud, actividades y publicación de entrenamientos.

## 1. Autenticación local

Instala `uv`, abre tu propia terminal y ejecuta la versión revisada y fijada:

```bash
uvx --python 3.12 \
  --from git+https://github.com/Taxuspt/garmin_mcp@e8554bcd761a4494dc12a98461224bb3dcf1fbc5 \
  garmin-mcp-auth
```

Escribe ahí tu correo, contraseña y MFA. No los pegues en el chat, un archivo del
proyecto, una variable persistente ni la configuración MCP.

El proceso crea tokens en `~/.garminconnect`. Confirma permisos:

```bash
chmod 700 ~/.garminconnect
chmod 600 ~/.garminconnect/*
```

## 2. Conectar el cliente

Después de autenticar, copia y adapta uno de estos ejemplos:

- `mcp/codex.example.toml`
- `mcp/claude-desktop.example.json`

Ambos fijan el commit revisado, omiten correo/contraseña y activan una lista de
herramientas de solo lectura. Reinicia el cliente después del cambio.

## 3. Primera consulta

Comprueba primero que el perfil sea válido y pide una evaluación, no un plan
agresivo:

```text
Lee mi perfil. Consulta los últimos 28 días mediante Garmin. Separa datos
medidos, declarados, estimados e inferidos. Resume línea base, datos faltantes y
riesgos antes de proponer una primera semana conservadora.
```

## Herramientas de escritura

La lista de lectura no permite crear ni borrar entrenamientos. Si una persona
decide habilitar escritura, debe hacerlo después, para herramientas concretas,
y exigir una vista previa y confirmación por cada cambio. No habilites las más
de 110 herramientas por defecto solo por comodidad.

## Escala multiusuario

No uses contraseñas de clientes ni copies tokens entre personas. Para un
producto, la arquitectura correcta es consentimiento individual y OAuth 2.0
mediante las APIs oficiales. Garmin describe Health API para métricas como
sueño, pasos, pulso y estrés, Activity API para actividades y Training API para
enviar planes a dispositivos.
