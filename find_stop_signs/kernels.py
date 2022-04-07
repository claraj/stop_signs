""" Kernels or filters or convolutions used by the Sobel
edge detection """

sobel_edge_detectors = {
    'sobel_vertical_edge_detection': [ 
        [-1, 0, 1], 
        [-2, 0, 2], 
        [-1, 0, 1], 
    ],

    'sobel_horizontal_edge_detection': [ 
        [1,   2,  1], 
        [0,   0,  0], 
        [-1, -2, -1], 
    ],

    'sobel_diagonal_edge_detection': [ 
        [2,  1,  0], 
        [1,  0, -1], 
        [0, -1, -2], 
    ],

    'sobel_other_diagonal_edge_detection': [ 
        [0, -1, -2], 
        [1,  0, -1], 
        [2,  1,  0], 
    ],
}


""" Currently unused """

box_blur_filter = [
    [1/9, 1/9, 1/9], 
    [1/9, 1/9, 1/9], 
    [1/9, 1/9, 1/9], 
]   

gaussian_blur_filter = [
    [1/16, 2/16, 1/16], 
    [2/16, 4/16, 2/16], 
    [1/16, 2/16, 1/16], 
] 


""" Structures used by Stefanelli and Rosenfeld algorithm
These are NOT kernels. Used to match patterns in the pixels being examined """

# Contour points - do the pixels seen match the pixels in the image?
# 1 = black
# 0 = white
# Edge image is black edges on white background. 

contour_points = [

    # lower
    [ 
        [None, None, None], 
        [None, 1,    None], 
        [None, 0,    None], 
    ],

    # above
    [ 
        [None, 0,    None], 
        [None, 1,    None], 
        [None, None, None], 
    ],

    # left
    [ 
        [None, None, None], 
        [0,    1,    None], 
        [None, None, None], 
    ],

    # right
    [ 
        [None, None, None], 
        [None, 1,    0   ], 
        [None, None, None], 
    ],

]


# at least one edge element in red 'r' and at least one edge element in blue 'b' 
# means that this pixel is of type a(number) and is a final point, edge element. 


ai = [

    # 'a1': 
    
    [ 
        ['b', 'b', 'b'], 
        [0, 1, 0], 
        ['r', 'r', 'r'], 
    ],

    # 'a2': 
    
    [ 
        ['r', 0, 'b'], 
        ['r', 1, 'b'], 
        ['r', 0, 'b'], 
    ],

    # 'a3':  
    
    [ 
        [ 0 , 'b', 'b'], 
        ['r',  1 , 'b'], 
        ['r', 'r',  0 ], 
    ],

    # 'a4': 
    
    [ 
        ['b', 'b',  0 ], 
        ['b',  1 , 'r'], 
        [ 0 , 'r', 'r'], 
    ],  
]

bi = [

    # 'b1': 
    
    [ 
        ['b',  'b',  'b' ], 
        [None,  1 ,  0   ], 
        [ 0 ,   1,   None], 
    ],

    # 'b2': 
    
    [ 
        ['b',  None, 0   ], 
        ['b',  1,    1   ], 
        ['b',  0,    None], 
    ],

    # 'b3': 
    
    [ 
        [None, 1 ,  0   ], 
        [ 0 ,  1,   None], 
        ['b', 'b',  'b' ], 
    ],

    # 'b4': 
    
    [ 
        [None, 0,    'b'], 
        [1,    1,    'b'], 
        [0,    None, 'b'], 
    ],
]

final_b_kernels = [
    # i = 0 then b1 and b2 are final 
    [bi[0], bi[1]], 
    # i = 1 then b3 and b4 are final 
    [bi[2], bi[3]], 
    # i = 2 then b1 and b4 are final  <- from lecture
    [bi[0], bi[3]], 
    # i = 3 then b2 and b3 are final   <- from lecture
    [bi[1], bi[2]], 
]


