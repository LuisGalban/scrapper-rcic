from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import io
import time
import pandas as pd

def ejecutar_scrapper():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    path_to_chromedriver = r'C:\Users\Kike-pc\Downloads\chromedriver-win64\chromedriver.exe'
    service = Service(executable_path=path_to_chromedriver)
    
    driver = webdriver.Chrome(service=service)
    driver.get('https://register.college-ic.ca/Public-Register-EN/RCIC_Search.aspx')
    
    wait = WebDriverWait(driver, 10)
    find = driver.find_element(By.ID, "ctl01_TemplateBody_WebPartManager1_gwpciSearchLicensee_ciSearchLicensee_ResultsGrid_Sheet0_SubmitButton")
    
    find.click()
    time.sleep(3)
    
    capacidad = wait.until(EC.element_to_be_clickable((By.ID, "ctl01_TemplateBody_WebPartManager1_gwpciSearchLicensee_ciSearchLicensee_ResultsGrid_Grid1_ctl00_ctl03_ctl01_PageSizeComboBox_Input")))
    capacidad.click()
    
    selec_capacidad = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'10') and @role='option']")))
    selec_capacidad.click()
    time.sleep(3)
    start_page = 2
    for _ in range(start_page - 1):
        time.sleep(3)
        next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@title='Next Page']")))
        next_page_button.click()
        time.sleep(3)
    data = []
    
    page_count = start_page
    while page_count < 20:
        try:
            rows = driver.find_elements(By.XPATH, "//tbody/tr")
            
            for row in rows:
                try:
                    print("Procesando fila")
                    name = row.find_element(By.XPATH, ".//td[3]").text.strip()
                    college_id = row.find_element(By.XPATH, ".//td[2]").text.strip()
                    type_ = row.find_element(By.XPATH, ".//td[5]").text.strip()
                    
                    # Encontrar el enlace dentro de cada fila y hacer clic en él
                    link = row.find_element(By.XPATH, ".//a[@title='Select']")
                    href = link.get_attribute('href')
                    
                    driver.execute_script("window.open(arguments[0]);", href)
                    driver.switch_to.window(driver.window_handles[-1])
                    
                    # Esperar a que la nueva página cargue
                    time.sleep(3)
                    
                    licensee_details_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'rtsLink') and .//span[text()='Licensee Details']]")))
                    licensee_details_link.click()
                    time.sleep(3)
                    
                    company = driver.find_element(By.XPATH, '//*[@id="ctl01_TemplateBody_WebPartManager1_gwpciProfileCCO_ciProfileCCO_Employment_ResultsGrid_Grid1_ctl00__0"]/td[1]')
                    start_date = driver.find_element(By.XPATH, '//*[@id="ctl01_TemplateBody_WebPartManager1_gwpciProfileCCO_ciProfileCCO_Employment_ResultsGrid_Grid1_ctl00__0"]/td[2]')
                    country = driver.find_element(By.XPATH, '//*[@id="ctl01_TemplateBody_WebPartManager1_gwpciProfileCCO_ciProfileCCO_Employment_ResultsGrid_Grid1_ctl00__0"]/td[3]')
                    province_state = driver.find_element(By.XPATH, '//*[@id="ctl01_TemplateBody_WebPartManager1_gwpciProfileCCO_ciProfileCCO_Employment_ResultsGrid_Grid1_ctl00__0"]/td[4]')
                    city = driver.find_element(By.XPATH, '//*[@id="ctl01_TemplateBody_WebPartManager1_gwpciProfileCCO_ciProfileCCO_Employment_ResultsGrid_Grid1_ctl00__0"]/td[5]')
                    email = driver.find_element(By.XPATH, '//*[@id="ctl01_TemplateBody_WebPartManager1_gwpciProfileCCO_ciProfileCCO_Employment_ResultsGrid_Grid1_ctl00__0"]/td[6]')
                    phone = driver.find_element(By.XPATH, '//*[@id="ctl01_TemplateBody_WebPartManager1_gwpciProfileCCO_ciProfileCCO_Employment_ResultsGrid_Grid1_ctl00__0"]/td[7]')
                    
                    data.append({
                        'Name': name,
                        'College ID': college_id,
                        'Type': type_,
                        'Company': company.text,
                        'Start Date': start_date.text,
                        'Country': country.text,
                        'Province/State': province_state.text,
                        'City': city.text,
                        'Email': email.text,
                        'Phone': phone.text
                    })
                    
                    time.sleep(3)
                    
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    
                except Exception as e:
                    print(f"Error al procesar la fila: {e}")
                    
            try:
                next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@title='Next Page']")))
                next_page_button.click()
                time.sleep(2)
                find = driver.find_element(By.ID, "ctl01_TemplateBody_WebPartManager1_gwpciSearchLicensee_ciSearchLicensee_ResultsGrid_Sheet0_SubmitButton")
                find.click()
                capacidad = wait.until(EC.element_to_be_clickable((By.ID, "ctl01_TemplateBody_WebPartManager1_gwpciSearchLicensee_ciSearchLicensee_ResultsGrid_Grid1_ctl00_ctl03_ctl01_PageSizeComboBox_Input")))
                capacidad.click()
                selec_capacidad = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'10') and @role='option']")))
                selec_capacidad.click()
                for _ in range(page_count):
                    time.sleep(3)
                    next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@title='Next Page']")))
                    next_page_button.click()
                    time.sleep(3)
                page_count += 1
            except Exception as e:
                print(f"Error al cambiar de página: {e}")
                break
        except Exception as e:
            print(f"Error al procesar la página: {e}")
            break
    
    driver.quit()
    df = pd.DataFrame(data)
    df.to_excel('output.xlsx', index=False)
    return print("Proceso completado y datos guardados en 'output.xlsx'")

ejecutar_scrapper()
