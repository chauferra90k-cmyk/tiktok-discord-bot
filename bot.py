import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from tiktok_handler import TikTokBot
import asyncio
import json

load_dotenv()

# Configuration du bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Instancier le gestionnaire TikTok
tiktok_bot = TikTokBot()

# Fichier de configuration des commentaires
CONFIG_FILE = "commentaires.json"

def charger_commentaires():
    """Charger les commentaires depuis le fichier JSON"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "default": [
                    "🔥 Excellent!",
                    "😂 Trop drôle!",
                    "👍 J'adore!",
                    "❤️ Magnifique!",
                    "✨ Incroyable!",
                ]
            }
    return {
        "default": [
            "🔥 Excellent!",
            "😂 Trop drôle!",
            "👍 J'adore!",
            "❤️ Magnifique!",
            "✨ Incroyable!",
        ]
    }

def sauvegarder_commentaires(commentaires):
    """Sauvegarder les commentaires dans le fichier JSON"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(commentaires, f, ensure_ascii=False, indent=2)

# Charger les commentaires au démarrage
commentaires_db = charger_commentaires()
tiktok_bot.set_commentaires(commentaires_db.get("default", []))

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est en ligne!")
    print("=" * 50)

@bot.command(name="commente")
async def commente_videos(ctx, hashtag: str, quantite: int = 3):
    """Commente les vidéos avec un hashtag
    Utilisation: /commente #mayotteislande 5
    """
    if not hashtag.startswith("#"):
        hashtag = "#" + hashtag
    
    hashtag = hashtag.lower().replace(" ", "")
    
    embed = discord.Embed(
        title="🔍 Recherche en cours...",
        description=f"Recherche de vidéos avec {hashtag}",
        color=discord.Color.blue()
    )
    message = await ctx.send(embed=embed)
    
    try:
        print(f"\n📱 Lancement: {hashtag} x{quantite}")
        resultado = await tiktok_bot.commenter_videos(hashtag, quantite)
        
        embed = discord.Embed(
            title="✅ Résultat",
            description=f"Hashtag: {hashtag}\n✅ Commentés: {resultado['exitosos']}\n❌ Erreurs: {resultado['fallidos']}",
            color=discord.Color.green()
        )
        await message.edit(embed=embed)
        
    except Exception as e:
        embed = discord.Embed(
            title="❌ Erreur",
            description=f"```{str(e)}```",
            color=discord.Color.red()
        )
        await message.edit(embed=embed)
        print(f"❌ Erreur: {str(e)}")

@bot.command(name="panel")
async def panel_commentaires(ctx):
    """Affiche le panel de gestion des commentaires"""
    
    commentaires = commentaires_db.get("default", [])
    
    # Créer l'embed du panel
    embed = discord.Embed(
        title="📝 Panel de Gestion des Commentaires",
        description="Gère les commentaires que le bot peut utiliser",
        color=discord.Color.purple()
    )
    
    # Afficher les commentaires actuels
    if commentaires:
        liste_com = "\n".join([f"`{i+1}.` {com}" for i, com in enumerate(commentaires)])
        embed.add_field(name="📋 Commentaires Actuels", value=liste_com, inline=False)
    else:
        embed.add_field(name="📋 Commentaires Actuels", value="Aucun commentaire", inline=False)
    
    embed.add_field(
        name="⚙️ Commandes Disponibles",
        value="""
`/ajouter_com <texte>` - Ajouter un commentaire
`/supprimer_com <numéro>` - Supprimer un commentaire
`/lister_com` - Afficher tous les commentaires
`/reset_com` - Réinitialiser les commentaires par défaut
        """,
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name="ajouter_com")
async def ajouter_commentaire(ctx, *, texte: str):
    """Ajouter un nouveau commentaire
    Utilisation: /ajouter_com Bv Bh
    """
    if not texte:
        await ctx.send("❌ Veuillez entrer un commentaire!")
        return
    
    commentaires = commentaires_db.get("default", [])
    
    if texte in commentaires:
        await ctx.send("⚠️ Ce commentaire existe déjà!")
        return
    
    commentaires.append(texte)
    commentaires_db["default"] = commentaires
    sauvegarder_commentaires(commentaires_db)
    tiktok_bot.set_commentaires(commentaires)
    
    embed = discord.Embed(
        title="✅ Commentaire Ajouté",
        description=f"**Nouveau:** {texte}\n**Total:** {len(commentaires)} commentaires",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)
    print(f"✅ Commentaire ajouté: {texte}")

@bot.command(name="supprimer_com")
async def supprimer_commentaire(ctx, numero: int):
    """Supprimer un commentaire par son numéro
    Utilisation: /supprimer_com 1
    """
    commentaires = commentaires_db.get("default", [])
    
    if numero < 1 or numero > len(commentaires):
        await ctx.send(f"❌ Numéro invalide! (1-{len(commentaires)})")
        return
    
    com_supprime = commentaires[numero - 1]
    commentaires.pop(numero - 1)
    commentaires_db["default"] = commentaires
    sauvegarder_commentaires(commentaires_db)
    tiktok_bot.set_commentaires(commentaires)
    
    embed = discord.Embed(
        title="🗑️ Commentaire Supprimé",
        description=f"**Supprimé:** {com_supprime}\n**Reste:** {len(commentaires)} commentaires",
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)
    print(f"🗑️ Commentaire supprimé: {com_supprime}")

