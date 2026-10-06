"""Bootstrap: put the shared workbook toolkit on the path."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLKIT = os.path.abspath(os.path.join(HERE, "..", "..",
                                       "ChipDesignAssociate", "Module2", "build"))
sys.path.insert(0, TOOLKIT)
sys.path.insert(0, HERE)
