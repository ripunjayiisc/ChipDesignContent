"""Bootstrap for the Module 3 Topic 1 build scripts.

Points CDA_IMG_DIR at this topic's img/ and puts the shared presentation
toolkit on the import path. The toolkit (dsl.py, deckkit.py, wbkit.py,
checkfit.py, render.sh) lives in Module2/build/ because that is where it was
first written; it is course-wide, not Module-2-specific, and every module's
build scripts import it from there so a fix to the design system reaches all
of them.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("CDA_IMG_DIR", os.path.join(HERE, "img"))
os.makedirs(os.environ["CDA_IMG_DIR"], exist_ok=True)

TOOLKIT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "Module2", "build"))
if not os.path.isdir(TOOLKIT):
    raise RuntimeError("shared toolkit not found at %s" % TOOLKIT)

sys.path.insert(0, TOOLKIT)      # dsl.py, deckkit.py, wbkit.py
sys.path.insert(0, HERE)
