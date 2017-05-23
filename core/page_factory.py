import logging

_log = logging.getLogger(__name__)


class ViewFactory(object):
    """ View factory creates the view objects
    ::
        
        View = ViewFactory(driver, config)
    
        View("Start").do_action()
    """

    def __init__(self, driver, cfg, views):
        """ Initiate view factory with driver,
        config and available views
        
        :param driver: webdriver
        :param cfg: configuration for application
        :param views: list of dicts with name and class name of view object
                      views = [{"name" : "StartPage", "class" : "StartPage"}]
        """
        self.driver = driver
        self.cfg = cfg
        self.views = views
        self.current_view = None

    def __call__(self, view=None):

        if view is None and self.current_view:
            return self.create(self.current_view)

        d = next((item for item in self.views if item["name"] == view), None)

        if d is None:
            raise TypeError("Page {0} does not exist in context".format(view))
        self.current_view = d
        return self.create(d)

    def create(self, view):
        """ Create a view object from class and
        then instance it with driver and config.
        
        :param view: dict view
        """

        view_class = view['class']
        view = view_class(self.driver, self.cfg)
        return view