@bot.command(name="lister_com")
async def lister_commentaires(ctx):
    """Affiche tous les commentaires configurés"""
    commentaires = commentaires_db.get("default", [])
    
    if not commentaires:
        await ctx.send("❌ Aucun commentaire configuré!")
        return
    
    embed = discord.Embed(
        title="📋 Liste des Commentaires",
        description="Tous les commentaires disponibles",
        color=discord.Color.blue()
    )
    
    liste = "\n".join([f"`{i+1}.` {com}" for i, com in enumerate(commentaires)])
    embed.add_field(name=f"Total: {len(commentaires)}", value=liste, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="reset_com")
async def reset_commentaires(ctx):
    """Réinitialiser les commentaires par défaut"""
    commentaires_par_defaut = [
        "🔥 Excellent!",
        "😂 Trop drôle!",
        "👍 J'adore!",
        "❤️ Magnifique!",
        "✨ Incroyable!",
        "🎯 Super!",
        "💯 Parfait!",
        "😍 Wow!",
        "🙌 Top!",
        "⚡ Dingue!",
    ]
    
    commentaires_db["default"] = commentaires_par_defaut
    sauvegarder_commentaires(commentaires_db)
    tiktok_bot.set_commentaires(commentaires_par_defaut)
    
    embed = discord.Embed(
        title="🔄 Réinitialisation",
        description=f"Les commentaires ont été réinitialisés!\n**Total:** {len(commentaires_par_defaut)} commentaires",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)
    print(f"🔄 Commentaires réinitialisés")

@bot.command(name="configurer")
async def configurer_hashtags(ctx, *, hashtags: str):
    """Configure les hashtags automatiques
    Utilisation: /configurer #mayotteislande #pourtoi #parati
    """
    liste_hashtags = hashtags.split()
    liste_hashtags = [h.lower().replace(" ", "") if h.startswith("#") else "#" + h.lower().replace(" ", "") for h in liste_hashtags]
    
    tiktok_bot.set_hashtags(liste_hashtags)
    
    embed = discord.Embed(
        title="📋 Hashtags configurés",
        description="\n".join(liste_hashtags),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)
    print(f"📋 Hashtags définis: {', '.join(liste_hashtags)}")

@bot.command(name="automatique")
async def automatique(ctx, intervalle: int = 60):
    """Lance les commentaires automatiques
    Utilisation: /automatique 120 (tous les 120 secondes)
    """
    await ctx.send(f"🤖 Mode automatique lancé (intervalle: {intervalle}s)")
    print(f"🤖 Boucle automatique: {intervalle}s")
    
    try:
        await tiktok_bot.boucle_automatique(intervalle)
    except Exception as e:
        print(f"❌ Erreur automatique: {str(e)}")

@bot.command(name="etat")
async def etat(ctx):
    """Affiche l'état du bot"""
    commentaires = commentaires_db.get("default", [])
    
    embed = discord.Embed(
        title="🟢 État du Bot",
        description="✅ Bot TikTok-Discord actif\n✅ Prêt à commenter",
        color=discord.Color.green()
    )
    embed.add_field(name="📝 Commentaires", value=f"{len(commentaires)} disponibles", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="arreter")
async def arreter(ctx):
    """Arrête le bot"""
    embed = discord.Embed(
        title="🛑 Arrêt",
        description="Bot arrêté",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)
    await bot.close()

@bot.command(name="aide")
async def aide(ctx):
    """Affiche l'aide complète"""
    embed = discord.Embed(
        title="🆘 Aide - Bot TikTok Discord",
        description="Liste de toutes les commandes disponibles",
        color=discord.Color.gold()
    )
    
    embed.add_field(
        name="🎬 Commentaires",
        value="""
`/commente <hashtag> [quantite]` - Commenter des vidéos
`/panel` - Afficher le panel de gestion
`/ajouter_com <texte>` - Ajouter un commentaire
`/supprimer_com <numéro>` - Supprimer un commentaire
`/lister_com` - Lister tous les commentaires
`/reset_com` - Réinitialiser les commentaires
        """,
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Configuration",
        value="""
`/configurer <hashtags>` - Configurer les hashtags
`/automatique [intervalle]` - Lancer en mode automatique
`/etat` - Afficher l'état du bot
`/arreter` - Arrêter le bot
        """,
        inline=False
    )
    
    await ctx.send(embed=embed)

# Obtenir le token
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("❌ DISCORD_TOKEN non trouvé dans .env")
    exit()

# Lancer le bot
try:
    bot.run(TOKEN)
except Exception as e:
    print(f"❌ Erreur de connexion: {str(e)}")
