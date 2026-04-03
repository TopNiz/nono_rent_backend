# nono_rent Backend

Système backend de gestion locative conforme à la loi française sur les baux d'habitation. Cette API permet la gestion des propriétés, locataires, baux et quittances de loyer avec génération automatique de documents PDF.

## Technologies

- **Langage**: Python 3.13
- **Framework API**: FastAPI
- **ORM**: SQLModel (SQLite)
- **Génération PDF**: ReportLab
- **Gestion des dépendances**: uv
- **Qualité de code**: ruff (linting & formatage)
- **Tests**: pytest
- **Conteneurisation**: Docker

## Installation

### Prérequis

- Python 3.13
- uv (gestionnaire de paquets Python)

### Installation locale

1. Cloner le dépôt (si non déjà fait via le monorepo):
```bash
git clone https://github.com/TopNiz/nono_rent_backend.git
```

2. Accéder au répertoire backend:
```bash
cd backend
```

3. Installer les dépendances avec uv:
```bash
uv sync
```

4. Vérifier l'installation:
```bash
uv run python -c "import fastapi; print('Installation réussie')"
```

### Variables d'environnement

Le backend utilise les variables d'environnement suivantes (à définir dans `.env`):
- `DATABASE_URL`: URL de connexion à la base de données (défaut: sqlite:///:memory:)
- `DEBUG`: Active le mode debug (true/false)

## Développement

### Démarrer le serveur de développement

```bash
uv run fastapi dev src/nono_rent_backend/main.py
```

Le serveur démarre sur http://localhost:8000 avec rechargement automatique.

### Documentation API

La documentation interactive est disponible sur:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints principaux

- **Locataires**: `/tenants/` - CRUD pour la gestion des locataires
- **Propriétaires**: `/landlords/` - CRUD pour la gestion des propriétaires
- **Propriétés**: `/properties/` - CRUD pour la gestion des biens locatifs
- **Baux**: `/leases/` - CRUD pour la gestion des contrats de location
- **Quittances**: `/receipts/` - CRUD pour la gestion des quittances de loyer
- **Génération PDF**: `/receipts/generate` - Endpoint pour générer les PDF de quittances

### Qualité de code

Ce projet suit des standards stricts de qualité de code:
- Typage statique obligatoire sur toutes les fonctions et valeurs de retour
- Formatage avec ruff (compatible Black)
- Linting avec ruff (remplace flake8, isort, etc.)
- Tests unitaires requis pour toutes les nouvelles fonctionnalités
- Gestion propre des exceptions avec des classes personnalisées

Pour vérifier la qualité du code:
```bash
uv run ruff check .
```

Pour formater le code automatiquement:
```bash
uv run ruff format .
```

### Bonnes pratiques de développement

1. **Approche TDD**: Écrire les tests avant l'implémentation
2. **Nommage explicite**: Variables, fonctions et classes en anglais, commentaires en français
3. **Documentation**: Docstrings pour toutes les fonctions publiques
4. **Gestion des erreurs**: Jamais d'exceptions silencieuses, toujours des classes personnalisées
5. **Typage fort**: Aucun type `Any`, annotations complètes requises

### Linting et formatage

Vérifier la qualité du code:
```bash
uv run ruff check .
```

Formater le code automatiquement:
```bash
uv run ruff format .
```

### Tests

Exécuter tous les tests:
```bash
uv run pytest
```

Exécuter un test spécifique:
```bash
uv run pytest tests/test_specific_file.py::test_name -x
```

## Docker

### Construction de l'image

```bash
docker build -t nono_rent_backend .
```

### Exécution avec Docker

```bash
docker run -p 8000:8000 nono_rent_backend
```

Le conteneur démarre avec la commande: `uv run fastapi run src/nono_rent_backend/main.py --host 0.0.0.0 --port 8000`

### Docker Compose

Dans le répertoire parent (monorepo), exécuter:
```bash
docker-compose up backend
```

## Déploiement

### Procédure de déploiement

1. S'assurer que les tests passent:
   ```bash
   uv run pytest
   ```

2. Construire l'image Docker:
   ```bash
   docker build -t nono_rent_backend:latest .
   ```

3. Pousser l'image vers le registre:
   ```bash
   docker push nono_rent_backend:latest
   ```

4. Déployer sur l'environnement cible:
   ```bash
   docker run -d -p 8000:8000 --name nono_rent_backend nono_rent_backend:latest
   ```

### Variables d'environnement en production

En production, configurez ces variables d'environnement:
```bash
DATABASE_URL=sqlite:///./data/database.db
DEBUG=false
```

### Sauvegarde des données

Les données sont stockées dans le fichier SQLite spécifié par `DATABASE_URL`. 
Pour sauvegarder:
```bash
cp ./data/database.db ./backups/database_$(date +%Y%m%d_%H%M%S).db
```

## Structure du projet

```
backend/
├── Dockerfile                  # Configuration Docker
├── pyproject.toml             # Dépendances et métadonnées
├── src/
│   └── nono_rent_backend/      # Code source principal
│       ├── main.py            # Point d'entrée de l'application
│       ├── api/               # Routeurs FastAPI
│       │   └── routers/       # Endpoints individuels (tenants, properties, leases, receipts)
│       ├── models/            # Modèles de données SQLModel (Tenant, Property, Lease, Receipt)
│       ├── services/          # Logique métier (calculs de quittances, gestion de baux)
│       └── database.py        # Configuration de la base de données (SQLite/SQLModel)
└── tests/                     # Tests unitaires et d'intégration
    ├── test_api.py           # Tests d'intégration de l'API complète
    ├── test_tenant.py        # Tests unitaires pour les locataires
    ├── test_property.py      # Tests unitaires pour les propriétés
    ├── test_lease.py         # Tests unitaires pour les baux
    ├── test_quittance.py     # Tests unitaires pour les quittances
    ├── test_landlord.py      # Tests unitaires pour les propriétaires
    ├── test_lease_service.py # Tests unitaires pour les services de bail
    └── test_quittance_service.py # Tests unitaires pour les services de quittance
```

## Contribution

Les contributions sont les bienvenues ! Voici le processus recommandé :

1. Fork le dépôt
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalité`)
3. Effectuez vos modifications
4. Ajoutez des tests pour couvrir vos changements
5. Vérifiez la qualité du code : `uv run ruff check .` et `uv run ruff format .`
6. Exécutez les tests : `uv run pytest`
7. Committez vos changements (`git commit -m 'feat: ajouter ma fonctionnalité'`)
8. Poussez la branche (`git push origin feature/ma-fonctionnalité`)
9. Ouvrez une Pull Request

### Convention de commits

Ce projet suit la convention des commits sémantiques :
- `feat:` pour une nouvelle fonctionnalité
- `fix:` pour une correction de bug
- `docs:` pour les mises à jour de documentation
- `style:` pour les changements qui n'affectent pas le sens du code
- `refactor:` pour un refactoring de code
- `test:` pour l'ajout ou la modification de tests
- `chore:` pour les mises à jour de maintenance

### Processus de revue

Toutes les Pull Requests doivent :
1. Passer tous les tests existants
2. Avoir une couverture de test adéquate
3. Suivre les standards de qualité du code
4. Être revues par au moins un autre développeur

## Maintenance

### Mise à jour des dépendances

```bash
uv sync --upgrade
```

### Vérification des vulnérabilités

```bash
uv pip audit
```

### Logs

Les logs sont disponibles via:
```bash
docker logs nono_rent_backend
```

### Sauvegarde des données

Les données sont stockées dans le fichier SQLite spécifié par `DATABASE_URL`. 
Pour sauvegarder:
```bash
cp ./data/database.db ./backups/database_$(date +%Y%m%d_%H%M%S).db
```

### Surveillance

Surveillance basique du service:
```bash
curl -f http://localhost:8000/health || echo "Service non disponible"
```

## Dépannage

### Problèmes courants

1. **ImportError: No module named 'fastapi'**
   - Solution: Réinstaller les dépendances avec `uv sync`

2. **Erreur de connexion à la base de données**
   - Vérifier la variable d'environnement DATABASE_URL
   - S'assurer que le répertoire de la base existe et est accessible

3. **Échec des tests**
   - Exécuter avec verbosité: `uv run pytest -v`
   - Vérifier les prérequis système

### Support

Pour toute question technique, consulter le fichier CONTRIBUTING.md ou ouvrir une issue sur GitHub.

---

*Pourquoi les développeurs préfèrent-ils vivre dans le Nord ? Parce que dans le Sud, il y a trop de soleil pour coder tranquillement ! 😄*