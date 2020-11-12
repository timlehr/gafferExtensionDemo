import IECore

import Gaffer
import GafferArnold
import GafferImage

class AkaArnoldRenderPreview(Gaffer.SubGraph):

    def __init__(self, name="AkaArnoldRenderPreview"):
        super(AkaArnoldRenderPreview, self).__init__(name)

        # create new nodes in Subgraph, in two different ways
        previewNode = GafferArnold.InteractiveArnoldRender("ArnoldIPR")
        self.addChild( previewNode )
        self['catalogue'] = GafferImage.Catalogue()

        # Promote the plugs we want to our new node
        # Note: There is also Gaffer.PlugAlgo.promoteWithName( renderNode["in"], name = "promotedIn" )
        Gaffer.PlugAlgo.promote(previewNode["in"])
        Gaffer.PlugAlgo.promote(self['catalogue']["out"])

        # some plugs can't be serialized so we manually recreate them, make sure to keep them non-serializable
        self.addChild(Gaffer.IntPlug("state", defaultValue = 0, minValue = 0, maxValue = 2, flags = Gaffer.Plug.Flags.Default & ~Gaffer.Plug.Flags.Serialisable, ))
        self.addChild(Gaffer.IntPlug( "imageIndex", defaultValue = 0, flags = Gaffer.Plug.Flags.Default & ~Gaffer.Plug.Flags.Serialisable, ))
        self.addChild(Gaffer.ObjectPlug("messages", direction = Gaffer.Plug.Direction.Out, defaultValue = Gaffer.Private.IECorePreview.MessagesData(), flags = Gaffer.Plug.Flags.Default & ~Gaffer.Plug.Flags.Serialisable, ))

        # Promote plugs by wiring them up manually
        previewNode["state"].setInput(self["state"])
        self["messages"].setInput(previewNode["messages"])
        self["catalogue"]["imageIndex"].setInput(self["imageIndex"])

IECore.registerRunTimeTyped(AkaArnoldRenderPreview)
