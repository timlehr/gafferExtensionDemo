import functools
import os
import sys
import importlib

import Gaffer
import GafferUI

def __exportAsExtension( graphEditor, box ):

    extName = GafferUI.TextInputDialogue(
        title="Extension Name",
        confirmLabel="Export",
        initialText=box.getName()
    ).waitForText(parentWindow=graphEditor.graphGadgetWidget().ancestor( GafferUI.ScriptWindow ))

    if not extName:
        return

    # export extension
    extensionDir = os.path.expanduser(os.path.join("~/gaffer/extensions/{}/".format(extName)))
    Gaffer.ExtensionAlgo.exportExtension(extName, [box], extensionDir)

    # add extension to path
    sys.path.append(os.path.join(extensionDir, "python"))

    # run startup code to register UI
    app = graphEditor.graphGadgetWidget().ancestor( Gaffer.ApplicationRoot )
    startupPaths = os.environ["GAFFER_STARTUP_PATHS"]
    try:
        os.environ["GAFFER_STARTUP_PATHS"] = os.path.join(extensionDir, "startup")
        app._executeStartupFiles("gui")
    finally:
        os.environ["GAFFER_STARTUP_PATHS"] = startupPaths

def __boxGraphEditorContextMenu( graphEditor, node, menuDefinition ):

    if not isinstance( node, Gaffer.Box ) :
        return

    menuDefinition.append(
        "/Export Box as Extension",
        {
            "command" : functools.partial( __exportAsExtension, graphEditor, node ),
            "active" : True,
        }
    )

GafferUI.GraphEditor.nodeContextMenuSignal().connect( __boxGraphEditorContextMenu, scoped = False )