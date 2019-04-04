# Gole, Karteek
# kpg3522
# 2019-02-04

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2019 Spring semester.

#----------------------------------------------------------------------
class cl_world :
  def __init__( self, objects = [], canvases = [] ) :
    self.objects = objects
    self.canvases = canvases

  def add_canvas( self, canvas ) :
    self.canvases.append( canvas )
    canvas.world = self

  def reset( self ) :
    self.objects = []
    for canvas in self.canvases :
      canvas.delete( 'all' )

  def create_graphic_objects( self, canvas, model ) :
    f = model.getFaces()
    for face in f:
      vert1 = model.getTransformedVertex(face[0])
      vert2 = model.getTransformedVertex(face[1])
      vert3 = model.getTransformedVertex(face[2])
      self.objects.append(canvas.create_line(vert1[0], vert1[1], vert2[0], vert2[1] ))
      self.objects.append(canvas.create_line(vert2[0], vert2[1], vert3[0], vert3[1]))
      self.objects.append(canvas.create_line(vert3[0], vert3[1], vert1[0], vert1[1]))

  def redisplay( self, canvas, event ) :
    pass
    # if self.objects :
    #   canvas.coords(self.objects[ 0 ], 0, 0, event.width, event.height )
    #   canvas.coords(self.objects[ 1 ], event.width, 0, 0, event.height )
    #   canvas.coords(self.objects[ 2 ],
    #     int( 0.25 * int( event.width ) ),
    #     int( 0.25 * int( event.height ) ),
    #     int( 0.75 * int( event.width ) ),
    #     int( 0.75 * int( event.height ) ) )

#----------------------------------------------------------------------
