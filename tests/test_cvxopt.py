#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2021 Stéphane Caron <stephane.caron@normalesup.org>
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

import cvxopt
import numpy as np
import unittest
import warnings

from typing import Tuple

import scipy

from numpy import array, ones
from numpy.linalg import norm
from scipy.sparse import csc_matrix

from qpsolvers import solve_qp
from qpsolvers.solvers.cvxopt_ import cvxopt_matrix


class TestCVXOPT(unittest.TestCase):

    """
    Test fixture for the CVXOPT solver.
    """

    def setUp(self):
        """
        Prepare test fixture.
        """
        warnings.simplefilter("ignore", category=UserWarning)

    def get_sparse_problem(
        self,
    ) -> Tuple[cvxopt.matrix, np.ndarray, cvxopt.matrix, np.ndarray]:
        """
        Get sparse problem as a quadruplet of values to unpack.

        Returns
        -------
        P : cvxopt.matrix
            Symmetric quadratic-cost matrix .
        q : numpy.ndarray
            Quadratic-cost vector.
        G : cvxopt.matrix
            Linear inequality matrix.
        h : numpy.ndarray
            Linear inequality vector.
        """
        n = 150
        M = scipy.sparse.lil_matrix(scipy.sparse.eye(n))
        for i in range(1, n - 1):
            M[i, i + 1] = -1
            M[i, i - 1] = 1
        P = cvxopt_matrix(csc_matrix(M.dot(M.transpose())))
        q = -ones((n,))
        G = cvxopt_matrix(csc_matrix(-scipy.sparse.eye(n)))
        h = -2.0 * ones((n,))
        return P, q, G, h

    def test_sparse(self):
        P, q, G, h = self.get_sparse_problem()
        x = solve_qp(P, q, G, h, solver="cvxopt")
        self.assertIsNotNone(x)
        known_solution = array([2.0] * 149 + [3.0])
        self.assertTrue(norm(x - known_solution) < 1e-2)  # aouch, not great!
        self.assertTrue(max(G * cvxopt_matrix(x) - cvxopt_matrix(h)) <= 1e-10)


if __name__ == "__main__":
    unittest.main()
