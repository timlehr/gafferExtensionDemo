import unittest

import Gaffer
import GafferUI
import GafferScene
import GafferSceneUI
import GafferImage

import DemoGafferExtension
import DemoGafferExtensionUI

import GafferUITest

class DocumentationTest( GafferUITest.TestCase ) :

    def test( self ) :

		self.maxDiff = None
		self.assertNodesAreDocumented(
			DemoGafferExtension,
			additionalTerminalPlugTypes = ( GafferScene.ScenePlug, GafferImage.ImagePlug )
		)

if __name__ == "__main__":
	unittest.main()
