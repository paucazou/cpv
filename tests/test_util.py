import sys
sys.path.append('./cpv')

import pytest
import util

def test_push_to_end():
    fun = util.push_to_end
    l = [1,2,3]
    assert fun(l) == [2,3,1]
    assert fun([1]) == [1]
    with pytest.raises(AssertionError):
        fun([])

