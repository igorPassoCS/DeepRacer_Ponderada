import math

def reward_function(params):
    # Parâmetros de entrada
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    abs_steering = abs(params['steering_angle'])

    # 1. Penalização rigorosa se sair da pista
    if not all_wheels_on_track:
        return 1e-3

    # 2. Centralização Contínua (Evita pulos/solavancos)
    # A distância máxima do centro até a borda da pista é metade da largura.
    max_distance = track_width / 2.0
    distance_ratio = distance_from_center / max_distance
    
    # Usamos uma função exponencial negativa para criar uma curva de recompensa suave.
    # Sem blocos if/else rígidos, o carro sente as mudanças gradualmente.
    center_reward = math.exp(-4.0 * distance_ratio)
    
    # 3. Penalização Contínua para movimentos de direção
    # Penaliza graus de direção mais altos fluidamente
    steering_smoothness = math.exp(-0.15 * abs_steering)
    
    # 4. Velocidade atrelada à suavidade do volante
    # O carro recebe mais recompensa por velocidade se o volante estiver reto.
    # Supondo uma velocidade máxima perto de 4.0 m/s
    speed_factor = speed / 4.0
    
    # 5. Cálculo final: base na centralização + bônus de velocidade condicional e suave
    reward = center_reward + (center_reward * steering_smoothness * speed_factor)
    
    return float(max(reward, 1e-3))