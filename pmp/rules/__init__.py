from .._common import introspect_func

from .rule import Rule
from .weakly_separable import WeaklySeparable
from .bloc import Bloc
from .borda import Borda
from .sntv import SNTV
from .chamberlin_courant import ChamberlinCourant
from .pav import PAV

rules_list = introspect_func(__name__, Rule)
