def point_calculator(opponent_items, user_items, user_weight):
    '''
    'point_calculator' 함수는 유저와 상대방의 매칭 점수를 유저의 가중치에 근거하여 합산합니다.
    '''
    point = 0
    
    for user_item in user_items:
        point += int(user_item in opponent_items) * user_weight
        
    return point

def get_user_weight(user):
    '''
    'get_user_weight' 함수는 유저가 입력한 항목별 선호 가중치를 기준으로 'user_weight' 딕셔너리를 생성합니다.
    이때 가중치는 항목별 가중치를 전체 가중치로 나눈 값. 즉 전체 가중치의 합은 100을 넘지 않습니다.
    그 이유는 선호 가중치를 모두 높게 입력한 유저의 경우, 다른 유저에 비해 매칭 점수가 월등히 높기 때문에 매칭 포인트의 볼륨을 평준화할 필요가 있습니다.
    매칭 포인트의 볼륨이 평준화 될지라도 개인 선호에 따른 매칭은 동일하게 기능합니다.
    '''
    user_weight = {}
    
    drinking_method  = user.drinking_method_weight
    alcohol_category = user.alcohol_category_weight
    alcohol_limit    = user.alcohol_limit_weight
    alcohol_level    = user.alcohol_level_weight
    flavor           = user.flavor_weight
    
    total_user_weight = drinking_method + alcohol_category + alcohol_limit + alcohol_level + flavor

    user_weight['drinking_method_weight']  = (drinking_method/total_user_weight) * 100
    user_weight['alcohol_category_weight'] = (alcohol_category/total_user_weight) * 100
    user_weight['alcohol_limit_weight']    = (alcohol_limit/total_user_weight) * 100
    user_weight['alcohol_level_weight']    = (alcohol_level/total_user_weight) * 100
    user_weight['flavor_weight']           = (flavor/total_user_weight) * 100

    return user_weight
