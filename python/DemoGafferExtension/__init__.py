__import__( "Gaffer" )
__import__( "GafferScene" )

from _DemoGafferExtension import *

import TaskAlgo
from AkaArnoldRenderPreview import AkaArnoldRenderPreview

__import__( "IECore" ).loadConfig( "GAFFER_STARTUP_PATHS", subdirectory = "DemoGafferExtension" )
