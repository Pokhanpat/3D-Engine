import pygame
from _math import *
#_math is basic math functions

#TO DO:
#Add object movement and rotation
#Make Potential child classes of object like cube and pyramid
#Make a game lmao

#3D vector class, useful for storing 3D points and performing calculations on them.
class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    #Returns the magnitude (Distance from 0) of the vector
    def mag(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    #Normalizes the vector (shortents it to have a length of 1, while retaining the angle it's facing)
    def normalize(self):
        return self.__truediv__(self.mag())
    #Basic Vector Operations
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
        
    def __add__(self, v):
        return Vector3(self.x + v.x, self.y + v.y, self.z + v.z)
    
    def __sub__(self, v):
        return Vector3(self.x - v.x, self.y - v.y, self.z - v.z)

    def __mul__(self, n):
        return Vector3(self.x * n, self.y * n, self.z * n)

    def __truediv__(self, n):
        return Vector3(self.x / n, self.y / n, self.z / n)
    #Cross product of 2 vectors, useful for calculating surface normals
    def cross(self, v):
        return Vector3((self.y * v.z) - (self.z * v.y), (self.z * v.x) - (self.x * v.z), (self.x * v.y) - (self.y * v.x))
    #Dot product of 2 vectors, useful for calcuating angles and reflections/projections.
    def dot(self, v):
        return self.x*v.x + (self.y*v.y) + (self.z*v.z)
    #Returns the distance between 2 vectors
    def dist(self, v):
        return sqrt((self.x - v.x)**2 + (self.y - v.y)**2 + (self.z - v.z)**2)
    
#2D Vector Class, used less but still important.
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    #Same stuff as 3D Vector, but 2D
    def mag(self):
        return sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        return self.__div__(self.mag())
    
    def __add__(self, v):
        return Vector2(self.x + v.x, self.y + v.y)
    
    def __sub__(self, v):
        return Vector2(self.x - v.x, self.y - v.y)

    def __mul__(self, n):
        return Vector2(self.x * n, self.y * n)
    
    def __div__(self, n):
        return Vector2(self.x / n, self.y / n)


#Camera class, controls the viewing point/angle of the 3D scene, as well as projection of 3D points into 2D ones.
class Camera:
    def __init__(self, pos: Vector3, rot: Vector3, aspect_ratio = 16/9):
        self.pos = pos  #Camera position in 3D Space
        self.rot = rot  #Camera rotation (euler angles (look them up)) in radians
        self.fov = PI/2   #Field of View of the camera
        self.near, self.far = 0.01, 1000 #Near and far clipping planes (any objects closer than near or farther than far will not be drawn)
        self.aspect_ratio = aspect_ratio    #Default window aspect ratio
        self.fV = Vector3(cos(self.rot.y)*cos(self.rot.x), sin(self.rot.x), sin(self.rot.y) * cos(self.rot.x))   #Vector that points forward from the camera
        self.rV = self.fV.cross(Vector3(0, 1, 0)).normalize() #Vector that points to the right from the camera
        self.uV = self.rV.cross(self.fV).normalize()   #Vector that points upward.
    
    def trasformationMatrix(self):  #Creates the transformation matrix that converts 3d points to 2d points
        viewMatrix = [  #Matrix that transforms a point to have its position and orientation relative to the camera
            [self.rV.x, self.rV.y, self.rV.z, self.pos.dot(self.rV) * -1],
            [self.uV.x, self.uV.y, self.uV.z, self.pos.dot(self.uV) * -1],
            [self.fV.x, self.fV.y, self.fV.z, self.pos.dot(self.fV) * -1],
            [0, 0, 0, 1]]
        try:
            self.projectionMatrix   #Check to see if the projection matrix has already been calculated
        except:                     # (It only needs to be calculated once when the camera is created)
            h = tan(self.fov / 2) * self.near   #Calculate the height of the screen space (not the same as the window)
            w = h * self.aspect_ratio           #Calculate the width
            self.projectionMatrix = [       #Create a projection matrix that transforms a camera-relative point, into
                [2 * self.near / w, 0, 0, 0],   #a 2D point
                [0, 2 * self.near / h, 0, 0],
                [0, 0,  -(self.far + self.near) / (self.far - self.near), -2 * self.far * self.near / (self.far - self.near)],
                [0, 0, -1, 0]
            ]
        return matmul(self.projectionMatrix, viewMatrix)    #Multiply the 2 matrices together to get the final point.

    def update(self):
        self.fV = Vector3(cos(self.rot.y)*cos(self.rot.x), sin(self.rot.x), sin(self.rot.y) * cos(self.rot.x))   #Vector that points forward from the camera
        self.rV = self.fV.cross(Vector3(0, 1, 0)).normalize() #Vector that points to the right from the camera
        self.uV = self.rV.cross(self.fV).normalize()   #Vector that points upward.

    def project(self, p: Vector3, sc:pygame.surface.Surface):  #Method that projects a 3D Point onto the Camera, and returns its 2D Output on the display surface
        hPoint = matmul(self.trasformationMatrix(), [[p.x],[p.y],[p.z],[1]])    #multiply the point by the transformation matrix
        try:    #will attempt to convert the point from 2d device coordinates to pygame coordinates
            nDc = Vector2(hPoint[0][0]/hPoint[3][0], hPoint[1][0]/hPoint[3][0])
            viewPoint = Vector2(((nDc.x + 1)/2)*sc.get_width(), ((1 - nDc.y)/2)*sc.get_height())
            return viewPoint    #Return projected point
        except:
            return ZeroDivisionError('Point projected at infinity!')    #error happens when point is projected infinitely far away
        


    def tryCulling(self, t):    #Optimization that ignores certain faces that aren't visible when rendering
        cToTri = t.points[0] - self.pos    
        if (cToTri.dot(t.normal)) >= 0: return True #Checks if face isnt facing the camera

        for point in t.points:
            if (point-self.pos).dot(self.fV.normalize()) <= 0:  #Checks if face is behind the camera
                return True
        
        return False


    
class Tri:  # Basic polygon face class, makes a triangle from 3 points
    def __init__(self, points: list, color: tuple):
        if len(points) != 3:    #Makes sure that exactly 3 points are provided
            raise ValueError('Invalid Number of Points in Tri!')

        self.points = points    #Triangle Points
        self.normal = (points[1] - points[0]).cross(points[2] - points[0]).normalize()  #Calculates a normal vector for the triangle (useful for calculating facing angle and reflections/collisions later)
        self.color = color  #Color of the triangle
        self.centroid = sum(points)/3

    def update(self):
      self.normal = (self.points[1] - self.points[0]).cross(self.points[2] - self.points[0]).normalize()
      self.centroid = sum(self.points)/3
  
    def draw(self, sc:pygame.surface.Surface, camera: Camera):  #Method that draws the triangle to the screen by projecting it onto a camera
        try:
            if not camera.tryCulling(self): #Checks to see if it can be ignored in rendering
                pointConv = [camera.project(p, sc) for p in self.points] #Project and transform points to draw on the screen
                pointConv = [(p.x, p.y) for p in pointConv] #Converts Vector2 to a coordinate list in the form (x, y)
                pygame.draw.polygon(sc, self.color, pointConv)  #Draws the triangle on the screen
            else:
                raise Exception('Culled Face')  #Dont draw the triangle if it is culled from rendering
        except Exception as e:
            return False    #Dont render if the face is culled or if an error arises in rendering

class Object:   #object class made up of triangles
    def __init__(self, verts:list, triColors:list):
        if len(verts)%3 != 0:   #Make sure the vertices are a multiple of 3 (each tri has 3 vertices)
            raise ValueError('Vertices are not a multiple of 3, cannot make Tri faces!')
            
        self.verts = verts 
        self.colors = triColors
        #Create tris out of vertices, and calculate the center point of the whole object shape
        self.tris = [Tri((self.verts[3*i], self.verts[3*i+1], self.verts[3*i+2]), self.colors[i]) for i in range(len(self.verts)//3)]
        self.centroid = sum([t.centroid for t in self.tris])/len(self.tris)
        
        for tri in self.tris:   #Make sure the triangle normals point outward from the shape 
            if tri.normal.dot(tri.centroid - self.centroid)<=0:
                tri.normal *= -1 

    def move(self, moveVector:Vector3):
        for t in self.tris: 
            t.points = [p + moveVector for p in t.points]
            t.update()
          
        self.centroid = sum([t.centroid for t in self.tris])/len(self.tris)
        for tri in self.tris:   #Make sure the triangle normals point outward from the shape
            if tri.normal.dot(tri.centroid - self.centroid)<=0:
                tri.normal *= -1 

    def rotate(self, rotationVector:Vector3):
      pass
                
class Scene:    #Scene class that stores objects and can be rendered with the camera
    def __init__(self, objects=[]):
        self.objects = objects 
        self.tris = [t for o in self.objects for t in o.tris]

    def generateZBuffer(self, c:Camera):    #Object-level z buffer
        distanceList = [(i, c.pos.dist(t.centroid)) for i, t in enumerate(self.tris)]
        sortedList = sorted(distanceList, key=lambda x: x[1], reverse=True)
        return [self.tris[i[0]] for i in sortedList]
    
    def render(self, sc: pygame.surface.Surface, c: Camera):    #render the object in the order of the z-buffers
          for tri in self.generateZBuffer(c):
              tri.draw(sc, c)
                
class Rect(Object):  #Rectangular prism object
  def __init__(self, pos:Vector3, width, height, depth, colors):
    self.colors = colors
    self.verts = [
            Vector3(pos.x, pos.y, pos.z), Vector3(pos.x+width, pos.y, pos.z), Vector3(pos.x+width, pos.y+height, pos.z), Vector3(pos.x,pos.y,pos.z), Vector3(pos.x,pos.y+height,pos.z), Vector3(pos.x+width,pos.y+height,pos.z),
            Vector3(pos.x, pos.y, pos.z+depth), Vector3(pos.x+width, pos.y, pos.z+depth), Vector3(pos.x+width, pos.y+height, pos.z+depth), Vector3(pos.x,pos.y,pos.z+depth), Vector3(pos.x,pos.y+height,pos.z+depth), Vector3(pos.x+width,pos.y+height,pos.z+depth),
            Vector3(pos.x,pos.y,pos.z), Vector3(pos.x,pos.y+height,pos.z), Vector3(pos.x,pos.y,pos.z+depth), Vector3(pos.x,pos.y,pos.z+depth), Vector3(pos.x, pos.y+height, pos.z+depth), Vector3(pos.x,pos.y+height,pos.z),
            Vector3(pos.x+width,pos.y,pos.z), Vector3(pos.x+width,pos.y+height,pos.z), Vector3(pos.x+width,pos.y,pos.z+depth), Vector3(pos.x+width,pos.y,pos.z+depth), Vector3(pos.x+width, pos.y+height, pos.z+depth), Vector3(pos.x+width,pos.y+height,pos.z),
            Vector3(pos.x,pos.y,pos.z), Vector3(pos.x+width, pos.y, pos.z), Vector3(pos.x+width, pos.y, pos.z+depth), Vector3(pos.x,pos.y,pos.z), Vector3(pos.x,pos.y,pos.z+depth), Vector3(pos.x+width,pos.y,pos.z+depth),
            Vector3(pos.x,pos.y+height,pos.z), Vector3(pos.x+width, pos.y+height, pos.z), Vector3(pos.x+width, pos.y+height, pos.z+depth), Vector3(pos.x,pos.y+height,pos.z), Vector3(pos.x,pos.y+height,pos.z+depth), Vector3(pos.x+width,pos.y+height,pos.z+depth)]

    super().__init__(self.verts, [color for color in self.colors for i in range(2)])    #make each face its own color
   
class Cube(Rect): #Cube object (ill rewrite this later probably)
    def __init__(self, pos:Vector3, width, colors):
        super().__init__(pos, width, width, width, colors)

class FPSCamera(Camera):    #Special camera that allows for FPS style movement and control
    def __init__(self, pos:Vector3, rot:Vector3, speed:float, rotSpeed:float, aspect_ratio = 16/9):
        super().__init__(pos, rot, aspect_ratio=aspect_ratio)
        self.speed = speed
        self.rotSpeed = rotSpeed
        self.binds = {      #Key bindings for controls
            'forward': pygame.K_w,
            'backward':pygame.K_s,
            'left':pygame.K_a,
            'right':pygame.K_d,
            'rotUp':pygame.K_UP,
            'rotDown':pygame.K_DOWN,
            'rotLeft':pygame.K_LEFT,
            'rotRight':pygame.K_RIGHT
        }
    
    def update(self):   #checks input for movement
        self.fV = Vector3(cos(self.rot.y)*cos(self.rot.x), sin(self.rot.x), sin(self.rot.y) * cos(self.rot.x))   #Vector that points forward from the camera
        self.rV = self.fV.cross(Vector3(0, 1, 0)).normalize() #Vector that points to the right from the camera
        self.uV = self.rV.cross(self.fV).normalize()   #Vector that points upward.
        keys = pygame.key.get_pressed() #uses the forward and right vectors from camera.transformationMatrix() to
        if keys[self.binds['forward']]: #move the camera relative to the direction its facing
            self.pos += self.fV
        if keys[self.binds['backward']]:
            self.pos-= self.fV
        if keys[self.binds['left']]:
            self.pos += self.rV
        if keys[self.binds['right']]:
            self.pos -= self.rV
        if keys[self.binds['rotLeft']]:
            self.rot.y += self.rotSpeed
        if keys[self.binds['rotRight']]:
            self.rot.y -= self.rotSpeed
        if keys[self.binds['rotUp']] and (self.rot.x - self.rotSpeed) > -PI/2:
            self.rot.x -= self.rotSpeed
        if keys[self.binds['rotDown']] and (self.rot.x + self.rotSpeed) < PI/2:
            self.rot.x += self.rotSpeed
