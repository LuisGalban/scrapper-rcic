import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class RCICScraper:
    def __init__(self):
        self.url = 'https://register.college-ic.ca/Public-Register-EN/RCIC_Search.aspx'
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.wait = WebDriverWait(self.driver, 12)
        self.data = []

    def configurar_busqueda(self):
        self.driver.get(self.url)
        # Click en buscar
        btn_search = self.wait.until(EC.element_to_be_clickable((By.ID, "ctl01_TemplateBody_WebPartManager1_gwpciSearchLicensee_ciSearchLicensee_ResultsGrid_Sheet0_SubmitButton")))
        btn_search.click()
        
        # Cambiar capacidad a 10 (o 50 para ser más eficiente)
        selector_paginas = self.wait.until(EC.element_to_be_clickable((By.ID, "ctl01_TemplateBody_WebPartManager1_gwpciSearchLicensee_ciSearchLicensee_ResultsGrid_Grid1_ctl00_ctl03_ctl01_PageSizeComboBox_Input")))
        selector_paginas.click()
        
        opcion_10 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'10') and @role='option']")))
        opcion_10.click()
        time.sleep(2)

    def extraer_datos_fila(self, row):
        try:
            name = row.find_element(By.XPATH, ".//td[3]").text.strip()
            college_id = row.find_element(By.XPATH, ".//td[2]").text.strip()
            
            # Logica de ventana secundaria
            link = row.find_element(By.XPATH, ".//a[@title='Select']")
            self.driver.execute_script("window.open(arguments[0]);", link.get_attribute('href'))
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Licensee Details']"))).click()
        
            empresa = self.driver.find_element(By.XPATH, '//*[contains(@id, "ResultsGrid_Grid1_ctl00__0")]/td[1]').text
            
            self.data.append({
                'Name': name,
                'College ID': college_id,
                'Company': empresa
            })
            
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except Exception as e:
            print(f"Error procesando fila: {e}")

    def ejecutar(self, max_paginas=5):
        try:
            self.configurar_busqueda()
            paginas_procesadas = 0
            
            while paginas_procesadas < max_paginas:
                rows = self.driver.find_elements(By.XPATH, "//tbody/tr")
                for row in rows:
                    self.extraer_datos_fila(row)
                
                # Siguiente página
                next_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@title='Next Page']")))
                next_btn.click()
                paginas_procesadas += 1
                
            df = pd.DataFrame(self.data)
            df.to_excel('rcic_data.xlsx', index=False)
            print("¡Éxito! Datos guardados.")
            
        finally:
            self.driver.quit()

if __name__ == "__main__":
    scraper = RCICScraper()
    scraper.ejecutar()