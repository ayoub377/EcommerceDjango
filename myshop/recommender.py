import redis
from django.conf import settings
from .models import Product

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class Recommender(object):

    def get_product_key(self, id, interaction_type):
        # Generate keys based on interaction type (purchase, view, cart)
        return f'product:{id}:{interaction_type}'

    def update_interaction(self, user_id, product_ids, interaction_type):
        # Update interactions for each product
        for product_id in product_ids:
            # Record user's interaction with the product
            r.zincrby(self.get_product_key(product_id, interaction_type), 1, user_id)

    def suggest_products_for(self, user_id, max_results=6):
        # Combine scores from purchase, view, and cart interactions
        interaction_types = ['purchased_with', 'viewed', 'added_to_cart']
        combined_scores = {}

        for interaction_type in interaction_types:
            # Get all product IDs the user interacted with
            product_ids = [int(id) for id in r.zrange(self.get_product_key(user_id, interaction_type), 0, -1)]
            # Aggregate scores across different interactions
            for product_id in product_ids:
                score = r.zscore(self.get_product_key(product_id, interaction_type), user_id) or 0
                print(score)
                combined_scores[product_id] = combined_scores.get(product_id, 0) + score

        # Sort products by combined scores and retrieve top recommendations
        suggestions = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:max_results]
        # Retrieve suggested products from database
        suggested_products = Product.objects.filter(id__in=[product_id for product_id, _ in suggestions])

        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id, 'purchased_with'))
