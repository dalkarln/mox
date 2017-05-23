# #
# # Re-write if only base condition is __call__
# # Then it could be used as methods instead
# # def VISIBLE(element):
# #     return ...
# #

import logging
from abc import abstractmethod

_log = logging.getLogger(__name__)


class BaseCondition(object):
    """ Base conditions passed to the wait_for parameter of :class: ``
    """
    def __call__(self, element):
        return self.evaluate(element)

    @abstractmethod
    def evaluate(self, element):
        """ abstract method to be implemented by derived classes
        """
        raise NotImplementedError


class VISIBLE(BaseCondition):
    """ Checks if element is visible """

    def evaluate(self, element):
        return element and element.is_displayed()


class INVISIBLE(BaseCondition):
    """ Checks if element is invisible """

    def evaluate(self, element):
        return not element or not element.is_displayed()


class CLICKABLE(BaseCondition):
    """ Checks if element is clickable """

    def evaluate(self, element):
        return element and element.is_enabled()
