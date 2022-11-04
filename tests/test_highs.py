#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2022 Stéphane Caron and the qpsolvers contributors.
#
# This file is part of qpsolvers.
#
# qpsolvers is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# qpsolvers is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with qpsolvers. If not, see <http://www.gnu.org/licenses/>.

import unittest
import warnings

from qpsolvers import solve_qp

from .problems import get_sd3310_problem


class TestHiGHS(unittest.TestCase):

    """
    Test fixture for the HiGHS solver.
    """

    def setUp(self):
        """
        Prepare test fixture.
        """
        warnings.simplefilter("ignore", category=UserWarning)

    def test_highs_tolerances(self):
        P, q, G, h, A, b = get_sd3310_problem()
        x = solve_qp(
            P,
            q,
            G,
            h,
            A,
            b,
            solver="highs",
            time_limit=0.1,
            primal_feasibility_tolerance=1e-1,
            dual_feasibility_tolerance=1e-1,
        )
        self.assertIsNotNone(x)