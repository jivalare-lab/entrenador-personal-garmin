# Seguridad

## Respuesta corta sobre la contraseña de Garmin

En el flujo interactivo revisado, la contraseña se pide con entrada oculta y no
se escribe en los archivos del proyecto. Se usa para iniciar sesión por HTTPS y
el servidor comunitario guarda tokens de sesión en `~/.garminconnect` con
permisos exclusivos del usuario.

Eso reduce el riesgo, pero no equivale a OAuth oficial: estás confiando tu clave
momentáneamente a código comunitario y a sus dependencias. El commit revisado por
este proyecto es `e8554bcd761a4494dc12a98461224bb3dcf1fbc5`; fijarlo evita que una
actualización futura se ejecute sin revisión.

## Hallazgos importantes

- La contraseña no debe aparecer en `config.toml`, JSON, `.env`, historial del
  shell, argumentos, chat, GitHub Actions ni repositorios.
- Los tokens son credenciales reutilizables: quien los copie puede acceder a la
  cuenta. Nunca compartas `~/.garminconnect`.
- El autenticador revisado también puede crear `~/.garminconnect_base64`.
  Base64 es otra representación del token, no cifrado. Trátalo como secreto y
  elimínalo si confirmas que ningún despliegue tuyo lo necesita.
- El servidor registra más de 110 herramientas si no se filtra. Los ejemplos de
  este repo usan `GARMIN_ENABLED_TOOLS` para exponer únicamente lecturas útiles.
- Activa MFA en Garmin y usa una contraseña única.

## Comprobación local sin revelar valores

```bash
stat -f '%Sp %N' ~/.garminconnect ~/.garminconnect/*  # macOS
# o
stat -c '%A %n' ~/.garminconnect ~/.garminconnect/*   # Linux
```

La carpeta debe ser `drwx------` (700) y los archivos `-rw-------` (600).

## Qué no contiene este repositorio

- contraseñas, tokens, cookies o archivos de sesión;
- exportaciones Garmin ni datos de salud reales;
- el perfil privado `profile/athlete.toml`;
- credenciales de Telegram u otros servicios.

Reporta fallos de seguridad en privado al propietario del repositorio. No abras
un issue que contenga credenciales o datos de salud.
