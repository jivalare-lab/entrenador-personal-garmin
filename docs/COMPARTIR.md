# Cómo compartir el proyecto

La opción recomendada es un repositorio privado de GitHub.

1. Envía a la otra persona el enlace del repositorio.
2. Añádela como colaboradora por su usuario de GitHub.
3. La persona clona el proyecto y crea `profile/athlete.toml` desde el ejemplo.
4. La persona autentica su propia cuenta Garmin en su propia computadora.
5. Nadie envía contraseñas, tokens ni exportaciones por correo o chat.

Antes de cualquier push ejecuta:

```bash
git status --short
git ls-files | grep -E '(athlete\.toml|\.env|garminconnect|\.log)$' && exit 1 || true
python3 scripts/validate_profile.py profile/athlete.example.toml
python3 -m unittest discover -s tests -v
```

Para convertirlo en producto multiusuario no reutilices este inicio de sesión
personal. Solicita acceso al programa oficial de Garmin y diseña consentimiento,
revocación, retención y eliminación de datos por usuario.
