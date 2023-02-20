from django.test import TestCase
from django.urls import reverse
from store.models import Coupon, Item

class CouponModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Coupon.objects.create(code='BlackFriday', amount=50)

    def test_code_max_length(self):
        coupon = Coupon.objects.get(id=1)
        max_length = coupon._meta.get_field('code').max_length
        self.assertEquals(max_length, 15)

class ItemModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Item.objects.create(
            title='iPhone',
            price = 123,
            discount_price=100,
            category='PH',
            label='P',
            slug=123,
            description='Small description',
        )

    def test_title_max_length(self):
        item = Item.objects.get(id=1)
        max_length = item._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_get_absolute_url(self):
        item = Item.objects.get(id=1)
        self.assertEquals(item.get_absolute_url(), '/product/123/')

    def test_discount_less_than_price(self):
        item = Item.objects.get(id=1)
        self.assertTrue(item.discount_price < item.price)

    def test_img_is_null(self):
        item = Item.objects.get(id=1)
        is_null = item._meta.get_field('image').null
        self.assertEquals(is_null, True)

    def test_discount_price_is_null(self):
        item = Item.objects.get(id=1)
        is_null = item._meta.get_field('discount_price').null
        self.assertEquals(is_null, True)

class HomeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_items = 13
        for item_num in range(number_of_items):
            Item.objects.create(
                title=f'Title {item_num}',
                price=item_num,
                category="TV",
                label='P',
                slug=item_num,
                description=f'Description {item_num}',   
            )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'home.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['item_list']) == 10)

    def test_lists_all_authors(self):
        #Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('home')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['item_list']) == 3) 

