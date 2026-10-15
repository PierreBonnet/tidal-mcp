# tidal-mcp

[![Soutenir sur Ko-fi](https://img.shields.io/badge/Ko--fi-Soutenir%20le%20projet-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/pierrobn)
Community derivative of [sickn33/tidal-mcp](https://github.com/sickn33/tidal-mcp), prepared for public source distribution. The upstream MIT license and required attribution are retained. This repository starts with a fresh Git history.

## Install and run

Requires Python 3.11–3.13.

```sh
python -m venv .venv
# Activate .venv using the command appropriate to your shell.
python -m pip install -e .
python -m pip install pytest
python -m pytest
tidal-auth
tidal-mcp
```

Configure your MCP client to launch the installed `tidal-mcp` executable over stdio. Run `tidal-auth` interactively once to authorize your own account. The session is stored in the platform user-data directory. Optional local settings: `TIDAL_MCP_DATA_DIR`, `TIDAL_MCP_SESSION_FILE`, `TIDAL_MCP_DRAFT_TTL_SECONDS` (60–3600). Writes are disabled by default; enable them with `TIDAL_MCP_ENABLE_WRITES=true`. Mutations require the preview/commit approval flow.

## Privacy

No account configuration, OAuth sessions, personal exports, or local Git history are distributed. Examples and tests use fixtures. Never commit your local credentials or session files. Runtime tools can return information from the account you connect; review outputs before sharing them.

## Changes in this derivative

Authentication and logout success messages omit local filesystem paths and account identifiers. Regression tests verify that successful authentication does not print these values.

Only GitHub source distribution is configured; this derivative is not published to npm or PyPI.

On Windows, local session confidentiality relies on the ACLs of your user-data directory; POSIX mode bits do not enforce owner-only access there. Keep custom storage directories private.

## Claude et ChatGPT

| Client | Connexion proposée |
| --- | --- |
| Claude Desktop | Serveur local MCP sur stdio, configuration ci-dessous |
| Claude Code | Même commande locale, via `claude mcp add` |
| ChatGPT | Serveur local relié par Secure MCP Tunnel, sous réserve d'accès à cette fonction |
| Claude web / mobile | Non fourni ici : exige un serveur MCP distant accessible en HTTPS |

Le dépôt GitHub contient le code, pas un endpoint MCP hébergé. Les tests vérifient l'initialisation et la découverte des outils sur stdio ; ils ne constituent pas une connexion réelle à ton compte Claude ou ChatGPT.

### Claude Desktop

Installe d'abord le projet avec les commandes ci-dessus. Ouvre la configuration MCP de Claude Desktop (`claude_desktop_config.json`) et fusionne cette entrée avec tes serveurs existants :

```json
{
  "mcpServers": {
    "tidal-mcp": {
      "command": "C:/mcp/tidal-mcp/.venv/Scripts/python.exe",
      "args": [
        "-m",
        "tidal_mcp"
      ],
      "env": {
        "TIDAL_MCP_ENABLE_WRITES": "false"
      }
    }
  }
}
```

Un [fichier exemple](examples/claude_desktop_config.example.json) est fourni. Remplace les chemins génériques et les valeurs `REPLACE_…` uniquement dans ta configuration privée. Sous macOS/Linux, utilise le chemin absolu du dépôt et `.venv/bin/python` à la place de `.venv/Scripts/python.exe`. Pour Steam, utilise le chemin absolu de Node si Claude ne le trouve pas. Aucun terminal interactif ne doit être nécessaire au démarrage. Redémarre Claude après modification.

### Claude Code

Après avoir défini les mêmes variables d'environnement dans ton terminal, enregistre la commande avec une portée utilisateur :

```sh
claude mcp add --transport stdio --scope user tidal-mcp -- "C:/mcp/tidal-mcp/.venv/Scripts/python.exe" "-m" "tidal_mcp"
```

Adapte les chemins à ton système ; consulte `claude mcp list`, puis `/mcp` dans Claude Code pour vérifier la connexion. Les secrets du terminal doivent être disponibles lors des lancements suivants ; une configuration d'environnement privée persistante peut être nécessaire.

### ChatGPT — tunnel privé

Installe [tunnel-client](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels), crée un tunnel autorisé pour ton espace et définis localement `CONTROL_PLANE_API_KEY`, ainsi que les variables du serveur.

```sh
tunnel-client init --sample sample_mcp_stdio_local --profile tidal-mcp --tunnel-id REPLACE_WITH_TUNNEL_ID --mcp-command "C:/mcp/tidal-mcp/.venv/Scripts/tidal-mcp.exe"
tunnel-client doctor --profile tidal-mcp --explain
tunnel-client run --profile tidal-mcp
```

Garde ce processus ouvert. Dans ChatGPT : **Plugins → Ajouter un serveur MCP personnalisé → Tunnel**, sélectionne ce tunnel, puis installe le plugin. Ce serveur local ne fournit pas OAuth côté MCP : choisis « Sans authentification » pour cette connexion privée protégée par les droits du tunnel. L'authentification du service reste locale. L'accès dépend des permissions de ton organisation/espace. [Guide officiel](https://developers.openai.com/api/docs/guides/custom-mcp-server).

Les commandes ci-dessus supposent des chemins sans espaces pour la commande encapsulée par le tunnel. Adapte-les ou configure le lancement selon l'aide de `tunnel-client`. Sous macOS/Linux, remplace l'exécutable Python installé par `.venv/bin/tidal-mcp`. Le tunnel donne accès au compte configuré sur cette machine : réserve-le à ton espace de confiance. Il ne transforme pas ce serveur personnel en service multi-utilisateur.

### Session et authentification

Exécute `tidal-auth` dans le même environnement et sous le même utilisateur que le serveur. Vérifie avec `tidal-auth --status`. Pour déconnecter : `tidal-auth --logout --yes`. Garde le fichier de session hors du dépôt. Les écritures restent désactivées ; si tu les actives, chaque action nécessite un aperçu puis ta confirmation.

### Vérification et dépannage

Essaie : « Vérifie mon authentification TIDAL avec tidal_auth_status. » Les résultats des outils et ressources peuvent contenir des données de ton compte ; le client qui les consulte les reçoit. Si le serveur ne démarre pas, vérifie les chemins absolus, l'installation des dépendances et les variables d'environnement. Si ChatGPT ne propose pas ton tunnel, vérifie ses droits et son rattachement à l'espace. Ne renseigne pas l'URL GitHub comme URL de serveur MCP.

Références : [Claude local](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop), [Claude Code MCP](https://code.claude.com/docs/en/mcp), [connecteurs Claude distants](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp). Documentation vérifiée le 10 octobre 2026.

## Soutenir le projet

Si ce serveur MCP vous est utile, vous pouvez soutenir son développement et sa maintenance avec un don facultatif sur [Ko-fi](https://ko-fi.com/pierrobn). Merci pour votre soutien !
