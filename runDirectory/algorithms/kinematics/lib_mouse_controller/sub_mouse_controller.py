global x_off
x_off = 0
global y_off
y_off = 0
global z_off
z_off = 0
global x_out
x_out = 0
global y_out
y_out = 0
global z_out
z_out = 0
global state
state = 0
global left
left = 0
global right
right = 0 
global scroll
scroll = 0 
global x_old 
x_old = 0
global y_old 
y_old = 0
global z_old 
z_old = 0
global scroll_offset
scroll_offset = 0
global scroll_out
scroll_out = 0

global x_out_init
global z_out_init
global y_out_init


# initial values
x_out_init = 0 # (x is the y for phantom_x)
y_out_init = 120 #(y is the x for phantom_x)
z_out_init = 120 # (z is the z)

def state_fun_0(msg):
    global x_off
    global y_off
    global z_off
    global x_out
    global y_out
    global z_out
    global state
    global left    
    global right
    global x_old
    global y_old
    global z_old
    global scroll_offset
    global scroll_out
    global x_out_init 
    global z_out_init
    global y_out_init

    btn = [0,0]
    ret = []
    btn = msg[3]
    left = btn[0]
    right = btn[1]
    x = msg[0]
    y = msg[1]
    scroll = msg[2]    
    x_out = x_out_init 
    y_out = y_out_init 
    z_out = z_out_init   
    scroll_out = scroll

    if(right == 1):        
        state = 1
    
    ret = [x_out,y_out,z_out,scroll_out]
    
    return(ret)

def state_fun_1(msg):
    global x_off
    global y_off
    global z_off
    global x_out
    global y_out
    global z_out
    global state
    global left    
    global right
    global x_old
    global y_old
    global z_old
    global scroll_offset
    global scroll_out
    global x_out_init 
    global z_out_init
    global y_out_init
    btn = [0,0]
    ret = []
    btn = msg[3]
    left = btn[0]
    right = btn[1]
    x = msg[0]
    y = msg[1]    
    scroll = msg[2]
    x_off = msg[0]
    y_off = msg[1]  
    scroll_offset = 0
	
    x_out = x_out_init #0
    y_out = y_out_init #0
    z_out = z_out_init #0

    scroll_out = 0
    if(right == 0):
        state = 2
    ret = [x_out,y_out,z_out,scroll_out]
    return(ret)

def state_fun_2(msg):
    global x_off
    global y_off
    global z_off
    global x_out
    global y_out
    global z_out
    global state
    global left    
    global right
    global x_old
    global y_old
    global z_old
    global scroll_offset
    global scroll_out
    global x_out_init 
    global z_out_init
    global y_out_init

    btn = [0,0]
    ret = []
    btn = msg[3]
    left = btn[0]
    right = btn[1]
    x = msg[0]
    y = msg[1]    
    scroll = msg[2]

    x_out = x_out_init + (x - x_off)
    y_out = y_out_init + (y - y_off)*(-1)
    Z_out = z_out_init + 0

    scroll_out = scroll - scroll_offset
    #print "scroll_offset", scroll_offset
    if(left == 1):
        state = 3
    
	if (right == 1):
		state = 7	    
        
    ret = [x_out,y_out,z_out,scroll_out]
    return(ret)

def state_fun_3(msg):
    global x_off
    global y_off
    global z_off
    global x_out
    global y_out
    global z_out
    global state
    global left    
    global right
    global x_old
    global y_old
    global z_old
    global scroll_offset
    global scroll_out
    global x_out_init 
    global z_out_init
    global y_out_init

    btn = [0,0]
    ret = []
    btn = msg[3]
    left = btn[0]
    right = btn[1]
    x = msg[0]
    y = msg[1]    
    scroll = msg[2]

    x_off = x
    y_off = y
    z_old = z_out

    state = 4
    ret = state_fun_4(msg)
    return(ret)

def state_fun_4(msg):
    global x_off
    global y_off
    global z_off
    global x_out
    global y_out
    global z_out
    global state
    global left    
    global right
    global x_old
    global y_old
    global z_old
    global scroll_offset
    global scroll_out
    global x_out_init 
    global z_out_init
    global y_out_init

    btn = [0,0]
    ret = []
    btn = msg[3]
    left = btn[0]
    right = btn[1]
    x = msg[0]
    y = msg[1]    
    scroll = msg[2]

    x_out = x_out
    y_out = y_out
    z_out = z_old + (y - y_off)*(-1)
    scroll_out = scroll - scroll_offset
    
    if(left == 0):
        state = 5
    ret = [x_out,y_out,z_out,scroll_out]
    return(ret)

def state_fun_5(msg):
    global x_off
    global y_off
    global z_off
    global x_out
    global y_out
    global z_out
    global state
    global left    
    global right
    global x_old
    global y_old
    global z_old
    global scroll_offset
    global scroll_out
    global x_out_init 
    global z_out_init
    global y_out_init

    btn = [0,0]
    ret = []
    btn = msg[3]
    left = btn[0]
    right = btn[1]
    x = msg[0]
    y = msg[1]    
    scroll = msg[2]

    x_off = x
    y_off = y
    x_old = x_out
    y_old = y_out

    state = 6
    ret = state_fun_6(msg)
    return(ret)

def state_fun_6(msg):
    global x_off
    global y_off
    global z_off
    global x_out
    global y_out
    global z_out
    global state
    global left    
    global right
    global x_old
    global y_old
    global z_old
    global scroll_offset
    global scroll_out
    global x_out_init 
    global z_out_init
    global y_out_init

    btn = [0,0]
    ret = []
    btn = msg[3]
    left = btn[0]
    right = btn[1]
    x = msg[0]
    y = msg[1]    
    scroll = msg[2]

    x_out = x_old + x - x_off
    y_out = y_old + (y - y_off)*(-1)
    z_out  = z_out  
    scroll_out = scroll - scroll_offset      
            
    if(left == 1):
        state = 3
        
    if (right == 1):
        state = 7	
        
    ret = [x_out,y_out,z_out,scroll_out]
    return(ret)

def state_fun_7(msg):
	global x_off
	global y_off
	global z_off
	global x_out
	global y_out
	global z_out
	global state
	global left	
	global right
	global x_old
	global y_old
	global z_old
	
	btn = [0,0]
	ret = []
	btn = msg[3]
	left = btn[0]
	right = btn[1]
	x = msg[0]
	y = msg[1]	
	scroll = msg[2]
	print "state 7 is reached"
	
    	ret = state_fun_0(msg)
    
	state = 0
	return(ret)

def controller(msg):
    global state
    if(state == 0):
        ret = state_fun_0(msg)
        return(ret)
    if(state == 1):
        ret = state_fun_1(msg)
        return(ret)
    if(state == 2):
        ret = state_fun_2(msg)
        return(ret)
    if(state == 3):
        ret = state_fun_3(msg)
        return(ret)
    if(state == 4):
        ret = state_fun_4(msg)
        return(ret)
    if(state == 5):
        ret = state_fun_5(msg)
        return(ret)
    if(state == 6):
        ret = state_fun_6(msg)
        return(ret)
    if(state == 7):
        ret = state_fun_7(msg)
        return(ret)

