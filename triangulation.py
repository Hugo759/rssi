import math

'''
This code triangulates the position and heading of a robot from three landmarks
which have known position.

Note that Angles increase counterclockwise from above, just like standard math.  Forward = 0.

This code and its notation is mostly from "A comprehensive study of three object triangulation"
by Charles Cohen and Frank Koss, University of Michigan.  I coded the section 3.4,
"Geometric Circle Intersection", although I needed to fill in the blanks a little bit.
This code is based on 2 intersecting circles.  The first circle passes through
beacon 1, beacon 2, and the robot, while the second circle passes through beacon 2,
beacon 3, and the robot.  This geometric construction allows a simple solution to the
position of the robot.  If the angles input are measured from the front of the robot,
it also gives the heading.

Code entered by Dave Kopp, 3/8/2015
'''
def vlen(vector):
    return math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
def seglen(pt1, pt2):
    return vlen(psub(pt2, pt1))
def vadd(vec1, vec2):
    return ( vec1[0]+vec2[0] , vec1[1]+vec2[1] )
def vscale(scale, vec):
    return (scale*vec[0], scale*vec[1])
def psub(pt1, pt2):
    return ( pt1[0]-pt2[0], pt1[1]-pt2[1] )
def pcenter(pt1, pt2):
    v12 = psub(pt2, pt1) # unit vector from landmark 1 to 2    
    return vadd(pt1, vscale(0.5, v12)) # pt1 + 0.5*v12
def vec_eq(vec1, vec2):
    equals = False
    if (vec1[0] == vec2[0]) and (vec1[1] == vec2[1]):
        equals = True
    return equals
def cosine_rule_get_angle(a, b, c):
    return math.acos((a*a + b*b - c*c)/(2*a*b))
def unitvec(vec):
    len_vec = vlen(vec)
    return(vec[0]/len_vec, vec[1]/len_vec)
def vdot(vec1, vec2):
    return vec1[0]*vec2[0] + vec1[1]*vec2[1]
def unit_normal(vec, facing_vec):
    if (vec[0] == 0): # ex. (0, 2)
        v_norm = (1, 0)
    elif (vec[1] == 0): # ex. (2, 0)
        v_norm = (0, 1)
    else:
        v_temp = (-1 * vec[1], vec[0])
        v_temp_len = vlen(v_temp)
        v_norm = (v_temp[0]/v_temp_len, v_temp[1]/v_temp_len)
    if vdot(v_norm, facing_vec) >= 0:
        return v_norm
    else:
        return vscale(-1, v_norm)
def v_direction(vec):
    return math.atan2(vec[1], vec[0])
def heading_to_unit_velocity(heading):
    return (math.cos(heading), math.sin(heading))
def properly_order_landmarks(landmark_list, angle_list):
    '''
    Reorders the landmarks as the first step of geometric triangulation.
    '''
    landmark_orders = ( (0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0) )
    landmark_order = landmark_orders[0]
    for order_index in range(0, len(landmark_orders)):
        landmark_order = landmark_orders[order_index]
        angle0 = angle_list[landmark_order[0]]
        angle1 = angle_list[landmark_order[1]]
        angle2 = angle_list[landmark_order[2]]
        alpha = (angle1 - angle0) % 360.0
        beta = (angle2 - angle1) % 360.0
        if ((alpha >= 0) and (beta >= 0) and (alpha <= 180) and (beta <= 180)):
            break
    new_angle_list = [0, 0, 0]
    new_landmark_list = [0, 0, 0]
    for order_index in range(0, len(landmark_order)):
        new_angle_list[order_index] = angle_list[landmark_order[order_index]] % 360.0
        new_landmark_list[order_index] = landmark_list[landmark_order[order_index]]
    return (new_angle_list, new_landmark_list)
