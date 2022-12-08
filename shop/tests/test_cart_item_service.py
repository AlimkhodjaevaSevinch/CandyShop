from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock, call
from shop.services.cart_item_service import CartItemServices


class CartItemServiceTest(SimpleTestCase):
    @patch('shop.services.cart_item_service.CandyItem')
    def test_add_cart_item_get(self, candy_item_patch):
        order_mock = MagicMock()
        candy_mock = MagicMock()
        amount = 42
        cart_item_mock = MagicMock(amount=2)
        is_created = False
        candy_item_patch.objects.get_or_create.return_value = cart_item_mock, is_created

        result = CartItemServices.add_cart_item(order_mock, candy_mock, amount)

        self.assertEqual(result, cart_item_mock)
        self.assertEqual(result.amount, amount + 2)
        candy_item_patch.objects.get_or_create.assert_called_once_with(
            order=order_mock,
            candy=candy_mock,
        )
        cart_item_mock.save.assert_called_once_with()

    @patch('shop.services.cart_item_service.CandyItem')
    def test_add_cart_item_create(self, candy_item_patch):
        order_mock = MagicMock()
        candy_mock = MagicMock()
        amount = 42
        cart_item_mock = MagicMock()
        is_created = True
        candy_item_patch.objects.get_or_create.return_value = cart_item_mock, is_created

        result = CartItemServices.add_cart_item(order_mock, candy_mock, amount)

        self.assertEqual(result, cart_item_mock)
        self.assertEqual(result.amount, amount)
        candy_item_patch.objects.get_or_create.assert_called_once_with(
            order=order_mock,
            candy=candy_mock,
        )
        cart_item_mock.save.assert_called_once_with()

    def test_get_candy_items_by_order(self):
        order_mock = MagicMock()
        candy_items_mock = MagicMock()
        order_mock.candy_items.all.return_value = candy_items_mock

        result = CartItemServices.get_candy_items_by_order(order_mock)

        self.assertEqual(result, candy_items_mock)
        order_mock.candy_items.all.assert_called_once_with()

    @patch('shop.services.cart_item_service.F')
    def test_calculate_total_for_each_candy_item(self, f_patch):
        candy_items_mock = MagicMock()
        annotated_candy_items_mock = MagicMock()
        candy_price_f_mock = MagicMock()
        amount_f_mock = MagicMock()
        f_patch.side_effect = [candy_price_f_mock, amount_f_mock]
        candy_items_mock.annotate.return_value = annotated_candy_items_mock

        result = CartItemServices.calculate_total_for_each_candy_item(candy_items_mock)

        self.assertEqual(result, annotated_candy_items_mock)
        f_patch.assert_has_calls([
            call('candy__price'),
            call('amount'),
        ])
        candy_items_mock.annotate.assert_called_once_with(
            total=candy_price_f_mock * amount_f_mock,
        )

    @patch('shop.services.cart_item_service.Sum')
    def test_calculate_total_price(self, sum_patch):
        candy_items_mock = MagicMock()
        candy_items_mock.aggregate.return_value = {'total_price': 100}
        sum_mock = MagicMock()
        sum_patch.return_value = sum_mock

        result = CartItemServices.calculate_total_price(candy_items_mock)

        self.assertEqual(result, 100)
        sum_patch.assert_called_once_with('total')
        candy_items_mock.aggregate.assert_called_once_with(
            total_price=sum_mock
        )
