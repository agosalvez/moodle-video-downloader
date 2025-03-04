from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import os
from datetime import datetime

class Config:
    def __init__(self, url, email, password, download_path):
        self.url = url
        self.email = email
        self.password = password
        self.download_path = os.path.abspath(download_path)
        os.makedirs(self.download_path, exist_ok=True)

class VideoDownloader:
    def __init__(self, config):
        self.config = config
        self.driver = self.iniciar_navegador()

    def iniciar_navegador(self):
        """Inicializa el navegador con configuración personalizada."""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-popup-blocking")
        prefs = {"download.default_directory": self.config.download_path}
        options.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def obtener_titulo_pagina(self):
        """Obtiene el título del video desde el elemento h2."""
        try:
            titulo_elemento = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.page-header-headings h1.h2"))
            )
            self.config.output_filename = titulo_elemento.text.strip().replace(" ", "_").replace("/", "_").replace("[", "_").replace("]", "_")
            print(f"Título detectado: {self.config.output_filename}")
        except Exception as e:
            print(f"Error al obtener el título: {e}")
            self.config.output_filename = "video_descargado"

    def descargar_video_directo(self, filename):
        """Descarga el video directamente desde la fuente."""
        try:
            video_src = self.driver.execute_script("""
                return document.querySelector('video source')?.getAttribute('src');
            """)
            
            if video_src:
                video_url = self.driver.current_url.rsplit('/', 1)[0] + '/' + video_src
                print(f"Descargando desde: {video_url}")
                
                cookies = {c['name']: c['value'] for c in self.driver.get_cookies()}
                response = requests.get(video_url, cookies=cookies, stream=True)

                if response.status_code == 200:
                    output_path = os.path.join(self.config.download_path, f"{self.config.output_filename}_{filename}.mp4")
                    with open(output_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Video descargado en: {output_path}")
                else:
                    print(f"Error al descargar video: {response.status_code}")
            else:
                print("No se encontró la URL del video.")
        except Exception as e:
            print(f"Error en la descarga: {e}")

    def login_automatico(self):
        """Realiza el inicio de sesión en la plataforma."""
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "i0116"))).send_keys(self.config.email)
            time.sleep(1)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
            
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "i0118"))).send_keys(self.config.password)
            time.sleep(1)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
            
            input("🕒 Complete el 2FA y presione [Enter] para continuar...")
        except Exception as e:
            print(f"Error en el login: {e}")

    def interactuar_en_pestana(self):
        """Busca y descarga el video desde la pestaña actual."""
        try:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            grabacion_link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@alt, 'Ver grabación')]")))
            filename = grabacion_link.text
            grabacion_link.click()
            time.sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.descargar_video_directo(filename)
        except Exception as e:
            print(f"Error en la pestaña de grabación: {e}")

    def abrir_enlace_inicial(self):
        """Abre los enlaces de las sesiones y gestiona las descargas."""
        self.obtener_titulo_pagina()
        enlaces_visitados = set()
        while True:
            try:
                self.driver.get(self.config.url)
                time.sleep(2)
                enlaces = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'courseindex-link') and contains(text(), 'SM142000') and contains(text(), 'Grupo 2')]"))
                )
                nuevos_enlaces = [e for e in enlaces if e.get_attribute("href") not in enlaces_visitados]
                
                if not nuevos_enlaces:
                    print("No quedan más enlaces.")
                    break
                
                enlace = nuevos_enlaces[0]
                enlaces_visitados.add(enlace.get_attribute("href"))
                enlace.send_keys(Keys.CONTROL + Keys.RETURN)
                time.sleep(2)
                self.interactuar_en_pestana()
            except Exception as e:
                print(f"Error en enlaces: {e}")
                break

    def ejecutar(self):
        self.driver.get(self.config.url)
        self.login_automatico()
        self.abrir_enlace_inicial()
        print("Proceso completado.")
        self.driver.quit()

# Programa principal
if __name__ == "__main__":
    config = Config(
        url="https://campus.uax.es/moodle/course/view.php?id=16854",
        email="YOUR_EMAIL",
        password="YOUR_PASSWORD",
        download_path="YOUR_PATH_TO_DOWNLOAD",
    )
    downloader = VideoDownloader(config)
    downloader.ejecutar()