def three_beacon_triangulation(landmark_list, angle_list, eps):
    (angles, landmarks) = properly_order_landmarks(landmark_list, angle_list)
    #print "Angles: ", angles, "Landmarks:", landmarks
    alpha = (angles[1] - angles[0]) % 360.0
    alpha = alpha * math.pi/180
    beta = (angles[2] - angles[1]) % 360.0
    beta = beta * math.pi/180
    if (alpha == 0 and beta == 0):
        print "Significant measurement error (collinear)."
        return
    pt1 = landmarks[0]
    pt2 = landmarks[1]
    pt3 = landmarks[2]
    v12 = unitvec(psub(pt2, pt1))    # unit vector from landmark 1 to 2
    v23 = unitvec(psub(pt3, pt2))    # unit vector from landmark 2 to 3
    d12 = vlen(psub(pt2, pt1))         #distance from point 1 to 2
    d23 = vlen(psub(pt3, pt2))         #distance from 2 to 3
    p12 = pcenter(pt1, pt2) # pt1 + 0.5*v12
    p23 = pcenter(pt2, pt3)

    
    if (alpha == 0): # Robot collinear with 1 and 2
        alpha = eps
    if (alpha == 180): # Robot collinear with 1 and 2
        alpha = 180 - eps
    if (beta == 0): # Robot collinear with 2 and 3
        beta = eps
    if (beta == 180): # Robot collinear with 2 and 3
        beta = 180 - eps
        
    la = 0
    lb = 0
    if not (alpha == 90):
        #if alpha is zero, then la is zero but the tangent blows up
        la = d12/( 2.0 * math.tan(alpha))
    if not (beta == 90):
        lb = d23 /( 2.0 * math.tan(beta))
    ra = d12 / (2.0 * math.sin(alpha)) #radius of circle a
    rb = d23 / (2.0 * math.sin(beta)) #radius of circle b
    
        #ca: center of circle a
    ca = (p12[0] - la*v12[1],
          p12[1] + la*v12[0])
        #cb: center of circle b
    cb = (p23[0] - lb*v23[1],
          p23[1] + lb*v23[0])
    cba = psub(ca, cb)              #points from center of circle b to center of circle a
    if vec_eq(ca, cb):
        print "Significant measurement error (concentric)."
        return

    '''
    #uncomment to debug
    print "la, lab:", la, lb
    print "pt1", pt1, "pt2", pt2, "v12", v12
    print "d12", d12, "alpha", 180/math.pi*alpha, "2*sin(alpha)", (2 * math.sin(alpha))
    print "ca, ra:", ca, ra
    print "cb, rb:", cb, rb
    print "cba", cba
    print "alpha, beta:", alpha*180/math.pi, beta*180/math.pi
    '''
    
    #get lengths of three segments of triangle (cb pt1 pt2) and find angle cb from the cosine rule
    tri_a = seglen(cb, ca) 
    tri_b = seglen(cb, pt2)
    tri_c = seglen(pt2, ca)
    gamma = cosine_rule_get_angle(tri_a, tri_b, tri_c) #math.asin(vlen(v12)/(2*ra))
    d2r = 2 * rb * math.sin(gamma)
    d2r_vec = vscale(d2r, unit_normal(cba, psub(ca, pt2)))
        #d2r*(the unit normal to cba generally facing from pt2 to ca)
    robot_coord = vadd(pt2, d2r_vec)
    vec_robot_to_pt1 = psub(pt1, robot_coord)
    heading = (v_direction(vec_robot_to_pt1) - (math.pi/180)*angles[0])
    unit_velocity = heading_to_unit_velocity(heading)
    return (robot_coord, ((180/math.pi)*heading % 360), unit_velocity)

#Begin program --------------------------------------------------------------------------

angle_list = [86.5650512, -11.5650512, -75] 
#This is a list of the measured angles to the three landmarks.
#Angles increase counterclockwise from above, just like standard math.  Forward = 0.

landmark_list = [(-1.0, 2.0),  (3.0, 1.0), (1.0, -1.0)]
#This is a list of the three landmarks, in the same order as the angles.  Each
#landmark has an x and a y coordinate.
#Note: These angles and landmarks were chosen to put the robot at the origin,
#with a heading of 30 degrees north of east.

result = three_beacon_triangulation(landmark_list, angle_list, 0.0001)
if result is not None:
    (robot_coord, heading, unit_velocity) = result
    print "Landmark coordinates:", landmark_list
    print "Angles to landmarks:", angle_list
    print "Triangulated robot coordinates:", robot_coord
    print "Heading:", heading, "Unit velocity:", unit_velocity