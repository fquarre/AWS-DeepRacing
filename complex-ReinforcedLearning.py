import math

def logiticDistFct(coef,inter,value):
    return 1/(1+math.exp(1)**(-(coef*value-inter)))
    
def stdDistFct(mu,sigma,value):
    return (math.exp(1)**(-0.5*((value-mu)/sigma)**2))/(sigma*math.sqrt(2*math.pi))/1.6

def reward_function(params): #Shepherd 3.5
    # Initialize the reward with typical value 
    reward = 1e-3
    
    # Read input variables
    debugList = []
    debugList.append("DEBUG")
    debugList.append(params['x'])
    debugList.append(params['y'])
    debugList.append(params['closest_waypoints'][0])
    debugList.append(params['waypoints'][params['closest_waypoints'][0]][0])
    debugList.append(params['waypoints'][params['closest_waypoints'][0]][1])

    MAXSPEED = 2.5
    MINSPEED = 1.5
    DEVIATIONTHRESHOLD = 10
    
    MAXSTEERINGANGLE_FLAT = 2
    DIFFERENTIAL_FLAT = 1.5
    MAXSTEERINGANGLE_STARTCURVE = 5
    DIFFERENTIAL_STARTCURVE = 2
    MAXSTEERINGANGLE_TURN = 10
    # !TODO: potential error - angles (track and streering) should be correlated in some way
    
    heading = params['heading']
    trackWidth = params['track_width']
    distanceFromCenter = params['distance_from_center']
    speed = params['speed']
    debugList.extend([heading,trackWidth,distanceFromCenter,distanceFromCenter/(trackWidth/2),speed])    
    
    # Calculate the direction of the center line based on the closest waypoints
    waypointsOffset = 1 #based on speed, determine how many waypoints ahead we need to calculate movements
    waypoints = params['waypoints']
    closestWaypoints = params['closest_waypoints']
    prevPoint = waypoints[closestWaypoints[0]]
    nextPoint = waypoints[closestWaypoints[1]]
    fwdPoint = waypoints[(closestWaypoints[1] + waypointsOffset) % len(waypoints)]
    debugList.extend([closestWaypoints[0],closestWaypoints[1],(closestWaypoints[1] + waypointsOffset) % len(waypoints)])

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    # based on number of offset waypoints, calculate if this is acute or obtuse, ie. need to start increasing or decreasing speed
    trackDirection = math.degrees(math.atan2(nextPoint[1] - prevPoint[1], nextPoint[0] - prevPoint[0]) ) #Convert to degrees
    forecastTrackDirection = math.degrees(math.atan2(fwdPoint[1] - prevPoint[1], fwdPoint[0] - prevPoint[0]))
    trackDifferential = round(trackDirection,5) - round(forecastTrackDirection,5)

    direction = 0 if (trackDifferential == 0) else (abs(trackDifferential)/trackDifferential) # 0-->Straight, -1-->Left, 1-->Right 
    
    if (abs(trackDifferential)>300):
        trackDifferential = (360-abs(trackDifferential))*direction

    debugList.extend([trackDirection,forecastTrackDirection,trackDifferential,abs(trackDirection - heading),direction,params['is_left_of_center']])

    #Coefficients for speed reward distribution
    SPEED_COEF_FLAT = 20
    SPEED_INTER_FLAT = 35
    SPEED_MU_STARTCURVE = (MINSPEED*1.5) #Max speed before after turn
    SPEED_SIGMA_STARTCURVE = .25
    SPEED_MU_TURN = MINSPEED #Max speed during turn
    SPEED_SIGMA_TURN = .25
    
    #Coefficients for position reward distribution
    DISTANCE_MU_FLAT = 0
    DISTANCE_SIGMA_FLAT = .25
    DISTANCE_MU_STARTCURVE = (trackWidth/2) * .5
    DISTANCE_SIGMA_STARTCURVE = .25
    DISTANCE_MU_TURN = (trackWidth/2) * .85
    DISTANCE_SIGMA_TURN = .25
    
    #if we're off center by 125% or going into the wrong direction, leave
    if ((speed < MINSPEED) or (distanceFromCenter > (trackWidth/2)) or (abs(trackDirection - heading) > DEVIATIONTHRESHOLD)):
        debugList.extend((-1,-1)) #SpeedReward --> -1 since we're failing, positionReward --> -1 since we're failing
        reward = 1e-3
    else:
        if (abs(trackDifferential)) <= DIFFERENTIAL_FLAT: # If track is straight(ish) !TODO: no rewarid on position wrt center?
            speedReward = logiticDistFct(SPEED_COEF_FLAT,SPEED_INTER_FLAT,speed)
            positionReward = stdDistFct(DISTANCE_MU_FLAT,DISTANCE_SIGMA_FLAT,distanceFromCenter)
            reward +=  speedReward + positionReward
            if abs(params["steering_angle"]) < MAXSTEERINGANGLE_FLAT:
                reward += 1
            debugList.append((speedReward,positionReward))
        elif (abs(trackDifferential)) <= DIFFERENTIAL_STARTCURVE: #if we're getting to a turn
            speedReward = stdDistFct(SPEED_MU_STARTCURVE,SPEED_SIGMA_STARTCURVE,speed)
            positionReward = stdDistFct(DISTANCE_MU_STARTCURVE,DISTANCE_SIGMA_STARTCURVE,distanceFromCenter)
            reward +=  speedReward + positionReward
            if  ((direction == -1) and not(params['is_left_of_center'])) or ((direction == 1) and params['is_left_of_center']):
                reward += .5
            if abs(params["steering_angle"]) < MAXSTEERINGANGLE_STARTCURVE:
                reward += 1
            debugList.append((speedReward,positionReward))    
        else: #(abs(trackDirection - forecastTrackDirection)) > MAXSTEERINGANGLE_TURN: !TODO: reward on steering angle?
            speedReward = stdDistFct(SPEED_MU_TURN,SPEED_SIGMA_TURN,speed)
            positionReward = stdDistFct(DISTANCE_MU_TURN,DISTANCE_SIGMA_TURN,distanceFromCenter)
            reward +=  speedReward + positionReward
            if  ((direction == -1) and not(params['is_left_of_center'])) or ((direction == 1) and params['is_left_of_center']):
                reward += 1
            #if abs(params["steering_angle"]) < MAXSTEERINGANGLE_TURN:
            #    reward += 1
            debugList.append((speedReward,positionReward))
            
    #Debug
    #DEBUG;x;y;previousPointID;previousPointX;previousPointY;heading;trackwidth;distanceFromCenter;%DistanceFromCenter;Speed;previousWaypoint;NextWaypoint;ForecastedWayPoint;TrackDirection;ForecastTrackDirection;TrackDifferential;abs(heading);Direction;isLeftOfCenter;speedReward;positionReward;reward;isOffTrack
    debugList.append(reward)
    debugList.append(params['is_offtrack'])
    print(*debugList, sep=";")

    return reward
