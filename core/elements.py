import logging

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, \
    StaleElementReferenceException


_log = logging.getLogger(__name__)


class BaseElement(object):
    """ Base element class for web element
    
    :param locator: locator of element
    :param timeout: time to wait for element in seconds
    :param wait_for: a wait for condition serving as an extra validation
    """

    def __init__(self, locator, timeout=None, wait_for=lambda el: el is not None):
        self.locator = locator
        self.timeout = timeout
        self.wait_for = wait_for
        self._root = lambda: None
        self.base_element = None

    @property
    def root(self):
        return self._root()

    @root.setter
    def root(self, value):
        self._root = value

    def __get__(self, instance, cls):

        if instance is None:
            return self

        if self.base_element is None:
            self.root = lambda: instance.driver
        else:
            self.root = self.base_element

        if self.timeout:

            def callback(_):
                return self.wait_for(self.root.find_element_by_locator(self.locator))
            try:
                WebDriverWait(
                    self.root, self.timeout, ignored_exceptions=[StaleElementReferenceException, ]
                ).until(callback)
            except TimeoutException, NoSuchElementException:
                _log.debug("Unable to find element located by {0}".format(self.locator))
                # removed raise and return None instead
                return None

        return self.root.find_element_by_locator(self.locator)


class BaseElements(object):
    """ Base elements class for web elements
    
    :param locator: locator of element
    :param timeout: time to wait for element in seconds
    :param wait_for: a wait for condition serving as an extra validation
    
    :return: WebElement :class: ``
    """

    def __init__(self, locator, timeout=None, wait_for=lambda el: len(el) > 0):
        self.locator = locator
        self.timeout = timeout
        self.wait_for = wait_for
        self._root = lambda: None
        self.base_element = None

    @property
    def root(self):
        return self._root()

    @root.setter
    def root(self, value):
        self._root = value

    def __get__(self, instance, cls):


        if instance is None:
            return self

        if self.base_element is None:
            self.root = lambda: instance.driver
        else:
            self.root = self.base_element
        '''
        if self.root is None:
            self.root = lambda: instance.driver
        '''
        if self.timeout:

            def callback(_):
                return self.wait_for(self.root.find_elements_by_locator(self.locator))

            try:
                WebDriverWait(
                        self.root, self.timeout, ignored_exceptions=[StaleElementReferenceException, ]
                    ).until(callback)
            except TimeoutException:
                _log.debug("Unable to find elements located by {0}".format(self.locator))
                raise
        return self.root.find_elements_by_locator(self.locator)

    def __getitem__(self, index):
        return lambda: self.__get__(self, self.__class__)[index]
