## 🤖 Bot TikTok-Discord Automatisé

Bot qui **commente les vidéos TikTok** avec des hashtags personnalisés, contrôlé via Discord avec un **panel de gestion des commentaires**.

### ✨ Fonctionnalités

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

### 3️⃣ Configurer le token Discord
```bash
# Éditer le fichier .env
nano .env
```

Ajoute ton **Discord Token**:
```env
DISCORD_TOKEN=ton_token_ici
```

**Comment obtenir le token?**
1. Va sur https://discord.com/developers/applications
2. Crée une nouvelle application
3. Va dans "Bot" et clique "Add Bot"
4. Copie le token

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
Commenter les vidéos avec un hashtag (une seule fois)

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

## 📝 Format des Hashtags

Les hashtags sont **automatiquement convertis en minuscules continus**:

| Entrée | Conversion |
|--------|----------|
| `#MayotteIslande` | `#mayotteislande` |
| `#PourToi` | `#pourtoi` |
| `#Viral Island` | `#viralislande` |

---

## ⚙️ Exemple d'Utilisation

### Étape 1: Configurer les commentaires
```
/panel
```
Voit la liste des commentaires actuels

```
/ajouter_com Bv Bh
/ajouter_com C'est fou!
/ajouter_com Top du top
/lister_com
```

### Étape 2: Configurer les hashtags
```
/configurer #mayotteislande #pourtoi #parati #viral
```

### Étape 3: Lancer le bot
```
/commente #mayotteislande 5
```

Ou en mode automatique:
```
/automatique 120
```

---

## 📁 Fichiers de Configuration

### `commentaires.json`
Stocke les commentaires personnalisés. Format:
```json
{
  "default": [
    "🔥 Excellent!",
    "Bv Bh",
    "C'est fou!"
  ]
}
```

### `.env`
Stocke le token Discord:
```env
DISCORD_TOKEN=ton_token_ici
```

---

## 🐛 Dépannage

### ❌ "DISCORD_TOKEN non trouvé"
```bash
# Vérifie que .env existe et contient le token
cat .env
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
- Vérifie que tu es **connecté à TikTok** dans le navigateur
- Attends que les vidéos **se chargent complètement**
- Vérifies les **sélecteurs CSS** (peuvent changer)
- Utilise `/lister_com` pour vérifier que tes commentaires sont bien ajoutés

### ⚠️ "Aucun commentaire configuré"
```bash
# Réinitialise les commentaires par défaut
/reset_com
```

---

## 📦 Dépendances

- `discord.py` - Bot Discord
- `selenium` - Web scraping TikTok
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

## ⚖️ Avertissement

⚠️ **Utilise ce bot responsablement:**
- Respecte les conditions d'utilisation de TikTok
- Ne spam pas les commentaires
- Évite les compte bans
- Utilise des délais appropriés entre commentaires
- Les commentaires trop similaires peuvent être bloqués

---

## 📞 Support

Si tu as des problèmes:
1. Utilise `/aide` pour voir toutes les commandes
2. Vérifies les logs du bot
3. Réinstalle les dépendances
4. Crée une issue sur GitHub

---

**Bon spam responsable! 🚀**
