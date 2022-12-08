from users.models import Profile


class ProfileService:

    @staticmethod
    def profile_create(user, number):
        profile = Profile.objects.create(user, number)
        return profile
