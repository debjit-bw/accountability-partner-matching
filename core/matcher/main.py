from core.matcher.exports.files import passions
from core.matcher.utils.onehot import make_onehot
from core.matcher.utils.dot import dot_product
from core.matcher.utils.availability import is_available


class matcher:
    def __init__(
        self,
        parameters: list = [
            2 / 3,
            1 / 2,
            3 / 2,
            1 / 2,
        ],
    ):
        assert len(parameters) == 5
        self.p0 = parameters[0]
        self.p1 = parameters[1]
        self.p2 = parameters[2]
        self.p3 = parameters[3]
        self.p4 = parameters[4]

    def passion_occupation_score(
        self, seeking_user: dict, target_user: dict, category: int
    ) -> float:
        """
        Returns the passion score for seeking_user and target_user
        """
        passion_ids = seeking_user["passion_ids"]
        target_passion_ids = target_user["passion_ids"]
        passion_vector = make_onehot(passion_ids, passions)
        target_passion_vector = make_onehot(target_passion_ids, passions)

        # From documentation
        if seeking_user["similarity_preference"] == "D":
            score = (
                len(passion_vector) - dot_product(passion_vector, target_passion_vector)
            ) * 100
            if (
                category == 1
                and seeking_user["occupation_id"] == target_user["occupation_id"]
            ):
                score *= self.p0  # Conditionally supressing score for category 1
                # score *= 2/3 # Conditionally supressing score for category 1
            elif (
                category == 2
                and seeking_user["occupation_id"] == target_user["occupation_id"]
            ):
                score *= self.p1  # Conditionally supressing score for category 2
                # score *= 1/2 # Conditionally supressing score for category 2

        # From documentation
        elif seeking_user["similarity_preference"] == "S":
            score = dot_product(passion_vector, target_passion_vector) * 100
            if (
                category == 1
                and seeking_user["occupation_id"] == target_user["occupation_id"]
            ):
                score *= self.p2  # Conditionally boosting score for category 1
                # score *= 3 / 2  # Conditionally boosting score for category 1
            elif (
                category == 2
                and seeking_user["occupation_id"] != target_user["occupation_id"]
            ):
                score *= self.p3  # Conditionally supressing score for category 2
                # score *= 1 / 2  # Conditionally supressing score for category 2
        
        if seeking_user["similarity_preference"] == target_user["similarity_preference"]:
            score *= self.p4

        return score

    def get_suggestions(self, user_id: str, available_users: dict) -> list:
        """
        Find matches for user_id among available_users
        user attributes:
        {
            'id': 'eERRZrZsmFN6UrOn9b4s',
            'age': 61,
            'gender': 'F',
            'occupation_id': '0',
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
            target_user["score"] = self.passion_occupation_score(
                seeking_user, target_user, 1
            )

        for target_user in category_2:
            target_user["score"] = self.passion_occupation_score(
                seeking_user, target_user, 2
            )

        target_users = category_1 + category_2
        target_users.sort(key=lambda target_user: target_user["score"], reverse=True)

        if len(target_users) > 20:
            return target_users[0:20]
        else:
            return target_users
