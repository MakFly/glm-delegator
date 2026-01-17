# Guide d'Utilisation - LLM Delegator

Guide complet pour utiliser les experts LLM spécialisés avec Claude Code.

## Table des Matières

- [Démarrage Rapide](#démarrage-rapide)
- [Utilisation Quotidienne](#utilisation-quotidienne)
- [Scénarios d'Usage](#scénarios-dusage)
- [Bonne Pratiques](#bonne-pratiques)
- [Résolution de Problèmes](#résolution-de-problèmes)

---

## Démarrage Rapide

### 1. Vérifier l'Installation

Une fois configuré, redémarrez Claude Code et vérifiez que les outils MCP sont disponibles :

```bash
# Les outils devraient apparaître sous la forme :
mcp__glm-delegator__glm_architect
mcp__glm-delegator__glm_code_reviewer
mcp__glm-delegator__glm_security_analyst
mcp__glm-delegator__glm_plan_reviewer
mcp__glm-delegator__glm_scope_analyst
```

### 2. Premier Test

Posez une question simple pour tester :

```
"Peux-tu demander à l'architecte d'analyser la structure de ce projet ?"
```

Si l'expert répond, l'installation est réussie !

---

## Utilisation Quotidienne

### Délégation Automatique

Claude détecte automatiquement quand déléguer basé sur votre requête. Aucune action spéciale n'est requise.

**Exemples de déclencheurs automatiques :**

| Votre requête | Expert sollicité |
|---------------|------------------|
| "Est-ce que cette authentification est sécurisée ?" | Security Analyst |
| "Quelle est la meilleure architecture pour ce feature ?" | Architect |
| "Peux-tu relire ce code et trouver les bugs ?" | Code Reviewer |
| "Review ce plan de migration" | Plan Reviewer |
| "Qu'est-ce que j'ai oublié dans ces specs ?" | Scope Analyst |

### Délégation Explicite

Vous pouvez aussi demander explicitement un expert :

```
"Ask the architect to design a caching strategy"
"Use the code reviewer to analyze this function"
"Have the security analyst check this endpoint"
```

### Appel Direct des Outils MCP

Pour un contrôle total, appelez les outils directement :

```javascript
// Mode Advisory (analyse seulement)
mcp__glm-delegator__glm_architect({
  task: "Compare Redis vs Memcached for session storage",
  mode: "advisory",
  context: "Building a Node.js microservice with 10k concurrent users"
})

// Mode Implementation (applique les changements)
mcp__glm-delegator__glm_code_reviewer({
  task: "Fix the race condition in the user registration flow",
  mode: "implementation",
  files: ["src/auth/register.ts"]
})
```

---

## Scénarios d'Usage

### Scénario 1 : Design d'Architecture

**Situation** : Vous concevez un nouveau système de notifications.

```
"How should I design a notification system that handles email, SMS, and push notifications?"
```

**Ce que l'Architect fera :**
1. Analyser vos besoins actuels
2. Proposer une architecture modulaire
3. Identifier les trade-offs (performance vs complexité)
4. Suggérer les patterns à utiliser

**Résultat typique :**
```
Based on your requirements, I recommend a strategy pattern:

1. NotificationChannel interface
2. Separate providers for EmailChannel, SmsChannel, PushChannel
3. A NotificationService that orchestrates sending
4. Queue-based processing for async delivery
```

### Scénario 2 : Code Review Multilingue

**Situation** : Vous voulez une review en français.

```
"Peux-tu faire une review complète de ce fichier src/auth/login.ts ?"
```

**Le Code Reviewer analysera :**
- Bugs potentiels
- Problèmes de performance
- Erreurs de logique
- Style et lisibilité
- Vulnérabilités de sécurité

**Support des langues :**
- Anglais (EN)
- Français (FR)
- Chinois (CN/中文)

### Scénario 3 : Analyse de Sécurité

**Situation** : Vous avez un endpoint d'upload de fichiers.

```
"Is this file upload endpoint secure? Could you check for vulnerabilities?"
```

**Le Security Analyst vérifiera :**
- Injection de fichiers malveillants
- Path traversal
- Limitation de taille
- Validation des types MIME
- Stockage sécurisé
- Vulnérabilités OWASP Top 10

### Scénario 4 : Validation de Plan

**Situation** : Avant une refactorisation majeure.

```
"Review this migration plan: I'm planning to move from Redux to Zustand"
```

**Le Plan Reviewer évaluera :**
- Complétude du plan
- Risques potentiels
- Étapes manquantes
- Ordre logique des opérations
- Plan de rollback

### Scénario 5 : Analyse de Scope

**Situation** : Les specs sont floues.

```
"I need to add 'user preferences' but I'm not sure what that should include"
```

**Le Scope Analyst aidera à :**
- Clarifier les exigences
- Identifier les fonctionnalités manquantes
- Poser les bonnes questions
- Définir les limites du scope

---

## Bonne Pratiques

### 1. Fournir du Contexte

Plus vous donnez de contexte, meilleure sera la réponse :

```
// Bien
"Ask the architect to design a database schema"

// Mieux
"Ask the architect to design a PostgreSQL schema for an e-commerce platform
with 100k products, 1M users, and heavy read traffic. We need to support
inventory management, order history, and product search."
```

### 2. Spécifier le Mode quand Nécessaire

```
// Pour une analyse sans modifications
mcp__glm-delegator__glm_code_reviewer({
  task: "Analyze the authentication flow for security issues",
  mode: "advisory"  // Lecture seule
})

// Pour appliquer des corrections
mcp__glm-delegator__glm_code_reviewer({
  task: "Fix the identified security vulnerabilities",
  mode: "implementation"  // Modifie les fichiers
})
```

### 3. Combiner les Experts

Pour des tâches complexes, sollicitez plusieurs experts :

```
"First, ask the scope analyst to clarify the requirements for the new feature,
then have the architect design the implementation approach,
and finally use the code reviewer to validate the implementation."
```

### 4. Itérer

N'hésitez pas à raffiner vos demandes :

```
"That's a good start. Now ask the security analyst to specifically check
for SQL injection vulnerabilities in the queries."
```

### 5. Vérifier les Recommandations

Les experts donnent des conseils, mais vous devriez toujours :

- Lire et comprendre les changements proposés
- Tester après implémentation
- Ajuster selon vos besoins spécifiques

---

## Résolution de Problèmes

### Les outils MCP n'apparaissent pas

**Symptôme** : Les outils `mcp__glm-delegator__*` ne sont pas disponibles.

**Solutions :**

1. Vérifiez la configuration dans `~/.claude.json` :
```bash
cat ~/.claude.json | grep -A 10 "glm-delegator"
```

2. Vérifiez que le chemin vers `glm_mcp_server.py` est correct :
```bash
ls -la /path/to/glm-delegator/glm_mcp_server.py
```

3. Redémarrez complètement Claude Code

4. Testez le serveur MCP manuellement :
```bash
python3 /path/to/glm-delegator/glm_mcp_server.py --debug
```

### Erreur d'authentification

**Symptôme** : "Authentication failed" ou "401 Unauthorized"

**Solutions :**

1. Vérifiez que la clé API est définie :
```bash
echo $GLM_API_KEY  # ou $ANTHROPIC_API_KEY, $OPENAI_API_KEY
```

2. Vérifiez que la clé est valide et active

3. Pour Z.AI, assurez-vous d'utiliser la bonne clé :
```bash
export GLM_API_KEY="your_actual_z_ai_key"
```

### Réponses vides ou incomplètes

**Symptôme** : L'expert répond très brièvement ou ne semble pas comprendre.

**Solutions :**

1. Augmentez `max-tokens` dans la configuration :
```json
"--max-tokens", "16384"
```

2. Soyez plus spécifique dans votre requête :
```
// Moins efficace
"Review this code"

// Plus efficace
"Review this authentication code for SQL injection vulnerabilities,
XSS risks, and session management issues. Focus on the login function."
```

3. Ajoutez plus de contexte sur votre projet

### Timeout

**Symptôme** : La requête expire après un certain temps.

**Solutions :**

1. Augmentez le timeout :
```json
"--timeout", "1200"  // 20 minutes au lieu de 10
```

2. Simplifiez la tâche (divisez-la en plus petites parties)

3. Vérifiez votre connexion internet

### Le mauvais expert est sélectionné

**Symptôme** : Claude sollicite le Security Analyst alors que vous vouliez l'Architect.

**Solution** : Soyez plus explicite :
```
"Ask the ARCHITECT (not the security analyst) to design the database schema"
```

Ou appelez l'outil directement :
```javascript
mcp__glm-delegator__glm_architect({
  task: "Design the database schema",
  mode: "advisory"
})
```

---

## Configuration Avancée

### Utiliser Plusieurs Providers

Vous pouvez configurer plusieurs experts avec différents providers :

```json
{
  "mcpServers": {
    "claude-architect": {
      "command": "python3",
      "args": ["~/glm-delegator/glm_mcp_server.py",
               "--provider", "anthropic-compatible",
               "--model", "claude-sonnet-4-20250514"]
    },
    "ollama-reviewer": {
      "command": "python3",
      "args": ["~/glm-delegator/glm_mcp_server.py",
               "--provider", "openai-compatible",
               "--base-url", "http://localhost:11434/v1",
               "--model", "llama3.1"]
    }
  }
}
```

### Personnaliser les Prompts d'Experts

Les prompts des experts sont définis dans `glm_mcp_server.py`. Pour les personnaliser :

1. Éditez le fichier
2. Modifiez les variables `SYSTEM_PROMPTS`
3. Redémarrez Claude Code

### Activer le Debug

Pour voir les requêtes et réponses brutes :

```json
"--debug"
```

Cela affichera dans les logs :
- Requêtes envoyées à l'API
- Réponses brutes du LLM
- Temps de réponse

---

## Exemples de Workflows

### Workflow 1 : Nouveau Feature

```
1. "Ask the scope analyst to define requirements for user notifications"
2. "Have the architect design the notification system architecture"
3. "Implement the notification service"
4. "Use the code reviewer to validate the implementation"
5. "Ask the security analyst to check for vulnerabilities"
```

### Workflow 2 : Bug Fix

```
1. "Analyze this bug: users are getting logged out randomly"
2. "Have the code reviewer find the root cause in the session management"
3. "Fix the identified issue"
4. "Ask the security analyst to verify the fix is secure"
```

### Workflow 3 : Refactorisation

```
1. "Review my plan to refactor the auth system"
2. "Have the architect validate the new architecture"
3. "Implement the refactor"
4. "Use the code reviewer to ensure no regressions"
```

---

## Ressources Supplémentaires

- [README.md](README.md) - Documentation principale
- [BACKEND_CONFIG.md](BACKEND_CONFIG.md) - Configuration des providers
- [CLAUDE.md](CLAUDE.md) - Guide pour les développeurs
- [Issues GitHub](https://github.com/MakFly/glm-delegator/issues) - Signaler des problèmes

---

## Support

Pour toute question ou problème :

1. Consultez ce guide d'utilisation
2. Vérifiez la section [Résolution de Problèmes](#résolution-de-problèmes)
3. Ouvrez une issue sur GitHub avec les détails du problème
4. Activez le mode `--debug` et incluez les logs dans votre rapport
