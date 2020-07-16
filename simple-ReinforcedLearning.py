def reward_function(params):
    import math
    waypoints = params['waypoints']
    closestWaypoints = params['closest_waypoints']
    prevPoint = waypoints[closestWaypoints[0]]
    nextPoint = waypoints[closestWaypoints[1]]
    trackDirection = math.degrees(math.atan2(nextPoint[1] - prevPoint[1], nextPoint[0] - prevPoint[0]) )
    speedMax = 2.5

    reward = 1e-3
    #if we're below 1m/s, off center by 80% or going into the wrong direction, leave
    if ((params['speed'] < 1) or (params["distance_from_center"] > ((params["track_width"]/2)*.8)) or (abs(trackDirection - params["heading"]) > 10)):
       reward = 1e-3 
    else:
        if abs(params["steering_angle"]) < 5:
            reward += 1
        reward += ( params["speed"] / speedMax ) + 1
   
    return float(reward)
