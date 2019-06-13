# Submodule containing a set of functions to list upstream dependencies of TaskNodes.

import Gaffer

# Set containing plugs with file paths
_filePlugNames = { "fileName" }

# Helper function to retrieve upstream nodes starting from 'entryNode'.
# This function omits the entry node, returning only upstream dependencies as a set.
def _getUpstreamNodes( entryNode ):

    upstreamNodes = set()

    def __traverseHierarchy( parent ):
        # iterate over child plugs, add relevant upstream nodes to set
        for childPlug in parent.children( Gaffer.Plug ):
            if childPlug.source() and childPlug.direction() == Gaffer.Plug.Direction.In:
                inputNode = childPlug.source().node()
                if inputNode != entryNode and inputNode not in upstreamNodes:
                    upstreamNodes.add( inputNode )
                    __traverseHierarchy( inputNode )
            __traverseHierarchy( childPlug )

    # traverse upstream from entry node
    __traverseHierarchy( entryNode )

    return upstreamNodes

# Returns a set containing all dependent source file names upstream of 'outputTaskPlug'.
# This excludes any file names on the queried node, as they are not considered dependencies.
# The file names are retrieved from the plugs defined in '_filePlugNames'.
# If a plug name matches a name in the plug name set, the value will be retrieved and added to the result set.
def getSourceFilenames( outputTaskPlug ):

    sourceFileNames = set()

    for node in _getUpstreamNodes( outputTaskPlug.node() ):
        plugNames = { plug.getName() for plug in node.children( Gaffer.Plug ) }
        intersection = _filePlugNames.intersection( plugNames )
        plugValues = [ node.getChild( plugName ).getValue() for plugName in intersection if node.getChild(plugName) ]
        sourceFileNames.update( plugValues )

    return sourceFileNames

# Returns a set containing all dependent source file names upstream of 'outputTaskPlug'.
# This excludes any file names on the queried node, as they are not considered dependencies.
# Variables in file names are substituted using the provided 'context'.
def getSubstitutedSourceFileNames( outputTaskPlug, context ):

    return { context.substitute( fileName ) for fileName in getSourceFilenames( outputTaskPlug ) }
