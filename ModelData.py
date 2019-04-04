# Gole, Karteek
# kpg3522
# 2019-02-04

import sys
import constructTransform

class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []
    self.xmin = self.ymin = self.zmin = float('inf')
    self.xmax = self.ymax = self.zmax = float('-inf')
    self.ax =self.ay = self.sx = self.sy = float(0.0)

    if inputFile is not None :
      # File name was given.  Read the data from the file.
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :
    # Read each line of the file.
    with open(inputFile, 'r') as fp:
      lines = fp.read().replace('\r', '').split('\n')

    for (index, line) in enumerate(lines, start=1):
      line = line.strip()

      # Ignore any blank line (or line that's only whitespace characters).
      if len(line) == 0:
        continue
      # Ignore any line that starts with a #.
      if line.startswith('#'):
        continue



      # For the remaining lines, if the line starts with:
      #  f -- Append the three integers as a tuple to self.m_Faces.
      elif line.startswith('f'):
        fface = []
        face = line.replace('f', '').split()
        try:
          for f_face in face:
            f = int(f_face)
            fface.append(f - 1)
          f_arr = tuple(fface)
          if len(f_arr) > 3:
            print("Line " + str(index) + " is a malformed face spec.")
          else:
            self.m_Faces.append(f_arr)
        except ValueError:
          print("Line " + str(index) + " is a malformed face spec.")
      #  v -- Append the three floats as a tuple to self.m_Vertices.
      elif line.startswith('v'):
        vvertice = []
        vertex = line.replace('v', '').split()
        try:
          for v_vertice in vertex:
            v = float(v_vertice)
            vvertice.append(v)
          v_arr = tuple(vvertice)

          if len(v_arr) > 3:
            print("Line " + str(index) + " is a malformed vertex spec.")
          else:
            if(self.xmin > v_arr[0]):
              self.xmin = v_arr[0]
            if(self.xmax < v_arr[0]):
              self.xmax = v_arr[0]
            if (self.ymin > v_arr[1]):
              self.ymin = v_arr[1]
            if (self.ymax < v_arr[1]):
              self.ymax = v_arr[1]
            if (self.zmin > v_arr[2]):
              self.zmin = v_arr[2]
            if (self.zmax < v_arr[2]):
              self.zmax = v_arr[2]
            self.m_Vertices.append(v_arr)
        except ValueError:
          print("Line " + str(index) + " is a malformed vertex spec.")
      #  w -- Keep the four floats as a tuple in self.m_Window.
      elif line.startswith('w'):
        if len(self.m_Window) != 0:
          print("Line " + str(index) + " is a duplicate window spec.")
        wwin = []
        window = line.replace('w', '').split()
        try:
          for win_window in window:
            w = float(win_window)
            wwin.append(w)
          w_arr = tuple(wwin)
          if len(w_arr) > 4:
            print("Line " + str(index) + " is a malformed window spec.")
          else:
            self.m_Window = w_arr
        except ValueError:
          print("Line " + str(index) + " is a malformed window spec.")
      #  s -- Keep the four floats as a tuple in self.m_Viewport.
      elif line.startswith('s'):
        if len(self.m_Viewport) != 0:
          print("Line " + str(index) + " is a duplicate viewport spec.")
        sview = []
        viewport = line.replace('s', '').split()
        try:
          for s_viewport in viewport:
            s = float(s_viewport)
            sview.append(s)
          s_arr = tuple(sview)
          if len(s_arr) > 4:
            print("Line " + str(index) + " is a malformed viewport spec.")
          else:
            self.m_Viewport = s_arr
        except ValueError:
          print("Line " + str(index) + " is a malformed viewport spec.")

      else:
        print("Line " + str(index) + " starts with different character.")

  def getBoundingBox( self ) :
    return (self.xmin,self.xmax,self.ymin,self.ymax,self.zmin,self.zmax)

  def specifyTransform( self, ax, ay, sx, sy ) :
    self.ax = ax
    self.ay = ay
    self.sx = sx
    self.sy = sy

  def getTransformedVertex( self, vNum ) :
    x = self.m_Vertices[vNum][0]
    y = self.m_Vertices[vNum][1]
    z = self.m_Vertices[vNum][2]
    xp = self.sx*x + self.ax
    yp = self.sy*y + self.ay
    zp = z*0
    return (xp,yp,zp)

  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window

def _main() :
  # Get the file name to load and the canvas size.
  fName  = sys.argv[1]
  width  = int( sys.argv[2] )
  height = int( sys.argv[3] )

  # Create a ModelData object to hold the model data from
  # the supplied file name.
  model = ModelData( fName )

  # Now that it's loaded, print out a few statistics about
  # the model data that we just loaded.
  print( "%s: %d vert%s, %d face%s" % (
    fName,
    len( model.getVertices() ), 'ex' if len( model.getVertices() ) == 1 else 'ices',
    len( model.getFaces() ), '' if len( model.getFaces() ) == 1 else 's' ))

  print( 'First 3 vertices:' )
  for v in model.getVertices()[0:3] :
    print( '     ', v )

  print( 'First 3 faces:' )
  for f in model.getFaces()[0:3] :
    print( '     ', f )

  w = model.getWindow()
  v = model.getViewport()
  print( 'Window line:', w )
  print( 'Viewport line:', v )
  print('Canvas size:', width, height)

  print( 'Bounding box:', model.getBoundingBox() )

  ( ax, ay, sx, sy ) = constructTransform.constructTransform( w, v, width, height )
  print( f'Transform is {ax} {ay} {sx} {sy}' )

  model.specifyTransform( ax, ay, sx, sy )

  print( 'First 3 transformed vertices:' )
  for vNum in range( 3 ) :
    print( '     ', model.getTransformedVertex( vNum ) )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
