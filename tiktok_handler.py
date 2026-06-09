import asyncio
import random
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

load_dotenv()

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
        self.is_logged_in = False
        
        # Identifiants TikTok depuis .env
        self.tiktok_username = os.getenv("TIKTOK_USERNAME")
        self.tiktok_password = os.getenv("TIKTOK_PASSWORD")
        self.headless = os.getenv("HEADLESS", "true").lower() == "true"
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
    
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
            
            if self.headless:
                options.add_argument("--headless")
            
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            # Options pour améliorer la stabilité
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            print("✅ Driver Selenium initialisé")
        except Exception as e:
            print(f"❌ Erreur initialisation driver: {str(e)}")
            raise
    
    async def se_connecter_tiktok(self):
        """Se connecter au compte TikTok"""
        if not self.tiktok_username or not self.tiktok_password:
            print("❌ Identifiants TikTok manquants dans .env")
            return False
        
        try:
            print(f"🔐 Connexion à TikTok: {self.tiktok_username}")
            
            # Aller à la page de connexion
            self.driver.get("https://www.tiktok.com/login")
            await asyncio.sleep(3)
            
            # Attendre et cliquer sur le bouton "Utiliser numéro de téléphone ou e-mail"
            try:
                # Attendre le chargement de la page
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
                )
                
                # Chercher le champ de connexion
                # TikTok utilise différents sélecteurs selon le navigateur
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                
                if len(inputs) > 0:
                    # Premier input = nom d'utilisateur/email
                    print("📝 Saisie du nom d'utilisateur...")
                    inputs[0].click()
                    inputs[0].clear()
                    inputs[0].send_keys(self.tiktok_username)
                    await asyncio.sleep(1)
                    
                    if len(inputs) > 1:
                        # Deuxième input = mot de passe
                        print("🔑 Saisie du mot de passe...")
                        inputs[1].click()
                        inputs[1].clear()
                        inputs[1].send_keys(self.tiktok_password)
                        await asyncio.sleep(1)
                        
                        # Chercher et cliquer le bouton de connexion
                        buttons = self.driver.find_elements(By.TAG_NAME, "button")
                        for btn in buttons:
                            if "connexion" in btn.text.lower() or "login" in btn.text.lower() or "se connecter" in btn.text.lower():
                                print("✅ Clic sur le bouton de connexion...")
                                btn.click()
                                await asyncio.sleep(5)
                                break
                
            except Exception as e:
                print(f"⚠️ Erreur saisie formulaire: {str(e)}")
                return False
            
            # Vérifier si connecté (chercher la page d'accueil)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/')]"))
                )
                self.is_logged_in = True
                print("✅ Connecté avec succès!")
                return True
            except:
                print("❌ Connexion échouée")
                return False
        
        except Exception as e:
            print(f"❌ Erreur connexion TikTok: {str(e)}")
            return False
    
    async def commenter_videos(self, hashtag, quantite):
        """Commenter les vidéos avec un hashtag"""
        exitosos = 0
        fallidos = 0
        
        if not self.commentaires:
            print("❌ Aucun commentaire configuré!")
            return {"exitosos": 0, "fallidos": 0}
        
        try:
            self.initialiser_driver()
            
            # Se connecter à TikTok
            if not await self.se_connecter_tiktok():
                print("⚠️ Impossible de se connecter, tentative sans connexion...")
            
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
                    await asyncio.sleep(3)
                    
                    # Chercher le bouton/champ commentaire
                    try:
                        # Scroller vers le bas pour voir le champ commentaire
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        await asyncio.sleep(2)
                        
                        # Chercher différents sélecteurs possibles pour le champ commentaire
                        comment_input = None
                        
                        # Essayer différents sélecteurs
                        selectors = [
                            ("input[placeholder*='Commente']", "input avec placeholder"),
                            ("input[placeholder*='Comment']", "input comment en anglais"),
                            ("input[data-testid*='comment']", "input data-testid"),
                            ("textarea[placeholder*='Commente']", "textarea"),
                            ("input[role='textbox']", "input textbox"),
                        ]
                        
                        for selector, description in selectors:
                            try:
                                comment_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                                print(f"    ✅ Champ trouvé: {description}")
                                break
                            except:
                                pass
                        
                        if comment_input:
                            # Cliquer sur le champ
                            comment_input.click()
                            await asyncio.sleep(1)
                            
                            # Saisir le commentaire
                            commentaire = random.choice(self.commentaires)
                            comment_input.send_keys(commentaire)
                            await asyncio.sleep(1)
                            
                            # Chercher et cliquer le bouton d'envoi
                            send_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                            for btn in send_buttons:
                                btn_text = btn.text.lower()
                                if "envoyer" in btn_text or "send" in btn_text or "poste" in btn_text:
                                    btn.click()
                                    print(f"    ✅ Commenté: {commentaire}")
                                    exitosos += 1
                                    await asyncio.sleep(2)
                                    break
                            else:
                                # Si pas de bouton visible, essayer Entrée
                                comment_input.send_keys(Keys.RETURN)
                                print(f"    ✅ Commenté (Entrée): {commentaire}")
                                exitosos += 1
                                await asyncio.sleep(2)
                        else:
                            print(f"    ⚠️ Champ commentaire non trouvé")
                            fallidos += 1
                        
                    except Exception as e:
                        print(f"    ⚠️ Erreur commentaire: {str(e)}")
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
