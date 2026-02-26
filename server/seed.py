import asyncio
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine, Base
from app.models.user import User
from app.models.menu import MenuCategory, MenuItem
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.services.auth_service import auth_service

async def seed_data():
    async with AsyncSessionLocal() as db:
        # 1. Create Users
        print("Seeding Users...")
        admin = User(
            full_name="Admin User",
            email="admin@tablemind.ai",
            password_hash=auth_service.get_password_hash("admin123"),
            role="admin"
        )
        test_user = User(
            full_name="Test Customer",
            email="test@example.com",
            password_hash=auth_service.get_password_hash("password123"),
            role="user"
        )
        db.add_all([admin, test_user])
        await db.flush()

        # 2. Create Categories
        print("Seeding Categories...")
        cat_burgers = MenuCategory(name="Burgers", description="Juicy burgers and sliders")
        cat_pizza = MenuCategory(name="Pizza", description="Artisan pizzas")
        cat_drinks = MenuCategory(name="Drinks", description="Refreshing beverages")
        db.add_all([cat_burgers, cat_pizza, cat_drinks])
        await db.flush()

        # 3. Create Menu Items
        print("Seeding Menu Items...")
        items = [
            MenuItem(
                category_id=cat_burgers.id,
                name="Classic Beef Burger",
                description="100% Angus beef, cheddar, lettuce, tomato, special sauce",
                price=Decimal("12.99"),
                is_vegetarian=False,
                is_spicy=False
            ),
            MenuItem(
                category_id=cat_burgers.id,
                name="Spicy Veggie Burger",
                description="Quinoa & black bean patty, avocado, spicy mayo",
                price=Decimal("11.50"),
                is_vegetarian=True,
                is_spicy=True
            ),
            MenuItem(
                category_id=cat_pizza.id,
                name="Margherita Pizza",
                description="Fresh mozzarella, basil, tomato sauce, olive oil",
                price=Decimal("14.00"),
                is_vegetarian=True,
                is_spicy=False
            ),
            MenuItem(
                category_id=cat_pizza.id,
                name="Pepperoni Feast",
                description="Loaded with pepperoni and extra mozzarella",
                price=Decimal("16.50"),
                is_vegetarian=False,
                is_spicy=True
            ),
            MenuItem(
                category_id=cat_drinks.id,
                name="Craft Cola",
                description="Small-batch organic cola",
                price=Decimal("3.50"),
                is_vegetarian=True,
                is_spicy=False
            )
        ]
        db.add_all(items)
        await db.flush()

        # 4. Create Historical Orders (for Analytics)
        print("Seeding Orders...")
        # Order 1 (Completed)
        order1 = Order(
            user_id=test_user.id,
            status="completed",
            total_amount=Decimal("29.49"), # Burger + Pizza + Cola - slight variation for realism
            created_at=datetime.now() - timedelta(days=2)
        )
        db.add(order1)
        await db.flush()
        
        oi1 = OrderItem(
            order_id=order1.id,
            menu_item_id=items[0].id,
            quantity=1,
            price_at_order=items[0].price,
            subtotal=items[0].price
        )
        oi2 = OrderItem(
            order_id=order1.id,
            menu_item_id=items[2].id,
            quantity=1,
            price_at_order=items[2].price,
            subtotal=items[2].price
        )
        db.add_all([oi1, oi2])
        
        p1 = Payment(
            order_id=order1.id,
            payment_method="credit_card",
            payment_status="success",
            transaction_id="TXN12345",
            paid_at=datetime.now() - timedelta(days=2)
        )
        db.add(p1)

        # Order 2 (Pending)
        order2 = Order(
            user_id=test_user.id,
            status="pending",
            total_amount=Decimal("11.50"),
            created_at=datetime.now() - timedelta(minutes=5),
            cancellation_deadline=datetime.now() + timedelta(minutes=2)
        )
        db.add(order2)
        await db.flush()
        
        oi3 = OrderItem(
            order_id=order2.id,
            menu_item_id=items[1].id,
            quantity=1,
            price_at_order=items[1].price,
            subtotal=items[1].price
        )
        db.add(oi3)

        await db.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
