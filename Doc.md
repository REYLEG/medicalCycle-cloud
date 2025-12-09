# 📘 Documentation — MediNexus Cloud

## 1. Contexte et objectif
MediNexus Cloud est conçu pour démontrer une application concrète des systèmes distribués : un service cloud médical qui doit être scalable, fault-tolerant et collaboratif.

---

## 2. Cas d’usage principaux
1. Création / consultation / mise à jour de dossiers patients.  
2. Partage sécurisé d’un dossier entre établissements (ex : transfert d’un patient).  
3. Alertes et rappels (rendez-vous, vaccins).  
4. Collaboration (commentaires, notes partagées entre professionnels).

---

## 3. Architecture détaillée (proposée)

### 3.1 Schéma logique (résumé)
- Load Balancer → répartit la charge sur plusieurs instances backend.  
- Instances backend (API) → exposent des endpoints REST/GraphQL.  
- Base de données distribuée → réplication master/replica ou cluster (Postgres cluster / MongoDB replica set).  
- Stockage objet → pour documents et images (S3 / équivalent).  
- Service de notifications → envoi d’emails / SMS / push.  
- Sauvegardes régulières et monitoring (Prometheus / Grafana).

### 3.2 Scalabilité
- Auto-scaling des instances backend en fonction de métriques (CPU, requêtes/s).  
- Partitionnement horizontal pour la base de données si besoin (sharding).

### 3.3 Tolérance aux pannes
- Réplication des données entre régions/zones.  
- Backups périodiques et procédure de restauration documentée.  
- Tests réguliers de basculement (DR drills).

### 3.4 Collaboration & cohérence
- Contrôle de concurrence optimiste (versioning des dossiers) pour gérer modifications simultanées.  
- Journalisation des modifications (audit trail).

---

## 4. Sécurité
- Authentification : OAuth2 / JWT.  
- Autorisation : RBAC (Role Based Access Control).  
- Chiffrement au repos et en transit.  
- Politique de confidentialité et conformité locale (expliquer loi locale si nécessaire).

---

## 5. Déploiement minimum viable (MVP) — plan 48h (simulation)
Objectif du MVP : prouver le concept (documentation + prototype minimal).  
Tâches prioritaires :
1. Rédiger README & DOC (fait).  
2. Démonstration fonctionnelle minimale : maquette d’interface (images) ou endpoints décrits.  
3. Diagramme architecture et explication de scalabilité / tolérance.  
4. Préparer présentation / capture d’écran à joindre.

---

## 6. Évolution future
- Remplacer le prototype par un backend réel (API + database).  
- Ajouter authentification forte et chiffrement avancé.  
- Intégration mobile & offline sync.

---

## 7. Références
- Tanenbaum & Van Steen — Distributed Systems (concepts).  
- Docs officielles : PostgreSQL, MongoDB Atlas, AWS S3, Kubernetes (pour scale & HA).