## 🤖 Bot TikTok-Discord Automatisé - AVEC CONNEXION AUTOMATIQUE

Bot qui **commente les vidéos TikTok** avec des hashtags personnalisés, contrôlé via Discord avec un **panel de gestion des commentaires** et **connexion automatique au compte TikTok**.

### ✨ Fonctionnalités

✅ **Connexion automatique** au compte TikTok  
✅ Commente les vidéos TikTok automatiquement  
✅ Contrôle via commandes Discord  
✅ **Panel de gestion des commentaires** (ajouter/supprimer)  
✅ Hashtags en **minuscules continus** (#mayotteislande)  
✅ Commentaires aléatoires et personnalisables  
✅ Mode automatique périodique  
✅ Compatible **Termux Linux**  

---

## 📋 Installation Rapide (Termux)

### 1️⃣ Cloner le repo
```bash
cd ~
git clone https://github.com/chauferra90k-cmyk/tiktok-discord-bot.git
cd tiktok-discord-bot
```

### 2️⃣ Exécuter le script d'installation
```bash
chmod +x setup.sh
bash setup.sh
```

### 3️⃣ Configurer les identifiants

**a) Token Discord:**
```bash
nano .env
```

Ajoute tes identifiants:
```env
DISCORD_TOKEN=ton_token_discord_ici
TIKTOK_USERNAME=ton_username_tiktok
TIKTOK_PASSWORD=ton_password_tiktok
```

**Comment obtenir le Discord Token?**
1. Va sur https://discord.com/developers/applications
2. Crée une nouvelle application
3. Va dans "Bot" et clique "Add Bot"
4. Copie le token

**Comment obtenir les identifiants TikTok?**
- `TIKTOK_USERNAME` = ton username ou email TikTok
- `TIKTOK_PASSWORD` = ton mot de passe TikTok

⚠️ **Important:** Garde ces identifiants secrets!

### 4️⃣ Lancer le bot
```bash
source venv/bin/activate
python bot.py
```

---

## 🎮 Commandes Discord

### Panel & Commentaires

#### `/panel`
Affiche le panel de gestion des commentaires avec tous les options disponibles
```
/panel
```

#### `/ajouter_com <texte>`
Ajouter un nouveau commentaire personnalisé
```
/ajouter_com Bv Bh
/ajouter_com 🔥 C'est fou!
/ajouter_com Top vidéo
```

#### `/supprimer_com <numéro>`
Supprimer un commentaire par son numéro
```
/supprimer_com 1
/supprimer_com 5
```

#### `/lister_com`
Afficher la liste complète de tous les commentaires
```
/lister_com
```

#### `/reset_com`
Réinitialiser les commentaires par défaut
```
/reset_com
```

### Commentaire Automatique

#### `/commente <hashtag> [quantite]`
Commenter les vidéos avec un hashtag (une seule fois) - **Se connecte automatiquement!**

```
/commente #mayotteislande 5
/commente #pourtoi 3
/commente #viral 10
```

#### `/configurer <hashtags>`
Configure les hashtags automatiques pour le mode automatique

```
/configurer #mayotteislande #pourtoi #parati #viral
```

#### `/automatique [intervalle]`
Lance les commentaires automatiques (en secondes) qui va répéter avec les hashtags configurés

```
/automatique 120
/automatique 300
```

### Gestion du Bot

#### `/etat`
Vérifie que le bot fonctionne et affiche le nombre de commentaires disponibles

```
/etat
```

#### `/aide`
Affiche l'aide complète avec toutes les commandes

```
/aide
```

#### `/arreter`
Arrête le bot

```
/arreter
```

---

## 🔐 Connexion Automatique à TikTok

Le bot se connecte **automatiquement** à ton compte TikTok quand tu lances une commande de commentaire:

1. Lit les identifiants depuis `.env`
2. Ouvre le navigateur
3. Se connecte à TikTok
4. Commence à commenter les vidéos

**Le bot utilise les identifiants du fichier `.env`:**

```env
TIKTOK_USERNAME=mon_username
TIKTOK_PASSWORD=mon_mot_de_passe
```

---

## 📝 Format des Hashtags

Les hashtags sont **automatiquement convertis en minuscules continus**:

| Entrée | Conversion |
|--------|----------|
| `#MayotteIslande` | `#mayotteislande` |
| `#PourToi` | `#pourtoi` |
| `#Viral Island` | `#viralislande` |

---

## ⚙️ Exemple d'Utilisation Complet

### Étape 1: Configuration initiale (une seule fois)

**a) Édite `.env`:**
```bash
nano .env
```

