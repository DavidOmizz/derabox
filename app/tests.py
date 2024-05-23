from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from app.models import Order, User, CustomerProfile


# Needs user object to work -------------------------------------
# class OrderModelTests(TestCase):
#     def test_generate_tracking_number(self):
#         # Create a new Order object
#         order = Order.objects.create(user_id=1, status='Pending', product_name='Test Product')
        
#         # Ensure that the tracking_number is generated correctly
#         # The tracking_number format should be 'TKYYYYNNNNN' where YYYY is the current year and NNNNN is a sequential number starting from 00001
#         expected_tracking_number = f'TK{order.created_at.year}{str(order.pk).zfill(5)}'
#         self.assertEqual(order.tracking_number, expected_tracking_number)


class OrderModelTests(TestCase):
    def test_generate_tracking_number(self):
        # Create a new User object
        user = User.objects.create(username='test_user', email='test@example.com')
        
        # Create a new Order object
        order = Order.objects.create(user=user, status='Pending', product_name='Test Product')
        
        # Ensure that the tracking_number is generated correctly
        # The tracking_number format should be 'TKYYYYNNNNN' where YYYY is the current year and NNNNN is a sequential number starting from 00001
        expected_tracking_number = f'TK{order.created_at.year}{str(order.pk).zfill(5)}'
        self.assertEqual(order.tracking_number, expected_tracking_number)
        
class CustomerProfileModelTests(TestCase):
    def test_customer_profile_str(self):
        # Create a new User object
        user = User.objects.create(username='test_user', email='test@example.com')
        
        # Create a new CustomerProfile object associated with the user
        customer_profile = CustomerProfile.objects.create(user=user, profile_picture='profile_picture.jpg', address='Test Address')
        
        # Ensure that the __str__ method returns the username of the associated user
        self.assertEqual(str(customer_profile), user.username)
        
        
        
        
        
    # class PostTestCase(TestCase):
    # def testPost(self):
    #     post = Post(title="My Title", description="Blurb", wiki="Post Body")
    #     self.assertEqual(post.title, "My Title")
    #     self.assertEqual(post.description, "Blurb")
        self.assertEqual(post.wiki, "Post Body")