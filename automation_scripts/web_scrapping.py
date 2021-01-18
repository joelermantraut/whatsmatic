#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Clase para facilitar la interaccion con un sitio WEB.

Emplea Selenium junto con Chrome Driver.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# Selenium imports
from time import sleep
# Standar Python

class WebScrapper(object):
    """Clase dedicada a scrappear un sitio WEB mediante Chromedriver"""
    def __init__(self, PATH, url):
        super(WebScrapper, self).__init__()
        self.PATH = PATH
        # Direccion donde esta guardado ChromeDriver
        self.url = url
        self.find_methods = [
            By.ID,
            By.XPATH,
            By.LINK_TEXT,
            By.PARTIAL_LINK_TEXT,
            By.NAME,
            By.TAG_NAME,
            By.CLASS_NAME,
            By.CSS_SELECTOR
        ]
        self.modifier_strings = {
            "ctrl": Keys.CONTROL,
            "alt": Keys.ALT,
            "shift": Keys.SHIFT,
            "enter": Keys.RETURN,
            "backspace": Keys.BACKSPACE,
            "arrow_down": Keys.ARROW_DOWN,
            "arrow_up": Keys.ARROW_UP,
            "arrow_left": Keys.ARROW_LEFT,
            "arrow_right": Keys.ARROW_RIGHT,
            'page_up': Keys.PAGE_UP,
            'page_down': Keys.PAGE_DOWN,
            "delete": Keys.DELETE,
            "escape": Keys.ESCAPE,
            "space": Keys.SPACE,
            "tab": Keys.TAB
        }
        self.init()

    def init(self):
        """
        Inicializa el WebDriver
        """
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get(self.url)

    def quit(self):
        """
        Cierra el ChromeDriver
        """
        self.driver.quit()

    def get_title(self):
        """
        Obtiene el titulo del sitio.
        """
        return self.driver.title

    def maximize(self):
        """
        Maximiza la ventana
        """
        self.driver.maximize_window()

    def refresh(self):
        """
        Refresca la pagina
        """
        self.driver.refresh()

    def get_elements(self, selector, roots=None):
        """
        Obtiene el objeto y lo devuelve.

        IMPORTANTE:
         - Si se le pasa root, usa ese elemento como raiz
         - Si no, usa el driver
         - Emplea los selectores de css

        FUENTE:
        https://selenium-python.readthedocs.io/locating-elements.html
        """
        if roots == None:
            roots = self.driver

        if type(roots) is not list:
            roots = [roots]

        new_roots = []
        for root in roots:
            new_roots += root.find_elements_by_css_selector(selector)

        return new_roots

    def process_keys(self, element, key):
        """
        Decide que teclas presionar.

         - Si recibe una combinacion: tecla + tecla, obtiene las
           teclas modificadores, las mantiene y presionas las otras.
        """
        if '+' in key and len(key) > 1: # Si esta el + pero no es solo un +
            keys = key.split('+') # Divide la cadena para obtener las teclas

            for key in keys: # Sirve para cualquier cantidad de modificadores
                if key in self.modifier_strings.keys():
                    key = self.modifier_strings[key]
                    ActionChains(self.driver).key_down(key).perform()
                # Obtiene el objeto de Selenium que corresponde a la modificadora
                else:
                    if element is None:
                            ActionChains(self.driver).send_keys(key).perform()
                    else:
                            ActionChains(self.driver).send_keys_to_element(element, key).perform()

            for key in keys:
                if key in self.modifier_strings.keys():
                    key = self.modifier_strings[key]
                    ActionChains(self.driver).key_up(key).perform()
            # Suelta todas los modificadores

        else:
            # Para teclas individuales
            if key in self.modifier_strings.keys():
                key = self.modifier_strings[key]
            # Verificamos si es una tecla especial

            if element is None:
                ActionChains(self.driver).send_keys(key).perform()
            else:
                ActionChains(self.driver).send_keys_to_element(element, key).perform()

    def send_keys(self, elements, keys_list):
        """
        Recibe una lista de teclas y las ejecuta una por una.

         - Si recibe un numero es el retardo hasta la proxima tecla.
         - Para enviar un numero debe recibir una cadena numerica.
         - Si element es una lista, ejecuta las acciones en cada elemento de la lista.
        """
        if type(elements) is not list:
            elements = [elements]

        for element in elements:
            for key in keys_list:
                if type(key) is int: # Es un numero
                    sleep(key) # Espero ese tiempo
                else:
                    self.process_keys(element, key)

    def click_elements(self, elements=None, times=1):
        """
        Clickea el elemento que se le pasa
         - Si recibe una lista, clickea cada elemento
         - Times: cantidad de veces que clickea el elemento
         - Times == 0, presiona y mantiene
         - Si no recibe elemento, clickea en la posicion actual del cursor
        """
        if type(elements) is not list:
            elements = [elements]

        for element in elements:
            if times == 0:
                ActionChains(self.driver).click_and_hold(element).perform() 
            else:
                try:
                    for i in range(times):
                        ActionChains(self.driver).click(element).perform()
                        sleep(0.1) # 100ms
                except Exception:
                    pass
                # Excepcion para los casos en los que se presiona
                # el elemento y eso lleva a una pagina en la que
                # el elemento ya no esta.

    def move_mouse_to_element(self, element):
        """
        Mueve el mouse a la mitad del elemento que se le pasa.

         - Si recibe una lista de mas de un elemento, no hace nada
         - Si recibe uno solo, se queda con ese elemento
        """

        if type(element) is list and len(element) > 1:
            return
        elif type(element) is list:
            element = element[0]
        elif type(element) is str:
            element = self.get_elements(element)[0]

        ActionChains(self.driver).move_to_element(element).perform()

    def scroll_to_element_class(self, element):
        """
        Scrolls up to set a element_class in view position.
        """
        self.scripting("document.getElementByClassName('{0}').scrollIntoView();".format(element_class))

    def clear_content(self, elements):
        """
        Pone en blanco input, textarea, etc.
        """

        if type(elements) is not list:
            elements = [elements] 

        for element in elements:
            element.clear()

    def screenshot(self, elements, filename=None):
        """
        Toma una captura del elemento que se le pasa

         - Si se le pasan varios, toma de todos.
         - Si alguna de las capturas devuelve False, devuelve False
         - Si no devuelve True
         - Si no se le pasa un nombre, usa el formato por defecto
         - Si se le pasa un nombre, del segundo en adelante le agrega
           un subindice
        """

        if type(elements) is not list:
            elements = [elements]

        for element in elements:
            i = elements.index(element)
            if i == 0:
                element.screenshot(filename + '.png')
            else:
                element.screenshot(filename + str(i) + '.png')

    def get_properties(self, name, elements=None):
        """
        Obtiene las propiedades o atributos del elemento
         - Si no se le pasa elemento, del driver
         - Si el nombre que se le pasa no existe, devuelve None
        """
        if elements == None:
            elements = self.driver
        elif type(elements) is not list:
            elements = [elements]

        attributes = []
        for element in elements:
            if name == 'display':
                attributes.append(element.is_displayed())
            elif name == 'enabled':
                attributes.append(element.is_enabled())
            elif name == 'selected':
                attributes.append(element.is_selected())
            else:
                attributes.append(element.get_attribute(name))

        return attributes

    def get_all_properties(self, elements=None):
        """
        Gets all properties of the element.

         - If the argument is a list of elements, does the same
           for each one.
         - If no element is given, use the driver.
        """
        properties = list()
 
        if elements == None:
            elements = self.driver
        elif type(elements) is not list:
            elements = [elements]

        for element in elements:
            properties.append(self.driver.execute_script(' \
                    var items = {}; \
                    for (index = 0; index < arguments[0].attributes.length; ++index) { \
                        items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value \
                    }; \
                    return items;',
                    element))

        return properties

    def scripting(self, code=None, filename=None):
        """
        Ejecuta un script JS.

         - Si lo que recibe es una lista de scripts, ejecuta uno por uno
        """
        if filename != None:
            file = open(filename, 'r')
            code = file.read()
            file.close()

        script_response = None

        if type(code) is list:
            script_response = list()
            for script in code:
                response = self.driver.execute_script(script)
                script_response.append(response)
        else:
            script_response = self.driver.execute_script(code)

        return script_response

def main():
    scrapper = WebScrapper(
        "/home/joel/Apps/chromedriver",
        "https://web.whatsapp.com" 
    )

    sleep(5)

    element = scrapper.get_elements("._3soxC")
    print(element)
    # scrapper.move_mouse_to_element(element)

    sleep(5)

    scrapper.quit()

if __name__ == "__main__":
    main()