```env
DISCORD_TOKEN=ton_token_discord
TIKTOK_USERNAME=mon_username_tiktok
TIKTOK_PASSWORD=mon_mot_de_passe_tiktok
```

**b) Sauvegarde** (Ctrl+O, Entrée, Ctrl+X)

### Étape 2: Configurer tes commentaires

```
/panel
```
Vois la liste des commentaires actuels

```
/ajouter_com Bv Bh
/ajouter_com C'est fou!
/ajouter_com Top du top
/lister_com
```

### Étape 3: Configurer les hashtags

```
/configurer #mayotteislande #pourtoi #parati #viral
```

### Étape 4: Lancer les commentaires

**Option 1 - Une seule fois:**
```
/commente #mayotteislande 5
```

**Option 2 - Mode automatique (toutes les 2 minutes):**
```
/automatique 120
```

---

## 📁 Fichiers de Configuration

### `.env`
Stocke tes identifiants. Format:
```env
DISCORD_TOKEN=discord_token_ici
TIKTOK_USERNAME=username_tiktok
TIKTOK_PASSWORD=password_tiktok
HEADLESS=true
DEBUG=false
```

**⚠️ Important:**
- Ne partage JAMAIS ce fichier
- Ajoute-le à `.gitignore` (déjà fait ✅)
- Utilise des identifiants sécurisés

### `commentaires.json`
Stocke les commentaires personnalisés:
```json
{
  "default": [
    "🔥 Excellent!",
    "Bv Bh",
    "C'est fou!"
  ]
}
```

---

## 🐛 Dépannage

### ❌ "Identifiants TikTok manquants"
```bash
# Vérifie que .env contient TIKTOK_USERNAME et TIKTOK_PASSWORD
cat .env
```

### ❌ "Connexion TikTok échouée"
- Vérifie que les identifiants sont **corrects**
- Essaie de te **connecter manuellement** sur TikTok
- Attends quelques secondes avant relancer
- TikTok peut avoir une **vérification** (résous-la manuellement d'abord)

### ❌ "DISCORD_TOKEN non trouvé"
```bash
# Édite et ajoute ton token
nano .env
```

### ❌ "Driver Selenium non trouvé"
```bash
# Réinstalle les dépendances
pip install --force-reinstall selenium webdriver-manager
```

### ❌ "Chrome/Chromium introuvable" (Termux)
```bash
# Installe Chromium
apt install -y chromium-browser
```

### ⚠️ Les commentaires ne s'envoient pas
- Vérifie que tu es **connecté à TikTok** (vérif 2FA)
- Attends que les vidéos **se chargent complètement**
- Vérifies les **sélecteurs CSS** (peuvent changer)
- Utilise `/lister_com` pour vérifier que tes commentaires sont bien ajoutés
- Essaie de **commenter manuellement** d'abord

### ⚠️ "Aucun commentaire configuré"
```bash
# Réinitialise les commentaires par défaut
/reset_com
```

---

## 📦 Dépendances

- `discord.py` - Bot Discord
- `selenium` - Automatisation TikTok
- `webdriver-manager` - Gestion du driver Chrome
- `python-dotenv` - Variables d'environnement
- `beautifulsoup4` - Parsing HTML

---

## 🚀 Utilisation en Arrière-Plan (Termux)

```bash
# Lancer en arrière-plan
nohup python bot.py > bot.log 2>&1 &

# Vérifier les logs
tail -f bot.log

# Voir les processus Python
ps aux | grep python

# Arrêter le processus
pkill -f "python bot.py"
```

---

## ⚖️ Avertissement & Responsabilité

⚠️ **Important - Utilise ce bot responsablement:**

- ✅ Respecte les conditions d'utilisation de TikTok
- ✅ Ne spam pas les commentaires
- ✅ Utilise des délais appropriés entre commentaires
- ✅ Évite les suspensions/bans de compte
- ✅ Varie les commentaires
- ⛔ Ne publie pas ce bot gratuitement
- ⛔ Les commentaires trop similaires seront bloqués
- ⛔ TikTok peut détecter l'automatisation

**Tu es responsable de l'utilisation que tu en fais!**

---

## 🔒 Sécurité

- Les identifiants sont stockés **localement** dans `.env`
- Ils ne sont **jamais** envoyés à GitHub (grâce à `.gitignore`)
- Ne partage **jamais** ton fichier `.env`
- Utilise des **mots de passe forts**

---

## 📞 Support

Si tu as des problèmes:
1. Utilise `/aide` pour voir toutes les commandes
2. Vérifies les logs du bot (`tail -f bot.log`)
3. Réinstalle les dépendances
4. Crée une issue sur GitHub

---

**Bon spam responsable! 🚀**
