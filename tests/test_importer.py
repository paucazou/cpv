import sys
sys.path.append('./cpv/')

import importer

def test_import_msx():
    assert importer.import_msx("tests/examples/Example.mscx") == 'CM\n* High one\nC4 4 0\nD4 4 4\nE4 4 8\nFs4 4 12\nG4 4 16\nF4 4 20\nBb4 4 24\nC5 4 28\n* High second\nGss4 4 0\nG4 4 4\nA4 4 8\n* Low one\nC3 4 0\nB2 4 4\nA2 4 12\nAbb2 4 16\nD3 4 20\nEb3 4 24\nC3 4 28\n* Low second\nA3 4 0\nC4 4 4\nA3 4 8\n'
