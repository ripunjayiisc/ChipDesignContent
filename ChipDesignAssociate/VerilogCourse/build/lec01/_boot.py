"""Bootstrap: put the shared toolkit on the path and point it at this lecture's img/."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("CDA_IMG_DIR", os.path.join(HERE, "img"))
os.makedirs(os.environ["CDA_IMG_DIR"], exist_ok=True)
# the shared toolkit (dsl.py, deckkit.py, wbkit.py) lives in Module2/build
TOOLKIT = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                       "Module2", "build"))
sys.path.insert(0, TOOLKIT)
sys.path.insert(0, HERE)
