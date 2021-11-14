from core.matcher.files import passions, occupations
from core.matcher.onehot import make_onehot
from core.matcher.dot import dot_product
from core.matcher.ages import age_lower_bound, age_upper_bound

def age_in_range(seeking_user, target_user):
    """
    Returns True if target_user is within seeking_user's age range
    """
    lower_bound = max(seeking_user['age_lower_bound'] - 5, age_lower_bound)
    upper_bound = min(seeking_user['age_upper_bound'] + 5, age_upper_bound)
    return lower_bound <= target_user['age_of_self'] <= upper_bound

def is_available(seeking_user, target_user):
    """
    Returns True if target_user is available for seeking_user
    """
    if target_user["gender_of_self"] in seeking_user["gender_preference"]:
        if age_in_range(seeking_user, target_user):
            return 1
        else:
            return 2
    return 0

def passion_occupation_score(seeking_user: dict, target_user: dict, category: int) -> float:
    """
    Returns the passion score for seeking_user and target_user
    """
    passion_ids = seeking_user['passion_ids']
    target_passion_ids = target_user['passion_ids']
    passion_vector = make_onehot(passion_ids, passions)
    target_passion_vector = make_onehot(target_passion_ids, passions)

    # From documentation
    if seeking_user['similarity_preference'] == 'D':
        score = (1 - dot_product(passion_vector, target_passion_vector)) * 100
        if category == 1 and seeking_user["occupation_id_of_self"] == target_user["occupation_id"]:
            score *= 2/3 # Conditionally supressing score for category 1
        elif category == 2 and seeking_user["occupation_id_of_self"] == target_user["occupation_id"]:
            score *= 1/2 # Conditionally supressing score for category 2

    # From documentation
    elif seeking_user['similarity_preference'] == 'S':
        score = dot_product(passion_vector, target_passion_vector) * 100
        if category == 1 and seeking_user["occupation_id_of_self"] == target_user["occupation_id"]:
            score *= 3/2 # Conditionally boosting score for category 1
        elif category == 2 and seeking_user["occupation_id_of_self"] != target_user["occupation_id"]:
            score *= 1/2 # Conditionally supressing score for category 2
        
    return score

def match(user_id: str, available_users: dict) -> list:
    """
    Find matches for user_id among available_users
    user attributes:
    {
        'id': 'eERRZrZsmFN6UrOn9b4s',
        'age_of_self': 61,
        'gender_of_self': 'F',
        'occupation_id_of_self': '0',
        'gender_preference': ['M'],
        'passion_ids': ['15', '2', '3', '9'],
        'occupation_id': '4',
        'age_lower_bound': 49,
        'age_upper_bound': 63,
        'similarity_preference': 'D'
    }
    """
    category_1 = []
    category_2 = []

    seeking_user = available_users[user_id]

    for id, target_user in available_users.items():
        # print(target_user)
        if id != user_id:
            availability = is_available(seeking_user, target_user)
            if availability == 1:
                category_1.append(dict(target_user))
            elif availability == 2:
                category_2.append(dict(target_user))
    
    for target_user in category_1:
        target_user['score'] = passion_occupation_score(seeking_user, target_user, 1)
    
    for target_user in category_2:
        target_user['score'] = passion_occupation_score(seeking_user, target_user, 2)
    
    target_users = category_1 + category_2
    target_users.sort(key=lambda target_user: target_user['score'], reverse=True)

    return target_users[0:20]


    