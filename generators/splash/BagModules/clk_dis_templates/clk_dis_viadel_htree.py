# -*- coding: utf-8 -*-
########################################################################################################################
#
# Copyright (c) 2014, Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#   disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################################################################

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
# noinspection PyUnresolvedReferences,PyCompatibility
from builtins import *

import os
import pkg_resources

from bag.design import Module


yaml_file = pkg_resources.resource_filename(__name__, os.path.join('netlist_info', 'clk_dis_viadel_htree.yaml'))


# noinspection PyPep8Naming
class clk_dis_templates__clk_dis_viadel_htree(Module):
    """Module for library clk_dis_templates cell clk_dis_viadel_htree.

    Fill in high level description here.
    """

    def __init__(self, bag_config, parent=None, prj=None, **kwargs):
        Module.__init__(self, bag_config, yaml_file, parent=parent, prj=prj, **kwargs)

    def design(self, lch, pw, nw, m_dff=2, m_inv1=4, m_inv2=8, m_tgate=4, n_pd=4, m_capsw=2, num_bits=5, num_ways=8, unit_cell=1, clock_pulse='False', device_intent='fast'):
        """To be overridden by subclasses to design this module.

        This method should fill in values for all parameters in
        self.parameters.  To design instances of this module, you can
        call their design() method or any other ways you coded.

        To modify schematic structure, call:

        rename_pin()
        delete_instance()
        replace_instance_master()
        reconnect_instance_terminal()
        restore_instance()
        array_instance()
        """
        self.parameters['lch'] = lch
        self.parameters['pw'] = pw
        self.parameters['nw'] = nw
        self.parameters['m_dff'] = m_dff
        self.parameters['m_inv1'] = m_inv1
        self.parameters['m_inv2'] = m_inv2
        self.parameters['m_tgate'] = m_tgate
        self.parameters['n_pd'] = n_pd
        self.parameters['m_capsw'] = m_capsw
        self.parameters['num_bits'] = num_bits
        self.parameters['num_ways'] = num_ways
        self.parameters['unit_cell'] = unit_cell
        self.parameters['device_intent'] = device_intent
        self.parameters['clock_pulse'] = clock_pulse


        self.instances['I0'].design(lch=lch, pw=pw, nw=nw, m_dff=m_dff, m_inv1=m_inv1, m_inv2=m_inv2,
            m_tgate=m_tgate, n_pd=n_pd, m_capsw=m_capsw, num_bits=num_bits, unit_cell=unit_cell, clock_pulse=clock_pulse, device_intent=device_intent, num_ways=num_ways)    #viadel

        self.rename_pin('CLKO','CLKO<%d:0>'%(num_ways-1))
        self.rename_pin('DATAO','DATAO<%d:0>'%(num_ways-1))
        self.reconnect_instance_terminal('I0', 'CLKO<%d:0>'%(num_ways-1), 'CLKO<%d:0>'%(num_ways-1))
        self.reconnect_instance_terminal('I0', 'DATAO<%d:0>'%(num_ways-1), 'DATAO<%d:0>'%(num_ways-1))

        #for i in range(num_ways):
        #    self.rename_pin('CAL'+str(i),'CLKCAL'+str(i)+'<%d:0>'%(num_bits-1))
        #    self.reconnect_instance_terminal('I0', 'CAL'+str(i), 'CLKCAL'+str(i)+'<%d:0>'%(num_bits-1))
        cal_pn=','.join(['CLKCAL'+str(i)+'<%d:0>'%(num_bits-1) for i in range(num_ways)])
        cal_pn_term=','.join(['CLKCAL'+str(i)+'<%d:0>'%(num_bits-1) for i in range(num_ways)])
        clk_pn=''
        for i in range(num_ways):
            #cal_pn+='CLKCAL'+str(i)+'<%d:0>,'%(num_bits-1)
            if i%2==0:
                clk_pn+='CLKIN,'
            else: 
                clk_pn+='CLKIP,'
        #cal_pn=cal_pn[:-1]
        clk_pn=clk_pn[:-1]
        self.rename_pin('CAL0',cal_pn)
        self.reconnect_instance_terminal('I0', cal_pn_term, cal_pn)
        self.reconnect_instance_terminal('I0', 'CLKI<%d:0>'%(num_ways-1), clk_pn)



    def get_layout_params(self, **kwargs):
        """Returns a dictionary with layout parameters.

        This method computes the layout parameters used to generate implementation's
        layout.  Subclasses should override this method if you need to run post-extraction
        layout.

        Parameters
        ----------
        kwargs :
            any extra parameters you need to generate the layout parameters dictionary.
            Usually you specify layout-specific parameters here, like metal layers of
            input/output, customizable wire sizes, and so on.

        Returns
        -------
        params : dict[str, any]
            the layout parameters dictionary.
        """
        return {}

    def get_layout_pin_mapping(self):
        """Returns the layout pin mapping dictionary.

        This method returns a dictionary used to rename the layout pins, in case they are different
        than the schematic pins.

        Returns
        -------
        pin_mapping : dict[str, str]
            a dictionary from layout pin names to schematic pin names.
        """
        return {}
