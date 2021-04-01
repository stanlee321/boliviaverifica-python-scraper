import json

import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from logger import LoggingHandler

from datetime import  datetime
import pandas as pd

from typing import Any

log = LoggingHandler()

class NewsScraper:

    def __init__(self,project_path:str ):
        """
        This scraper downloads information from https://boliviaverifica.bo/
        """
        # Project path

        self.PROJECT_PATH = project_path

    def _login_custom(self,
                    input_link:str,
                    headless:bool):
        """ Logging into our own profile """

        try:
            driver = None
            options = Options()

            #  Code to disable notifications pop up of Chrome Browser
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument("--mute-audio")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")

            if headless:
                options.add_argument("--headless")

                    
            try:
                driver = webdriver.Chrome(
                    executable_path=ChromeDriverManager().install(), 
                    options=options
                )

            except Exception:
                print("Error loading chrome webdriver " + sys.exc_info()[0])
                exit(1)

            driver.get(input_link)
            driver.maximize_window()

            return driver

        except Exception as e:
            print(e)
            print("There's some error in log in.")
            print(sys.exc_info()[0])

    def get_last_page_number(self, driver:Any, selectors:Any):

        page_numbers = driver.find_elements_by_xpath(selectors.get("page-numbers"))

        # Crear una lista auxiliar para agarrar los valores de text de los numeros del paginador
        aux_list = []

        # Iterar sobre los numeros que se encontraron.
        for number in page_numbers:
            print(number.text)
            aux_list.append(int(number.text))

        max_number = max(aux_list)

        return max_number

    def go_to_page(self, driver:Any, page_number:int ):
        """
         Este metodo navegara a la pagina con el page_number como parametro
        """
        # https://boliviaverifica.bo/category/coronavirus/page/8/


        link = f"https://boliviaverifica.bo/category/coronavirus/page/{page_number}/"

        print(link)

        driver.get(link)

        time.sleep(5)

    def get_post_links(self, driver:Any, selectors:Any, page_number: int):
        """
        Este metodo tiene el fin de extraer los links de cada uno de los posts en una pagina que se cargo.
        """
        # Aqui buscamos las imagenes de las noticias
        post_elements = driver.find_elements_by_xpath(selectors.get("post_img"))

        print("FOUND POSTS??", len(post_elements))

        my_links = []
        # para cada una de las imagenes encontradas, extraer el HREF (link)
        for elemenent in post_elements:
            img = elemenent.find_element_by_xpath(selectors.get("thumb-zoom"))
            _link = img.get_attribute('href')

            my_data = { "link": _link, "page": page_number}

            my_links.append(my_data)

        
        df_aux = pd.DataFrame(my_links)
        df_aux.to_csv(f"{page_number}_links.csv", index=False)

        print("DONE.. saved in ...", f"{page_number}_links.csv")

        #print(_link)


    def get_post_info(self, driver:Any, selectors:Any):

        title_element = driver.find_element_by_xpath(selectors.get("entry-title"))
        date_element = driver.find_element_by_xpath(selectors.get("posted-on"))
        post_view = driver.find_element_by_xpath(selectors.get("post-view"))


        title_text = title_element.text
        date_text = date_element.text
        views_text = post_view.text
        

        print("TITLE: " , title_text)
        print("CREATED AT: " , date_text)
        print("VIEWS TEXT: " , views_text)

        content_element = driver.find_element_by_xpath(selectors.get("entry-content clearfix"))
        
        # Extract all the images from the page
        images = content_element.find_elements_by_tag_name('img')

        for img in images:
            link_to_image = img.get_attribute('src')
            print(link_to_image)

        # Extraer todos los textos.

        texts = content_element.find_elements_by_xpath(selectors.get("style-text"))

        my_whole_text = ""

        for text_element in texts:

            my_whole_text += "<SP>"  + text_element.text + "<EP>"

        print(my_whole_text)
        
    

    def run_scraper(self, selectors:dict, category:str,  headless:bool = False )->None:
        """
        Download a file from a given page.
        
        
        :PARAMS:
        -------
        :param: headless: bool - if we run the scraper in headless mode (WITH OUT UI)
        :RETURNS:
        --------
        PATH TO THE DOWNLOADED FILE
        """

        try:
                
            # Load the base link for the page
            link = selectors.get("base_link")

            # Category link

            new_link = link + "category/" + category

            # Create web Driver 
            driver = self._login_custom(
                input_link = new_link,
                headless = headless)

            # Take some time for load the Page ....
            time.sleep(5)

            # Calcular el numero total de paginas existentes
            max_value = self.get_last_page_number( driver = driver, selectors = selectors)
            print("LAST PAGE: ", max_value)

            # Navegar a cada una de esas paginas
            for page_number in range(1, max_value):

                # Navegar a la siguiente pagina
                self.go_to_page(driver = driver, page_number = page_number )

                # Extraer, extraer los links a los posts
                self.get_post_links(driver = driver, selectors = selectors, page_number = page_number )

        except Exception as e:
            print(e)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log.logger.error(f"ERROR!!! at time: {now}, {e}")

        return None

    def test_scraper(self,  selectors:dict,  headless:bool = False, category:str = "coronavirus" ):
        # Load the base link for the page
        #link = "https://boliviaverifica.bo/los-10-puntos-clave-para-conocer-el-plan-nacional-de-vacunacion-covid-19/"
        link = "https://boliviaverifica.bo/es-falso-que-se-suspendio-la-vacunacion-en-una-ciudad-de-argentina/"
        # Create web Driver 
        driver = self._login_custom(
            input_link = link,
            headless = headless)

        # Take some time for load the Page ....
        time.sleep(5)
        
        self.get_post_info(driver = driver, selectors = selectors )

        
    def main(self, selectors:dict,  headless:bool = False, category:str = "coronavirus"):

        
        #self.run_scraper(selectors = selectors, headless = headless, category = category)

        self.test_scraper( selectors = selectors,  headless = headless, category = category )


if __name__ == "__main__":

    cwd = os.getenv("PROJ_DIR")
    
    # set the desired category
    category = "coronavirus"


    # Open the selectors
    with open(f"{cwd}/selectors.json") as a:
        selectors = json.load(a)

    # Create Instance of the scraper
    # Test main pipeline
    elecciones = NewsScraper(project_path = cwd )

    # RUN
    elecciones.main(selectors=selectors, headless=False, category = category)