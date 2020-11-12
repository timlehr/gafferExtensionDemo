import IECore

import Gaffer
import GafferSceneUI

import DemoGafferExtension

print "*** REGISTERED ***"

Gaffer.Metadata.registerNode(

    DemoGafferExtension.AkaArnoldRenderPreview,

    "description",
    """
    Wraps the Interactive Arnold Preview node with a catalogue to go along with it, because everything else is nuts.
    """,

    plugs = {
        "state" : [

			"description",
			"""
			Turns the rendering on and off, or pauses it.
			""",

			"label", "Render",
			"plugValueWidget:type", "GafferSceneUI.InteractiveRenderUI._StatePlugValueWidget",
			"layout:section", "Render",
		],

		"imageIndex" : [

			"description",
			"""
			Specifies the index of the currently
			selected image. This forms the output
			from the catalogue node.
			""",

			"plugValueWidget:type", "GafferImageUI.CatalogueUI._ImageListing",
			"label", "",
			"layout:section", "Render.Images",

		],

		"messages" : [

			"description",
			"""
			Messages from the render process.
			""",

			"label", "Messages",
			"plugValueWidget:type", "GafferSceneUI.InteractiveRenderUI._MessagesPlugValueWidget",
			"layout:section", "Render.Log",
			"nodule:type", "",

		],

    },

)
