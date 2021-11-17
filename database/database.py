class db_manager:
    def __init__(self, fb) -> None:
        self.db = fb.client()

    def get_interested_users(self, is_test = True) -> dict:
        
        # Configuring test case
        if is_test:
            collection = u'test_AP_interested_users'
            document = u'all_users'
        else:
            collection = u'AP_interested_users'
            document = u'all_users'

        interested_users = self.db.collection(collection).document(document).get().to_dict()
        return interested_users