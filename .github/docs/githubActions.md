# Configuración de Secrets para Deploy en GitHub Actions

Este documento describe los secrets necesarios para ejecutar correctamente el workflow de despliegue de `google-places-api` hacia el servidor de producción desde GitHub Actions.

## Ubicación

En GitHub:

1. Ir al repositorio `google-places-api`.
2. Seleccionar **Settings**.
3. Ir a **Secrets and variables** → **Actions**.
4. Crear los siguientes Repository Secrets.

---

## Secrets requeridos

### SSH_HOST

IP o dominio del servidor de producción donde se encuentra GoMarket.

**Ejemplo:**

```text
167.99.xxx.xxx
```

No incluir `http://` ni `https://`.

---

### SSH_USER

Usuario SSH utilizado para conectarse al servidor.

**Ejemplo:**

```text
root
```

---

### SSH_PRIVATE_KEY

Clave privada SSH utilizada por GitHub Actions para acceder al servidor.

Se recomienda utilizar una clave dedicada para el deploy.

Por ejemplo:

```bash
ssh-keygen -t ed25519 \
  -C "github-actions-google-places-api" \
  -f ~/.ssh/google_places_deploy
```

Esto genera:

```text
~/.ssh/google_places_deploy
~/.ssh/google_places_deploy.pub
```

La clave pública debe agregarse al servidor:

```text
~/.ssh/authorized_keys
```

La clave privada puede visualizarse localmente con:

```bash
cat ~/.ssh/google_places_deploy
```

Copiar el contenido completo:

```text
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

y guardarlo como valor del secret:

```text
SSH_PRIVATE_KEY
```

Nunca guardar la clave privada dentro del repositorio.

---

## Secrets requeridos para el deploy actual

El workflow utiliza:

```text
SSH_HOST
SSH_USER
SSH_PRIVATE_KEY
```

No es necesario configurar `BLUDCODE_VUE_UI_SSH_KEY`, ya que este proyecto no instala el paquete privado `@bludcode/vue-ui`.

La API Key de Google Places tampoco debe almacenarse como un secret SSH.

Actualmente la aplicación utiliza en el servidor:

```text
API_KEY.txt
```

Este archivo debe permanecer fuera del repositorio.

---

## Verificación de acceso SSH

Para verificar temporalmente la conexión puede agregarse al workflow:

```yaml
- name: Test SSH
  uses: appleboy/ssh-action@v1
  with:
    host: ${{ secrets.SSH_HOST }}
    username: ${{ secrets.SSH_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      whoami
      hostname
      pwd
```

Una vez verificada la conexión, este paso puede eliminarse.

---

## Uso en GitHub Actions

El deploy se realiza mediante SSH:

```yaml
- name: Deploy
  uses: appleboy/ssh-action@v1
  with:
    host: ${{ secrets.SSH_HOST }}
    username: ${{ secrets.SSH_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      set -e

      cd /var/www/googlemaps_backend/google-places-api

      git pull origin main

      source /var/www/googlemaps_backend/venv/bin/activate

      pip install -r requirements.txt

      if pm2 describe "locations.gomarket.com.uy" >/dev/null 2>&1; then
        pm2 restart "locations.gomarket.com.uy" --update-env
      else
        pm2 start api.py \
          --name "locations.gomarket.com.uy" \
          --interpreter /var/www/googlemaps_backend/venv/bin/python3
      fi

      pm2 save
```

---

## Archivos sensibles

Los siguientes archivos nunca deben ser versionados:

```text
API_KEY.txt
*.pem
```

El `.gitignore` debe contener al menos:

```gitignore
API_KEY.txt
*.pem
```

Antes de realizar un commit se puede verificar con:

```bash
git status
git ls-files | grep -E 'API_KEY|\.pem$'
```

El segundo comando idealmente no debe devolver resultados.

---

## Troubleshooting

### Error de autenticación SSH

```text
ssh: handshake failed: ssh: unable to authenticate
```

Verificar:

- `SSH_PRIVATE_KEY` contiene una clave privada válida.
- La clave pública correspondiente está en `~/.ssh/authorized_keys` del servidor.
- `SSH_USER` es correcto.
- `SSH_HOST` apunta al servidor correcto.

### Connection refused

```text
connect: connection refused
```

Verificar que SSH esté funcionando en el servidor y que el host y puerto sean correctos.

### El microservicio no está ejecutándose

Verificar:

```bash
pm2 list
```

Debe aparecer:

```text
locations.gomarket.com.uy
```

También puede verificarse el puerto:

```bash
sudo lsof -i :5000
```

### Verificar el endpoint directamente

Desde el servidor:

```bash
curl -i "http://127.0.0.1:5000/locations/v1/api/bars/near?latitude=-34.8763&longitude=-56.0948"
```

Esto permite comprobar Flask sin pasar por Nginx.

---

## Resumen

| Secret | Descripción |
|---|---|
| `SSH_HOST` | Host/IP del servidor de producción |
| `SSH_USER` | Usuario SSH utilizado para el deploy |
| `SSH_PRIVATE_KEY` | Clave privada utilizada por GitHub Actions |