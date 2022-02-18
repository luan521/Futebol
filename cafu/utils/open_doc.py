from cafu.utils.queries.webdriver_chrome import WebdriverChrome
from cafu.metadata.paths import path

def open_doc(subpackage=''):
    """
    Args:
        subpackage: (str) complemento do caminho para um subpackage específico
        
    Abre a documentação da biblioteca cafu
    """
    
    path_doc = (
                'file:///' +
                path('initial_path') +
                f'/docs/build/html/module/cafu{subpackage}.html'
               )
    
    web = WebdriverChrome(headless=False)
    web.web.get(path_doc)