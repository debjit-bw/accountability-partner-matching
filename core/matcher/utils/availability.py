from core.matcher.ages import age_lower_bound, age_upper_bound

def age_in_range(seeking_user, target_user):
    """
    Returns True if target_user is within seeking_user's age range
    """
    lower_bound = max(seeking_user['age_lower_bound'] - 5, age_lower_bound)
    upper_bound = min(seeking_user['age_upper_bound'] + 5, age_upper_bound)
    target_user_in_range = lower_bound <= target_user['age'] <= upper_bound
    
    lower_bound = max(target_user['age_lower_bound'] - 5, age_lower_bound)
    upper_bound = min(target_user['age_upper_bound'] + 5, age_upper_bound)
    seeking_user_in_range = lower_bound <= seeking_user['age'] <= upper_bound

    if target_user_in_range and seeking_user_in_range:
        return True
    else:
        return False

def is_available(seeking_user, target_user):
    """
    Returns True if target_user is available for seeking_user
    """
    if target_user["gender"] in seeking_user["gender_preference"] and seeking_user["gender"] in target_user["gender_preference"]:
        if age_in_range(seeking_user, target_user):
            return 1
        else:
            return 2
    return 0