from core.matcher.utils.availability import is_available

def score_algorithm(seeking_user, algorithm_suggestions):
    """
    Scores a given algorithm output based on seeking_user's preferences

    user attributes:
    {
        'id': 'eERRZrZsmFN6UrOn9b4s',
        'age': 61,
        'gender': 'F',
        'gender_preference': ['M'],
        'passion_ids': ['15', '2', '3', '9'],
        'occupation_id': '4',
        'age_lower_bound': 49,
        'age_upper_bound': 63,
        'similarity_preference': 'D'
    }
    Scoring:
        10 for lying inside age limit (is_available returns 1)
        -5 for lying outside age limit +- 5 (is_available returns 2)

        For similarity_preference == "S":
            +5 for each matching passion
            -5 for each non-matching passion

            +10 for a matching occupation
            -5 for a non-matching occupation
        
        For similarity_preference == "D":
            +5 for each non-matching passion
            -5 for each matching passion

            +10 for a non-matching occupation
            -5 for a matching occupation
        
        For similarity_preference:
            +10 if it matches for both users
            -10 if it doesn't match for both users

    """

    score = 0

    for suggested_user in algorithm_suggestions:
        availability = is_available(seeking_user, suggested_user)
        if availability == 1:
            score += 10
        elif availability == 2:
            score -= 5
        
        if seeking_user['similarity_preference'] == 'S':
            for passion_id in seeking_user['passion_ids']:
                if passion_id in suggested_user['passion_ids']:
                    score += 5
                else:
                    score -= 5
            
            if seeking_user['occupation_id'] == suggested_user['occupation_id']:
                score += 10
            else:
                score -= 5
        else:
            for passion_id in suggested_user['passion_ids']:
                if passion_id in seeking_user['passion_ids']:
                    score -= 5
                else:
                    score += 5
            
            if seeking_user['occupation_id'] == suggested_user['occupation_id']:
                score -= 5
            else:
                score += 10
        
        if seeking_user["similarity_preference"] == suggested_user["similarity_preference"]:
            score += 10
        else:
            score -= 10
    
    return score / len(algorithm_suggestions)
