import matplotlib.pyplot as plt
import numpy as np
from stl import mesh

def get_theta(index_z, index_theta,number_points_theta):
    if index_z % 2 == 0:
        theta = np.pi * ( 2 * index_theta - 1 ) / number_points_theta
    else:
        theta = np.pi * ( 2 * index_theta ) / number_points_theta
    return theta

def get_z(index_z, number_points_z , height, zoffset):
    zstep = height / ( number_points_z - 1 )
    z = index_z * zstep
    if index_z == 0:
        z+=zoffset
    return z

def get_vertices(height, radius, number_points_z, number_points_theta, zoffset):
    vertices=[[0,0,zoffset]]

    for i in range(number_points_z):
        for j in range(number_points_theta):

            theta = get_theta(i,j,number_points_theta)
            x=radius*np.cos(theta)
            y=radius*np.sin(theta)
            
            z = get_z(i, number_points_z , height, zoffset)

            vertices.append([x,y,z])
        
    vertices=np.asarray(vertices)

    return vertices

def get_bottom_face(index_theta, number_points_theta, zoffset):
    index_1 = index_theta + 1
    index_2 = ( index_theta + 2 )
    if index_2 == number_points_theta + 1:
        index_2 = 1
    if int(zoffset)==0:
        return [0, index_2, index_1]
    return [0, index_1, index_2]

def append_bottom_faces(faces, zoffset, number_points_theta):
    for i in range(number_points_theta):
        face = get_bottom_face(i, number_points_theta, zoffset)
        faces.append(face)
    return faces

def get_side_face_uptriangle(index_z, index_theta, number_points_theta, zoffset):
    index_1 = index_theta + index_z * number_points_theta + 1
    index_2 = index_1 + 1
    index_3 = index_1 + number_points_theta
    if index_z % 2 != 0:
        index_3 += 1

    if index_2 == ( index_z + 1 ) * number_points_theta + 1:
            index_2 = index_1 - index_theta
        
    if index_3 == ( index_z + 2 ) * number_points_theta + 1:
        index_3 = ( index_z + 1 ) * number_points_theta + 1

    if int(zoffset)==0:
        return [index_1, index_2, index_3]
    return [index_1,index_3,index_2]

def get_side_face_downtriangle(index_z, index_theta, number_points_theta, zoffset):
    index_1 = index_theta + index_z * number_points_theta + 1
    index_2 = index_1 + number_points_theta
    index_3 = index_2 + 1
    if index_z %2 == 0:
        index_1 += 1
    
    if index_1 == index_2 - index_theta:
        index_1 = index_z * number_points_theta + 1
    if index_3 == ( index_z + 2 ) * number_points_theta + 1:
        index_3 = ( index_z + 1 ) * number_points_theta + 1

    if int(zoffset)==0:
        return [index_1, index_3, index_2] 
    return [index_1, index_2, index_3]

def append_side_faces(faces, zoffset, number_points_z, number_points_theta):
    for i in range(number_points_z-1):
        for j in range(number_points_theta):
            face_up   = get_side_face_uptriangle(i, j, number_points_theta, zoffset)
            face_down = get_side_face_downtriangle(i, j, number_points_theta, zoffset)
            faces.append(face_up)
            faces.append(face_down)
    return faces

def create_surface(height,radius,number_points_z,number_points_theta,zoffset):
    
    vertices = get_vertices(height, radius, number_points_z, number_points_theta, zoffset)

    faces = []
    faces = append_bottom_faces(faces, zoffset, number_points_theta)
    faces = append_side_faces(faces, zoffset, number_points_z, number_points_theta)     
    faces=np.asarray(faces)

    return vertices,faces



height=100
radius=40
number_points_z=5
number_points_theta=10
wall=2
limit=15

v1,f1=create_surface(height,radius,number_points_z,number_points_theta,0)
v2,f2=create_surface(height,radius-wall,number_points_z,number_points_theta,wall)

f2+=number_points_z*number_points_theta+1

off1=number_points_theta*(number_points_z-1)+1
off2=number_points_theta*(2*number_points_z-1)+2
fclose=[]
for i in range(number_points_theta): 
    i1=off1+i
    i2=off2+i
    i3=off1+i+1
    if i3==off1+number_points_theta:
        i3=off1
    fclose.append([i1,i3,i2])

    i1=off2+i
    i2=off1+i+1
    i3=off2+i+1
    if i3==off2+number_points_theta:
        i3=off2
    if i2==off1+number_points_theta:
        i2=off1
    fclose.append([i1,i2,i3])

fclose=np.asarray(fclose)

offset=limit/2
for i in range(1,number_points_theta+1):
    x=np.random.rand()*limit-offset
    y=np.random.rand()*limit-offset
    v1[i][0]+=x
    v1[i][1]+=y
    v2[i][0]+=x
    v2[i][1]+=y

for i in range(number_points_theta+1,len(v1)):
    signe1=1
    signe2=1
    if np.random.rand()*limit-offset < 0:
        sign1=-1
    if np.random.rand()*limit-offset < 0:
        signumber_points_z=-1
    
    x=np.random.rand()*limit-offset
    y=np.random.rand()*limit-offset
    z=np.random.rand()*limit-offset
    vec=np.asarray([x,y,z])
    v1[i][0]+=x
    v1[i][1]+=y
    v1[i][2]+=z
    v2[i][0]+=x
    v2[i][1]+=y
    v2[i][2]+=z

vertices=np.append(v1,v2,axis=0)

faces=np.append(f1,f2,axis=0)
faces=np.append(faces,fclose,axis=0)

faces=np.asarray(faces)
# Create the mesh
vase = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))


for i, f in enumerate(faces):
    for j in range(3):
        vase.vectors[i][j] = vertices[f[j],:]

number=int(np.random.rand()*10000)
# Write the mesh to file "cube.stl"
vase.save('vase_'+str(number)+'.stl')