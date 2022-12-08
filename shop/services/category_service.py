from shop.models import Category


class CategoryService:

    @staticmethod
    def all_categories():
        categories = Category.objects.all()
        return categories
