import asyncio
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TikTokBot:
    def __init__(self):
        self.commentaires = [
            "🔥 Excellent!",
            "😂 Trop drôle!",
            "👍 J'adore!",
            "❤️ Magnifique!",
            "✨ Incroyable!",
        ]
        self.hashtags_config = []
        self.driver = None
    
    def set_commentaires(self, commentaires):
        """Définir les commentaires à utiliser"""
        self.commentaires = commentaires
        print(f"✅ Commentaires définis: {len(commentaires)} disponibles")
    
    def set_hashtags(self, hashtags):
        """Définir les hashtags à utiliser"""
        self.hashtags_config = hashtags
        print(f"✅ Hashtags configurés: {', '.join(hashtags)}")
    
    def initialiser_driver(self):
        """Initialiser le driver Selenium"""
        try:
            options = Options()
            # Pour Termux, utiliser en headless
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            print("✅ Driver Selenium initialisé")
        except Exception as e:
            print(f"❌ Erreur initialisation driver: {str(e)}")
            raise
    
    async def commenter_videos(self, hashtag, quantite):
        """Commenter les vidéos avec un hashtag"""
        exitosos = 0
        fallidos = 0
        
        if not self.commentaires:
            print("❌ Aucun commentaire configuré!")
            return {"exitosos": 0, "fallidos": 0}
        
        try:
            self.initialiser_driver()
            
            # Nettoyer le hashtag
            hashtag = hashtag.lower().replace(" ", "")
            if not hashtag.startswith("#"):
                hashtag = "#" + hashtag
            
            url = f"https://www.tiktok.com/search/video?q={hashtag}"
            print(f"📍 URL: {url}")
            
            self.driver.get(url)
            await asyncio.sleep(3)
            
            # Scroller pour charger les vidéos
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(1)
            
            # Trouver tous les liens de vidéos
            video_links = []
            try:
                videos = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/video/']")
                video_links = [v.get_attribute("href") for v in videos[:quantite]]
                print(f"🎬 {len(video_links)} vidéos trouvées")
            except Exception as e:
                print(f"⚠️ Erreur recherche vidéos: {str(e)}")
            
            # Commenter chaque vidéo
            for i, video_url in enumerate(video_links, 1):
                try:
                    print(f"  [{i}/{len(video_links)}] Accès à {video_url}")
                    self.driver.get(video_url)
                    await asyncio.sleep(2)
                    
                    # Chercher le bouton commentaire
                    try:
                        # Scroller vers le bas
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        await asyncio.sleep(1)
                        
                        # Chercher le champ de commentaire
                        comment_input = self.driver.find_element(
                            By.CSS_SELECTOR, 
                            "input[placeholder*='Commente']"
                        )
                        
                        commentaire = random.choice(self.commentaires)
                        comment_input.send_keys(commentaire)
                        await asyncio.sleep(1)
                        
                        # Chercher le bouton d'envoi
                        try:
                            send_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                            send_btn.click()
                            print(f"    ✅ Commenté: {commentaire}")
                            exitosos += 1
                        except:
                            print(f"    ⚠️ Impossible d'envoyer le commentaire")
                            fallidos += 1
                        
                    except Exception as e:
                        print(f"    ⚠️ Champ commentaire non trouvé: {str(e)}")
                        fallidos += 1
                    
                    # Attendre avant la prochaine
                    await asyncio.sleep(random.randint(3, 7))
                    
                except Exception as e:
                    print(f"    ❌ Erreur vidéo {i}: {str(e)}")
                    fallidos += 1
                    await asyncio.sleep(2)
        
        except Exception as e:
            print(f"❌ Erreur générale: {str(e)}")
        
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                    print("🛑 Driver fermé")
                except:
                    pass
        
        print(f"📊 Résumé: ✅ {exitosos} | ❌ {fallidos}\n")
        return {"exitosos": exitosos, "fallidos": fallidos}
    
    async def boucle_automatique(self, intervalle=60):
        """Boucle automatique de commentaires"""
        if not self.hashtags_config:
            print("❌ Aucun hashtag configuré!")
            return
        
        while True:
            try:
                hashtag = random.choice(self.hashtags_config)
                print(f"\n🔄 Cycle automatique: {hashtag}")
                await self.commenter_videos(hashtag, 2)
                
                print(f"⏳ Prochaine exécution dans {intervalle}s...")
                await asyncio.sleep(intervalle)
            
            except Exception as e:
                print(f"❌ Erreur boucle: {str(e)}")
                await asyncio.sleep(10)
