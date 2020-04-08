'''
Class for util.
'''


import random
import numpy as np
from item import Item
from vote import Vote, ApprovalVote
from items import Items
from votes import Votes
from election import Election


class Util:
    '''
    Util.
    '''


    @staticmethod
    def check_approval_election(election):
        pass


    @staticmethod
    def check_unitcost_election(election):
        pass


    @staticmethod
    def dist(pos1, pos2):
      return(((pos1.x() - pos2.x())**2 + (pos1.y() - pos2.y())**2)**(0.5))
