#!/usr/bin/python

#         __________________________
#         |____C_O_P_Y_R_I_G_H_T___|
#         |                        |
#         |  (c) NIWA, 2008-2010   |
#         | Contact: Hilary Oliver |
#         |  h.oliver@niwa.co.nz   |
#         |    +64-4-386 0461      |
#         |________________________|


# asynchronous tasks: cycle time required for some operations, at least for now, so give all 
# the time of 2999010101 but never change it.

import sys, re
from task import task
from mod_nopid import nopid

class asynchronous_task( nopid, task ):

    used_outputs = {}
    
    quick_death = True

    def __init__( self, state, no_reset ):
        # Call this AFTER derived class initialisation

        # Derived class init MUST define:
        #  * prerequisites and outputs
        #  * self.env_vars 

        # Top level derived classes must define:
        #   self.id 
        #   <class>.instance_count = 0

        task.__init__( self, state, no_reset )

    def next_tag( self ):
        return str( int( self.tag ) + 1 )

    def check_requisites( self ):
        for message in self.prerequisites.get_satisfied_list():
            # record which outputs already been used by this task type
            self.__class__.used_outputs[ message ] = True

            if message in self.prerequisites.match_group.keys():
                # IS THIS TOP LEVEL 'IF' NECESSARY?
                mg = self.prerequisites.match_group[ message ]

                for output in self.outputs.get_list():
                    m = re.match( '^(.*)\((.*)\)(.*)', output )
                    if m:
                        (left, mid, right) = m.groups()
                        newout = left + mg + right

                        del self.outputs.satisfied[ output ]
                        self.outputs.satisfied[ newout ] = False

                        self.env_vars[ 'ASYNCID' ] = mg 

                for deathpre in self.death_prerequisites.get_list():
                    m = re.match( '^(.*)\((.*)\)(.*)', deathpre )
                    if m:
                        (left, mid, right) = m.groups()
                        newpre = left + mg + right

                        del self.death_prerequisites.satisfied[ deathpre ]
                        self.death_prerequisites.satisfied[ newpre ] = False

        # if task is asynchronous it has
        #  - used_outputs
        #  - loose prerequisites
        #  - death prerequisites

    def satisfy_me( self, outputs ):
        self.prerequisites.satisfy_me( outputs, self.__class__.used_outputs.keys() )
        self.death_prerequisites.satisfy_me( outputs )
