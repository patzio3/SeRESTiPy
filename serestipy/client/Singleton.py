#!/usr/bin/env  python3
#@file   Singleton.py
#
#@date   Feb 10, 2022
#@author Patrick Eschenbach
#@copyright \n
# This file is part of the program SeRESTiPy.\n\n
# SeRESTiPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.\n\n
# SeRESTiPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.\n\n
# You should have received a copy of the GNU Lesser General
# Public License along with SeRESTiPy.
# If not, see <http://www.gnu.org/licenses/>.\n

##@brief A non-thread-safe helper class to ease implementing singletons.
# This should be used as a decorator -- not a metaclass -- to the
# class that should be a singleton.
# 
# The decorated class can define one `__init__` function that
# takes only the `self` argument. Also, the decorated class cannot be
# inherited from. Other than that, there are no restrictions that apply
# to the decorated class.
# 
# To get the singleton instance, use the `getInstance` method. Trying
# to use `__call__` will result in a `TypeError` being raised.
# https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
class Singleton:
    def __init__(self, decorated):
        self._decorated = decorated

    ##@brief Returns the singleton instance. Upon its first call, it creates a
    # new instance of the decorated class and calls its `__init__` method.
    # On all subsequent calls, the already created instance is returned.
    def getInstance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `getInstance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)