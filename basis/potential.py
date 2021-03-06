"""Defines a class and methods for evaluating 1D potentials.
"""
import numpy as np
from basis import msg
class Potential(object):
    """Represents a 1D potential.
    Args:
        potcfg (str): path to the potential config file.
    Attributes:
        filepath (str): absolute path to the file that this potential
          represents.
        params (dict): keys are parameter names; values are
          python-evaluated objects.
        regions (dict): keys are a tuple (:class:`float`,
            :class:`float`) that specify the start and end of the region; 
	    values are either functions or variables to define the 
	    potential's value in that region.
        parser (ConfigParser): parses the potential config file.
    Examples:
        >>> from basis.potential import Potential
        >>> import numpy as np
        >>> x = np.linspace(-2, 2, 100)
        >>> pot = Potential("sho.cfg")
        >>> V = pot.evaluate(x)
        >>> V = pot(x)
    """
    def __init__(self, potcfg):
        from os import path
        self.filepath = path.abspath(path.expanduser(potcfg))
        self.params = {}
        self.regions = {}
        self.parser = None
        
        self._parse_config()

    def __getattr__(self, attr):
        if attr in self.params:
            return self.params[attr]
        else:
            emsg = "{} is not an attribute of the Potential object."
            raise AttributeError(emsg.format(attr))            
        
    def __call__(self, value):
        """Evaluates the potential for the given value(s).
        Args:
            value (numpy.ndarray or float): where to evaluate.
        Returns:
            numpy.ndarray or float: potential evaluated at `value`.
        
        Raises:
            ValueError: if the argument is not as `int` or `float`.
        """
        if isinstance(value, list) or isinstance(value, np.ndarray):
            return np.array(list(map(self, value)))

        if not isinstance(value, (int, float)):
            raise ValueError("Only `int` and `float` values can be "
                             "evaluated by the potential.")

        for xi, xf in self.regions:
            if value >= xi and value < xf:
                function = self.regions[(xi, xf)]
                if hasattr(function, "__call__"):
                    return function(value)
                else:
                    return function
        else:
            return 0.    

    def __mul__(self, value): #pragma: no cover
        """Increases the strength of the potential by `value`.
        
        Args:
            value (float): how much to multiply by.
        """
        #Do I want to overwrite the value of 'strength' 
	#or return a new Potential instance?
        pass
        
    def _parse_params(self):
        """Extracts the potential params from the specified 
	config parser.
        """
        if self.parser.has_section("parameters"):
            for param, svalue in self.parser.items("parameters"):
                self.params[param] = eval(svalue)

    def adjust(self, **kwargs):
        """Adjusts the parameters of the potential.
        Args:
            kwargs (dict): parameters and values to overwrite.
        Notes:
            if a parameter is specified that was not originally defined in
            the potential config file, the update is ignored. A warning is
            printed that can be seen if verbosity is enabled.
        """
        for k, v in kwargs.items():
            if k in self.params:
                self.params[k] = v
            else:
                wmsg = "'{}' is not a valid parameter for '{}'." #pragma: no cover
                msg.warn(wmsg.format(k, self.filepath))	#pragma: no cover
        self._parse_regions()

    def _parse_regions(self):
        """Parses the potential's region specifications from config.
        """
        if not self.parser.has_section("regions"):
            raise ValueError("[regions] is required to define a potential.") #pragma: no cover
        self.regions = {}
        
        for i, spec in self.parser.items("regions"):
            domain, sfunc = spec.split('|')
            if "numpy" in sfunc and "numpy" not in self.params:
                import numpy as np #pragma: no cover
                self.params["numpy"] = np #pragma: no cover
            if "operator" in sfunc and "operator" not in self.params:
                import operator
                self.params["operator"] = operator
            xi, xf = eval(domain, self.params)
            function = eval(sfunc, self.params)
            self.regions[(xi, xf)] = function
                
    def _parse_config(self):
        """Parses the potential config file to initialize the
        parameters and function call.
        """
        try:
            from ConfigParser import ConfigParser
        except ImportError:  #pragma: no cover
            from configparser import ConfigParser #pragma: no cover

        self.parser = ConfigParser()
        with open(self.filepath) as f:
            self.parser.readfp(f)
            
        self._parse_params()
        self._parse_regions()
