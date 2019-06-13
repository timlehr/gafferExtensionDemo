import os
import unittest

import IECore

import Gaffer
import GafferTest
import GafferDispatch
import GafferDispatchTest
import DemoGafferExtension.TaskAlgo as TaskAlgo


# TestCase class containing tests related to the 'TaskAlgo' submodule.
class TaskAlgoTest( GafferTest.TestCase ):

    # Internal helper, creating a Local dispatcher with temp directory
    def __createLocalDispatcher( self ):

        dispatcher = GafferDispatch.LocalDispatcher()
        dispatcher["jobsDirectory"].setValue( self.temporaryDirectory() )
        return dispatcher

    # Internal helper, creating new text writer at 'fileName'
    def __createTextWriter( self, fileName, text="", mode="a" ):

        node = GafferDispatchTest.TextWriter()
        node["fileName"].setValue( os.path.join( self.temporaryDirectory(), fileName ) )
        node["text"].setValue( text )
        node["mode"].setValue( mode )
        return node

    # Test: Source files in simple node graph
    def testSimpleGraph( self ):

        dispatcher = self.__createLocalDispatcher()

        # create node graph
        s = Gaffer.ScriptNode()
        s["n1"] = self.__createTextWriter( "output.txt" )
        s["n2"] = self.__createTextWriter( "simple2.txt" )
        s["n3"] = self.__createTextWriter( "simple3.txt" )
        s["n4a"] = self.__createTextWriter( "simple4a.txt" )
        s["n4b"] = self.__createTextWriter( "simple4b.txt" )

        s["n1"]["preTasks"][0].setInput( s["n2"]["task"] )
        s["n2"]["preTasks"][0].setInput( s["n3"]["task"] )
        s["n3"]["preTasks"][0].setInput( s["n4a"]["task"] )
        s["n3"]["preTasks"][1].setInput( s["n4b"]["task"] )

        # dispatch graph
        dispatcher.dispatch( [ s["n1"] ] )

        # get results
        result = TaskAlgo.getSourceFilenames( s["n1"]["task"] )
        expected = {
            s["n2"]["fileName"].getValue(),
            s["n3"]["fileName"].getValue(),
            s["n4a"]["fileName"].getValue(),
            s["n4b"]["fileName"].getValue(),
        }

        # assert results
        self.assertEqual( result, expected )
        for path in result:
            self.assertTrue( os.path.exists( path ), "'{}' does not exist.".format( path ) )

    # Test: Source files in simple node graph over a given frame range
    def testFrameRange( self ):

        # create dispatcher with frame range
        frameRangeString = "3-33"
        frameList = IECore.FrameList.parse( frameRangeString )

        dispatcher = self.__createLocalDispatcher()
        dispatcher["framesMode"].setValue( GafferDispatch.Dispatcher.FramesMode.CustomRange )
        dispatcher["frameRange"].setValue( frameRangeString )

        # create node graph
        s = Gaffer.ScriptNode()
        s["nOutput"] = self.__createTextWriter( "output_####.txt" )
        s["nSource"] = self.__createTextWriter( "source_####.txt" )

        s["nOutput"]["preTasks"][0].setInput( s["nSource"]["task"] )

        # dispatch graph
        dispatcher.dispatch( [ s["nOutput"] ] )

        # get results
        expected = set()
        result = set()

        for frame in frameList.asList():
            context = Gaffer.Context( s.context() )
            context.setFrame( frame )
            expected.add( context.substitute( s["nSource"]["fileName"].getValue() ) )
            result.update( TaskAlgo.getSubstitutedSourceFileNames( s["nOutput"]["task"], context=context ) )

        # assert results
        self.assertEqual( result, expected )
        for path in result:
            self.assertTrue( os.path.exists( path ), "'{}' does not exist.".format( path ) )

    # Test: Source files in a simple node graph driven by a wedge node
    def testWedge(self):

        dispatcher = self.__createLocalDispatcher()
        wedgeStrings = [ "wedging", "is", "awesome" ]

        # create node graph
        s = Gaffer.ScriptNode()
        s["writer"] = self.__createTextWriter( "wedge_${wedgeString}.txt" )
        s["wedge"] = GafferDispatch.Wedge()

        s["wedge"]["preTasks"][0].setInput( s["writer"]["task"] )
        s["wedge"]["variable"].setValue( "wedgeString" )
        s["wedge"]["mode"].setValue( int( GafferDispatch.Wedge.Mode.StringList ) )
        s["wedge"]["strings"].setValue( IECore.StringVectorData( wedgeStrings ) )

        # dispatch graph
        dispatcher.dispatch( [ s["wedge"] ] )

        # get results
        expected = set()
        result = set()

        for wedgeString in wedgeStrings:
            context = Gaffer.Context( s.context() )
            context["wedgeString"] = wedgeString
            expected.add( context.substitute( s["writer"]["fileName"].getValue() ) )
            result.update( TaskAlgo.getSubstitutedSourceFileNames( s["wedge"]["task"], context=context ) )

        # assert results
        self.assertEqual( result, expected )
        for path in expected:
            self.assertTrue( os.path.exists( path ), "'{}' does not exist.".format( path ) )

    # Test: Source files in a graph containing a simple subgraph
    def testSubGraph(self):

        dispatcher = self.__createLocalDispatcher()

        # create node graph
        s = Gaffer.ScriptNode()
        s["n1"] = self.__createTextWriter( "output.txt" )
        s["n2"] = self.__createTextWriter( "graphWriter.txt" )
        s["box"] = Gaffer.Box()

        # create subgraph
        s["box"]["boxWriter"] = self.__createTextWriter( "boxWriter.txt" )
        s["box"]["out"] = Gaffer.BoxOut()
        s["box"]["out"]["name"].setValue( "task" )
        s["box"]["out"].setup( s["box"]["boxWriter"]["task"] )
        s["box"]["out"]["in"].setInput( s["box"]["boxWriter"]["task"] )

        # wire nodes
        s["n1"]["preTasks"][0].setInput( s["n2"]["task"] )
        s["n2"]["preTasks"][0].setInput( s["box"]["task"] )

        # dispatch graph
        dispatcher.dispatch( [ s["n1"] ] )

        # get results
        result = TaskAlgo.getSourceFilenames( s["n1"]["task"] )
        expected = {
            s["n2"]["fileName"].getValue(),
            s["box"]["boxWriter"]["fileName"].getValue()
        }

        # assert results
        self.assertEqual( result, expected )
        for path in result:
            self.assertTrue( os.path.exists( path ), "'{}' does not exist.".format( path ) )


if __name__ == "__main__":
    unittest.main()