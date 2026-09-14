# Production deployment

This service is deployed to the GoMarket production droplet at:

```text
/var/www/googlemaps_backend/google-places-api
```

The PM2 process is `locations.gomarket.com.uy`. Flask listens on
`127.0.0.1:5000`; Nginx proxies `/locations/v1` to that port. Flask routes are
under `/locations/v1/api/*`.

## Automated deployment

`.github/workflows/deploy-main.yml` runs only after a push to `main`. It SSHes
to production, verifies a clean `main` checkout, fast-forward pulls
`origin/main`, installs `requirements.txt`, and restarts or creates the PM2
process. It uses the existing virtual environment interpreter:

```text
/var/www/googlemaps_backend/venv/bin/python
```

The remote script uses `set -e`, so a failed command stops the deployment. PM2
state is saved after a successful restart or first start.

Required GitHub repository Actions secrets:

| Secret | Purpose |
|---|---|
| `SSH_HOST` | Production server host or IP, without `http://` or `https://` |
| `SSH_USER` | SSH user used by Actions; currently `root` |
| `SSH_PRIVATE_KEY` | Private key used for GitHub Actions → production server SSH |

Never put API keys or private keys in the repository or this document.

## SSH architecture

There are two separate SSH connections:

1. **GitHub Actions → production server:** the workflow uses the three secrets
   above to open the deployment SSH session.
2. **Production server → GitHub repository:** `git pull` uses the dedicated,
   read-only repository deploy key at `/root/.ssh/google_places_api`.

The production server’s `/root/.ssh/config` contains this project-specific
alias:

```sshconfig
Host github-google-places
  HostName github.com
  User git
  IdentityFile /root/.ssh/google_places_api
  IdentitiesOnly yes
```

The production checkout must use:

```text
git@github-google-places:mdamonte88/google-places-api.git
```

The alias is intentionally project-specific. Do not alter the generic
`Host github.com` configuration or remotes used by other GoMarket projects.
The default `/root/.ssh/id_rsa` is not used because it requires a passphrase
and cannot perform unattended pulls reliably.

Test repository SSH access on the production server with:

```bash
ssh -T git@github-google-places
git remote -v
```

Authentication should complete without a passphrase prompt. GitHub’s normal
shell-access refusal after successful authentication is expected.

## CORS

The API uses an explicit allowlist for `/locations/v1/api/*`:

- `https://gomarket.com.uy`
- `https://www.gomarket.com.uy`
- `https://localdashboard.gomarket.com.uy`
- `https://local.gomarket.com.uy`

Both production origins are retained because the apex and `www` frontend
origins are distinct browser origins. Wildcard CORS is not used, including on
the health endpoint.

## Verification

Repository state:

```bash
git status
git diff
git diff --cached
git remote -v
```

PM2 and port checks on the server:

```bash
pm2 list
pm2 describe locations.gomarket.com.uy
sudo lsof -i :5000
```

Direct Flask checks from the production server:

```bash
curl -i "http://127.0.0.1:5000/locations/v1/api/health"
curl -i "http://127.0.0.1:5000/locations/v1/api/bars/near?latitud=-34.8763&longitud=-56.0948"
```

Public Nginx checks:

```bash
curl -i "https://gomarket.com.uy/locations/v1/api/health"
curl -i "https://gomarket.com.uy/locations/v1/api/bars/near?latitud=-34.8763&longitud=-56.0948"
```

The current Flask handlers expect `latitud` and `longitud`. Requests using
`latitude` and `longitude` will be rejected as missing coordinates unless the
API is changed separately.

## Sensitive files

Never commit `API_KEY.txt`, `*.pem`, private SSH keys (including `id_rsa` and
`google_places_api`), or virtual environments (`venv/`, `venvs/`, `.venv/`).
The API key and deploy key remain server-local. Check tracked paths without
printing file contents:

```bash
git ls-files | grep -E 'API_KEY|\.pem$|google_places_api|id_rsa'
```

No output is expected.

## Troubleshooting

### SSH authentication failure

For Actions → server failures, verify `SSH_HOST`, `SSH_USER`, the matching
private key secret, and the server’s authorized key. For server → GitHub
failures, verify the read-only deploy key, permissions, alias, and remote.

### Passphrase prompts

An unattended deployment must not use a passphrase-protected key. Confirm the
production remote uses `github-google-places` and its `IdentityFile` is
`/root/.ssh/google_places_api`; do not replace the generic GitHub SSH config.

### `git pull` failure

Run `git status`, confirm the checkout is on `main`, and inspect `git remote -v`.
The workflow requires a clean working tree and a fast-forward-only update.
Resolve production-local source changes through Git before retrying.

### PM2 process missing

```bash
pm2 start api.py --name locations.gomarket.com.uy \
  --interpreter /var/www/googlemaps_backend/venv/bin/python
pm2 save
```

### Port 5000 is not listening

Check `pm2 logs locations.gomarket.com.uy`, verify the venv Python exists,
confirm server-local `API_KEY.txt` is present, and run `sudo lsof -i :5000`.

### HTTP 404

Use the `/locations/v1` Nginx prefix and Flask route suffix, such as
`/locations/v1/api/health`. Check Nginx and test the same route directly on
`127.0.0.1:5000`.

### CORS errors

Confirm the browser’s exact origin, including scheme and `www`, matches the
allowlist above. Test through Nginx and restart PM2 if an old process is still
serving an older `api.py`.
