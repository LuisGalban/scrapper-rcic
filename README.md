🕷️ RCIC Legal Data Scraper
Este es un proyecto de automatización desarrollado en Python utilizando Selenium para la extracción de datos públicos del registro oficial del College of Immigration and Citizenship Consultants (CCIC).

El script navega dinámicamente a través de los perfiles de los consultores, extrae información detallada (empresa, ubicación, contacto) y la estructura en un archivo Excel listo para su análisis.

🚀 Características
Gestión Automática de Drivers: Gracias a webdriver-manager, no necesitas descargar manualmente el chromedriver.exe. El script detecta tu versión de Chrome y lo configura solo.

Extracción Profunda: No solo toma los datos de la tabla principal, sino que entra en cada perfil para obtener detalles específicos de contacto.

Manejo de Paginación: Procesa múltiples páginas de resultados de forma secuencial.

🛠️ Requisitos Previos
Antes de ejecutar el script, asegúrate de tener instalado:

Python 3.8+

Google Chrome (El navegador)

📦 Instalación
Clona este repositorio:

Bash

git clone https://github.com/LuisGalban/scrapper-rcic.git
Instala las dependencias necesarias:

Bash

pip install -r requirements.txt
Nota sobre el Driver: A diferencia de otros scrapers básicos, este proyecto utiliza webdriver-manager. Esto significa que no necesitas buscar ni instalar el chromedriver manualmente; el código se encarga de la compatibilidad por ti.

📋 Uso
Simplemente ejecuta el script principal:

Bash

python scrap.py
Al finalizar, encontrarás un archivo llamado rcic_data.xlsx en la carpeta del proyecto con toda la información recolectada.
