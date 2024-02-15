class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.quantity = 0

class Cart:
    def __init__(self):
        self.products = []
        self.gift_wrap_fee = 1
        self.shipping_fee_per_package = 5
        self.discount_rules = {
            "flat_10_discount": lambda total_quantity, total_price, product_quantities, prices: 10 if total_price > 200 else 0,
            "bulk_5_discount": lambda total_quantity, total_price, product_quantities, prices: sum(price * 0.05 for price, qty in zip(prices, product_quantities) if qty > 10) if total_quantity > 20 else 0,
            "bulk_10_discount": lambda total_quantity, total_price, product_quantities, prices: total_price * 0.1 if total_quantity > 20 else 0,
            "tiered_50_discount": lambda total_quantity, total_price, product_quantities, prices: self.tiered_discount(total_quantity, product_quantities, prices)
        }

    def add_product(self, product, quantity, gift_wrap=False):
        product.quantity = quantity
        if gift_wrap:
            self.gift_wrap_fee += quantity
        self.products.append(product)

    def tiered_discount(self, total_quantity, product_quantities, prices):
        if total_quantity > 30 and any(qty > 15 for qty in product_quantities):
            excess_quantity = sum(qty - 15 for qty in product_quantities if qty > 15)
            return sum(prices[i] * 0.5 * (qty - 15) for i, qty in enumerate(product_quantities) if qty > 15), excess_quantity
        return 0, 0

    def calculate_total(self):
        total_quantity = sum(product.quantity for product in self.products)
        total_price = sum(product.quantity * product.price for product in self.products)
        discounts = {}
        for name, rule in self.discount_rules.items():
            discount_result = rule(total_quantity, total_price, [product.quantity for product in self.products], [product.price for product in self.products])
            if isinstance(discount_result, tuple):
                discounts[name] = discount_result[0]
            else:
                discounts[name] = discount_result
        max_discount = max(discounts.values())
        discount_name = [name for name, discount in discounts.items() if discount == max_discount][0]
        discount_amount = max_discount
        shipping_fee = (total_quantity + 9) // 10 * self.shipping_fee_per_package
        subtotal = total_price
        total = subtotal - discount_amount + self.gift_wrap_fee + shipping_fee
        return {
            "subtotal": subtotal,
            "discount_name": discount_name,
            "discount_amount": discount_amount,
            "shipping_fee": shipping_fee,
            "gift_wrap_fee": self.gift_wrap_fee,
            "total": total
        }


# Example usage:
product_a = Product("Product A", 20)
product_b = Product("Product B", 40)
product_c = Product("Product C", 50)

cart = Cart()
cart.add_product(product_a, 8, gift_wrap=True)
cart.add_product(product_b, 12)
cart.add_product(product_c, 18)

total_details = cart.calculate_total()

for product in cart.products:
    print(f"{product.name}: Quantity: {product.quantity}, Total: ${product.quantity * product.price}")

print(f"Subtotal: ${total_details['subtotal']}")
print(f"Discount Applied: {total_details['discount_name']}, Amount: ${total_details['discount_amount']}")
print(f"Shipping Fee: ${total_details['shipping_fee']}")
print(f"Gift Wrap Fee: ${total_details['gift_wrap_fee']}")
print(f"Total: ${total_details['total']}")
