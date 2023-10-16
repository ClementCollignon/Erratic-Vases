import matplotlib.pyplot as plt
import numpy as np
from stl import mesh
from scipy.interpolate import interp1d
height=100
radius=40
Nz=5
Nr=10

wall=2

limit=15

A=0

D=np.genfromtxt('curve/curbe1.txt')
x=D[:,0]
y=D[:,1]
x[0]=0
y[0]=0
x=x/np.max(x)
y=y/np.max(y)

x=x*height*1
y=y*A

profile=interp1d(x,y)

def create(height,radius,Nz,Nr,zoffset):
    
    N=Nr
    N2=Nz
    r=radius

    zmax=height
    
    zstep=zmax/(N2-1)
    
    vertices=[[0,0,zoffset]]
    for j in range(N2):
        for i in range(N):
            if j%2==0: offset=-1/N*np.pi
            else: offset=0
        
            theta=i/N*np.pi*2+offset
            z=j*zstep
        
            Radius=r +profile(z)
            
            
            x=Radius*np.cos(theta)
            y=Radius*np.sin(theta)
            
            if j==0:
                z+=zoffset
            # if j==N2-1 and zoffset>0:
            #     z-=1
            vertices.append([x,y,z])
        
    vertices=np.asarray(vertices)

    faces=[]
    offset_origin=1
    #Bottom faces:
    for i in range(N):
        i1=i+1
        i2=i+2
        if i2==N+1:
            i2=1    
        if int(zoffset)==0:
            faces.append([0,i2,i1])
        else:
             faces.append([0,i1,i2])
    
    #Side faces:

    for j in range(N2-1):
        for i in range(N):
        
            if j%2==0:
                i1=i+1+j*N
                i2=i+2+j*N
                i3=i+(j+1)*N+1
                if i2==(j+1)*N+1:
                    i2=1+j*N
            else:
                i1=j*N+1+i
                i2=j*N+2+i
                i3=(j+1)*N+2+i
                if i2==j*N+N+1:
                    i2=j*N+1
                if i3==(j+1)*N+N+1:
                    i3=(j+1)*N+1
            if int(zoffset)==0:
                faces.append([i1,i2,i3])
            else:
                faces.append([i1,i3,i2])
                
            if j%2==0:
                i1=i+j*N+2
                i2=i+j*N+N+1
                i3=i+j*N+N+2
                if i1==(j+1)*N+1:
                    i1=1+j*N
                if i3==(j+1)*N+N+1:
                    i3=j*N+N+1
            else:
                i1=i+j*N+1
                i2=i+(j+1)*N+1
                i3=i+(j+1)*N+2
                if i3==(j+1)*N+N+1:
                    i3=j*N+N+1
            if int(zoffset)==0:
                faces.append([i1,i3,i2])
            else:
                faces.append([i1,i2,i3])
       
            
    faces=np.asarray(faces)


    return vertices,faces


v1,f1=create(height,radius,Nz,Nr,0)
v2,f2=create(height,radius-wall,Nz,Nr,wall)

f2+=Nz*Nr+1

off1=Nr*(Nz-1)+1
off2=Nr*(2*Nz-1)+2
fclose=[]
for i in range(Nr): 
    i1=off1+i
    i2=off2+i
    i3=off1+i+1
    if i3==off1+Nr:
        i3=off1
    fclose.append([i1,i3,i2])

    i1=off2+i
    i2=off1+i+1
    i3=off2+i+1
    if i3==off2+Nr:
        i3=off2
    if i2==off1+Nr:
        i2=off1
    fclose.append([i1,i2,i3])

fclose=np.asarray(fclose)



offset=limit/2
for i in range(1,Nr+1):
    x=np.random.rand()*limit-offset
    y=np.random.rand()*limit-offset
    v1[i][0]+=x
    v1[i][1]+=y
    v2[i][0]+=x
    v2[i][1]+=y

for i in range(Nr+1,len(v1)):
    signe1=1
    signe2=1
    if np.random.rand()*limit-offset < 0:
        sign1=-1
    if np.random.rand()*limit-offset < 0:
        sign2=-1
    
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