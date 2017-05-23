import re
import abc
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


_log = logging.getLogger(__name__)


def Url(url):
    """ Decorator for view classes to add url property. 
    Url property is then used when navigating to view
    
    This should be a relative path to the view
    """
    def _wrapper(cls):
        setattr(cls, "url", url)
        return cls
    return _wrapper

class View(object):
    """ Base class for which all page objects extends from.  
    The Goal of page objects is to allow a logic encapsulation of page recoginition,
    mapping of page elements and exposing logical services. 
    
    All views that extends from View have to implement exist(). 
    This method will check that we are on the right page.
    
    This base view also works as a context manager using with statement
    ::
    
        @Url('/my/relative/path')  
        class MyView(View)
            element = BaseElement("css=h1")

    """

    __metaclass__ = abc.ABCMeta

    url = None

    def __init__(self, driver, cfg, *args):
        _log.debug("View Initialized: {0}".format(self.__class__.__name__))
        self._driver = driver
        self.cfg = cfg

    @property
    def driver(self):
        return self._driver

    @abc.abstractmethod
    def exist(self):
        """ Abstract method that needs to be implemented at every view
        """
        raise NotImplementedError


    def open(self, exists=True, **kwargs):
        """ Open is used when navigation to a view. 
        Uses url property which can be set using Url decorator
        
        :param exits: used if view to open should exist or not
        :param kwargs: keywords to replace in view url
                        eg Url("relative path")
                        
        """

        if self.url is None:
            _log.debug("Page {0} does not have url defined".format(self.__class__.__name__))

        local_url = '{0}{1}'.format(self.cfg.base_url, self.url)

        if kwargs is not None:
            for i, j in kwargs.iteritems():
                local_url = re.sub("(?is)<%s>" % i, str(j), local_url)

        if "<" in local_url or ">" in local_url:
            _log.debug("Url not parsed correctly: {0}".format(local_url))

        _log.debug("open url: {0}".format(local_url))
        self.driver.get(local_url)

        self.wait_for_ajax()

        if exists:
            self.exist()

    def hover(self, element):
        raise NotImplementedError("")

    def wait_for_ajax(self, timeout=10):
        """ Wait for Ajax (jQuery) to finish """

        try:
            WebDriverWait(self.driver, timeout).until(lambda driver: driver.execute_script("return jQuery.active == 0"))
        except TimeoutException:
            _log.debug("Timeout waiting for jQuery")

    def __enter__(self):
        return self

    def __exit__(self, expected_type, expected_value, expected_traceback):
        pass
