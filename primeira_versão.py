def reward_function(params):
    # Parâmetros de entrada
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    abs_steering = abs(params['steering_angle'])
    progress = params['progress']
    steps = params['steps']

    # 1. Penalização rigorosa se sair da pista
    if not all_wheels_on_track:
        return 1e-3

    # 2. Recompensa por se manter no centro da pista
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3

    # 3. Penalizar direção brusca (ziguezague)
    ABS_STEERING_THRESHOLD = 15.0 
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward zar direção brusca (ziguezague)
    ABS_STEERING_THRESHOLD = 15.0 
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8 

    # 4. Recompensar alta velocidade apenas em retas
    if abs_steering < 5.0 and speed > 2.0:
        reward *= 1.5 
    
    # 5. Recompensa por terminar o trajeto de forma eficiente
    if steps > 0:
        # Aumenta a recompensa proporcionalmente à velocidade de progresso
        reward += (progress / steps) * 2.0
        
    return float(max(reward, 1e-3))