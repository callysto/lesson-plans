from math import sqrt, isnan
import numpy as np

"""
This script is for generating the surface points of the bezier surface.
"""
"""
    Takes in P, U, V as 2D arrays of vectors (Both the same size), n resolution of each "tile" since this can be rectangular.
    Returns XX, YY, ZZ 2d arrays of where each point of the grid lies.
    P,U,V = [
        [[x,y,z], [x,y,z]],
        [[x,y,z], [x,y,z]]
    ]
    P - is points
    V is direction along the i'th direction P[i][ ] \/
    U is direction along the j'th direction P[ ][j] ->
    
    (P).-> (U) -  -  -  (P).->(U) -   -   -  
       |                   |
       v (V)   P[0,0]      v(V)          P[0,1]
       |                   |
    (P).-> (U) -   -  - (P).->(U)  -  -   -
       |                   |
       v (V)   P[1,0]      v(V)
    """
def GetSurface(p, u, v, n):
    P = np.array(p)
    U = np.array(u)
    V = np.array(v)
    columns = len(P[0])-1 #columns of P
    rows = len(P)-1       #ros of P,
    
    #adding one for the included endpoint, all numbers repeat mod 1, we sample our t points from this instead of calculating them
    T = np.linspace(0, 1, n+1, endpoint = True)
    
    rowsLinspace = np.linspace(0, 1*rows   , n*rows    + 1, endpoint = True)
    colsLinspace = np.linspace(0, 1*columns, n*columns + 1, endpoint = True)
    XX, YY    = np.meshgrid(colsLinspace, rowsLinspace)
    ZZ, dummy = np.meshgrid(colsLinspace, rowsLinspace)
    
    #GENERATE THE TOP LINES FOR LATER INTERPOLATION
    for i in range(0, rows+1):
        for j in range(0, columns):
            A = P[i][j  ]
            D = P[i][j+1]

            B = A + U[i][j  ]
            C = D - U[i][j+1]
            # Generate the top line, n+1 = len(T)
            for t in range(0, n+1):  
                point = BCurve(A, B, C, D, T[t])
                #print(point)
                #[i*n][j*n + t] are the i'th tile row, and j'th tile column, at subposition t
                XX[i * n][j*n + t] = point[0]
                YY[i * n][j*n + t] = point[1]
                ZZ[i * n][j*n + t] = point[2]
    
    #FILL IN FROM TOP TO BOTTOM USING THE TOP LINES
    for i in range(0, rows):
        for j in range(0, columns):
            #for each tile, generate the grid in it.
            #using the top and bottom generated points, and the 
            #interpolated handles, it generates the grid inbetween. 
            
            B_ha = V[i][j]   
            B_hb = V[i][j]   + U[i][j]
            B_hc = V[i][j+1] - U[i][j+1] #negative U[i][j+1] to orientate properly for interpolation
            B_hd = V[i][j+1]

            C_ha = V[i+1][j]
            C_hb = V[i+1][j]   + U[i+1][j]
            C_hc = V[i+1][j+1] - U[i+1][j+1]
            C_hd = V[i+1][j+1]
            
            for t in range(0, n+1):
                A = [XX[ i   *n][j*n + t], YY[ i   *n][j*n + t], ZZ[ i   *n][j*n + t]]
                D = [XX[(i+1)*n][j*n + t], YY[(i+1)*n][j*n + t], ZZ[(i+1)*n][j*n + t]]
                
                B = A + Lerp(B_ha, B_hd, T[t])  
                C = D - Lerp(C_ha, C_hd, T[t])
                for s in range(1, n): #(1, n = len(T)-1) because top and bottom already generated 
                    point = BCurve(A, B, C, D, T[s])
                    
                    XX[i*n+s][j*n+t] = point[0]
                    YY[i*n+s][j*n+t] = point[1]
                    ZZ[i*n+s][j*n+t] = point[2]
              
    return XX, YY, ZZ
    

"""
Takes in points A,B,C,D
and a interpolation value t in [0,1] range.

Outputs a point in the same dimension
"""
def BCurve(A,B,C,D, t):
    
    A0 = np.multiply(A, -1*t**3 + 3*t**2 - 3*t + 1)
    B0 = np.multiply(B,  3*t**3 - 6*t**2 + 3*t)
    C0 = np.multiply(C, -3*t**3 + 3*t**2)
    D0 = np.multiply(D,  1*t**3)
    return A0 + B0 + C0 + D0 #arrays can add onto eachother nicely.
"""
A linear interpolation between A and B
using the interpolation value t in [0,1] range.

Outputs a point in the same dimension
"""
def Lerp(A, B, t):
    A0 = np.multiply(A, -t + 1)
    B0 = np.multiply(B,  t)
    return A0 + B0
    