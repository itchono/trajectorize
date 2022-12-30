class FakeBody:
    '''
    Defines a body with a monkey-patched mu attribute which behaves like a
    Body from the kerbol_system module.
    '''

    def __init__(self, mu):
        self.mu = mu


EARTH_SI = FakeBody(3.986004418e14)
EARTH_KM = FakeBody(3.986004418e5)
