import numpy as np
from stl import mesh

class VaseGenerator(object):
    """Creates stl file for a 3D printable vase with a given number of vertices that are randomly distributed in (x, y, z).
    Attributes:
    height: the nominal height of the vase in mm.
    radius: the nominal radius of the vase in mm.
    number_of_points_z: the number of vertices along the height of the vase.
    number_of_points_theta: the number of vertices along the perimeter of the vase.
    wall_thickness: the thicnkess of the walls of the vase in mm.
    randomness: the maximum displacement of the vertices in mm with respect to their original position.
    Note that the final height and radius of the vase will vary because of the randomness.
    """

    def __init__(self, height, radius, number_points_z, number_points_theta, wall_thickness, randomness):
        self.height = height
        self.radius = radius
        self.number_points_z = number_points_z
        self.number_points_theta = number_points_theta
        self.wall_thickness = wall_thickness
        self.randomness = randomness
        self.zstep = self.height / ( self.number_points_z - 1 )
    
    def generate_random_vase(self, path):
        """This is the only public method.
        Generate a stl file for a vase wih random vertices positions.
        The properties of the vase will follow the attributes of the class.
        The stl file will be named vase_{4 randim numbers}.stl
    Args:
        path: path where the stl file will be saved.
    """
        number=int(np.random.rand()*10000)
        vertices, surface = self.__create_vertices_faces_vase()
        vase = self.__create_vase(vertices, surface)
        vase.save(f"{path}vase_{str(number)}.stl")
    
    def __create_vertices_faces_vase(self):
        vertices, main_surfaces = self.__create_main_surfaces()
        top_surface = self.__create_top_surface()
        surface = np.append(main_surfaces, top_surface, axis = 0)
        return vertices, surface
    
    def __create_vase(self, vertices, surface):
        vase = mesh.Mesh(np.zeros(surface.shape[0], dtype=mesh.Mesh.dtype))
        dimension = 3
        for i, f in enumerate(surface):
            for j in range(dimension):
                vase.vectors[i][j] = vertices[f[j],:]
        return vase

    def __create_main_surfaces(self):
        vertices_outer, faces_outer = self.__create_main_surface(inner = False)
        vertices_inner, faces_inner = self.__create_main_surface(inner = True)
        
        faces_inner +=  self.number_points_z * self.number_points_theta + 1
        
        vertices_inner, vertices_outer = self.__add_randomness_bottom(vertices_inner, vertices_outer)
        vertices_inner, vertices_outer = self.__add_randomness_sides(vertices_inner, vertices_outer)

        vertices = np.append(vertices_outer, vertices_inner, axis = 0)
        faces = np.append(faces_outer, faces_inner, axis = 0)
        
        return vertices, faces

    def __add_randomness_bottom(self, vertices_inner, vertices_outer):
        center = self.randomness / 2
        for i in range(1, self.number_points_theta + 1):
            x = np.random.rand() * self.randomness - center
            y = np.random.rand() * self.randomness - center
            vertices_inner[i][0] += x
            vertices_outer[i][0] += x
            vertices_inner[i][1] += y
            vertices_outer[i][1] += y
        return vertices_inner, vertices_outer

    def __add_randomness_sides(self, vertices_inner, vertices_outer):
        center = self.randomness / 2
        for i in range(self.number_points_theta + 1, len(vertices_inner)):
            x = np.random.rand() * self.randomness - center
            y = np.random.rand() * self.randomness - center
            z = np.random.rand() * self.randomness - center
            vertices_inner[i][0] += x
            vertices_outer[i][0] += x
            vertices_inner[i][1] += y
            vertices_outer[i][1] += y
            vertices_inner[i][2] += z
            vertices_outer[i][2] += z
        return vertices_inner, vertices_outer

    def __create_top_surface(self):
        faces_close=[]
        faces_close = self.__append_top_faces(faces_close)
        faces_close = np.asarray(faces_close)
        return faces_close

    def __create_main_surface(self, inner):
        vertices = self.__get_vertices(inner)
        faces = []
        faces = self.__append_bottom_faces(faces, inner)
        faces = self.__append_side_faces(faces, inner)     
        faces = np.asarray(faces)
        return vertices,faces
    
    def __get_vertices(self, inner):
        zoffset = 0
        radius = self.radius
        if inner:
            zoffset = self.wall_thickness
            radius = self.radius - self.wall_thickness
        vertices=[[0,0,zoffset]]
        for i in range(self.number_points_z):
            for j in range(self.number_points_theta):
                theta = self.__get_theta(i,j)
                x = radius * np.cos(theta)
                y = radius * np.sin(theta)
                z = self.__get_z(i, inner)
                vertices.append([x,y,z])
        vertices=np.asarray(vertices)
        return vertices
    
    def __append_top_faces(self, faces):
        offset_1 = self.number_points_theta * ( self.number_points_z - 1 ) + 1
        offset_2 = self.number_points_theta * ( 2 * self.number_points_z - 1 ) + 2
        for i in range(self.number_points_theta):
            face_up   = self.__get_top_face_uptriangle(i, offset_1, offset_2)
            face_down = self.__get_top_face_downtriangle(i, offset_1, offset_2)
            faces.append(face_up)
            faces.append(face_down)
        return faces
    
    def __append_bottom_faces(self, faces, inner):
        for i in range(self.number_points_theta):
            face = self.__get_bottom_face(i, inner)
            faces.append(face)
        return faces
    
    def __append_side_faces(self, faces, inner):
        for i in range(self.number_points_z-1):
            for j in range(self.number_points_theta):
                face_up   = self.__get_side_face_uptriangle(i, j, inner)
                face_down = self.__get_side_face_downtriangle(i, j, inner)
                faces.append(face_up)
                faces.append(face_down)
        return faces
    
    def __get_bottom_face(self, index_theta, inner):
        index_1 = index_theta + 1
        index_2 = ( index_theta + 2 )
        if index_2 == self.number_points_theta + 1:
            index_2 = 1
        if inner:
            return [0, index_1, index_2]
        return [0, index_2, index_1]

    def __get_side_face_uptriangle(self, index_z, index_theta, inner):
        index_1 = index_theta + index_z * self.number_points_theta + 1
        index_2 = index_1 + 1
        index_3 = index_1 + self.number_points_theta
        if index_z % 2 != 0:
            index_3 += 1

        if index_2 == ( index_z + 1 ) * self.number_points_theta + 1:
                index_2 = index_1 - index_theta
            
        if index_3 == ( index_z + 2 ) * self.number_points_theta + 1:
            index_3 = ( index_z + 1 ) * self.number_points_theta + 1

        if inner :
            return [index_1,index_3,index_2]
        return [index_1, index_2, index_3]
    
    def __get_side_face_downtriangle(self, index_z, index_theta, inner):
        index_1 = index_theta + index_z * self.number_points_theta + 1
        index_2 = index_1 + self.number_points_theta
        index_3 = index_2 + 1
        if index_z %2 == 0:
            index_1 += 1
        
        if index_1 == index_2 - index_theta:
            index_1 = index_z * self.number_points_theta + 1
        if index_3 == ( index_z + 2 ) * self.number_points_theta + 1:
            index_3 = ( index_z + 1 ) * self.number_points_theta + 1

        if inner :
            return [index_1, index_2, index_3]
        return [index_1, index_3, index_2] 
    
    def __get_top_face_uptriangle(self, index_theta, offset_1, offset_2):
        offset_1 = self.number_points_theta * ( self.number_points_z - 1 ) + 1
        offset_2 = self.number_points_theta * ( 2 * self.number_points_z - 1 ) + 2

        index_1 = offset_1 + index_theta
        index_2 = offset_2 + index_theta
        index_3 = index_1 + 1
        if index_3 == offset_1 + self.number_points_theta:
            index_3 = offset_1
        
        return [index_1, index_3, index_2]
    
    def __get_top_face_downtriangle(self, index_theta, offset_1, offset_2):
        index_1 = offset_2 + index_theta
        index_2 = offset_1 + index_theta + 1
        index_3 = index_1 + 1

        if index_3 == offset_2 + self.number_points_theta:
            index_3 = offset_2
        if index_2 == offset_1 + self.number_points_theta:
            index_2 = offset_1
        
        return [index_1, index_2, index_3]

    def __get_theta(self, index_z, index_theta):
        if index_z % 2 == 0:
            theta = np.pi * ( 2 * index_theta - 1 ) / self.number_points_theta
        else:
            theta = np.pi * ( 2 * index_theta ) / self.number_points_theta
        return theta

    def __get_z(self, index_z, inner):
        z = index_z * self.zstep
        if inner and index_z == 0:
            z += self.wall_thickness
        return z
    