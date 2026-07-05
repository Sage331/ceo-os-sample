MOCK_SHOPIFY_RESPONSE = {
    "orders": [
        {
            "id": 1234567890,
            "total_price": "150.00",
            "currency": "USD",
            "line_items": [
                {"name": "Premium T-Shirt", "price": "50.00", "quantity": 2},
                {"name": "Classic Hat", "price": "25.00", "quantity": 2},
            ],
        },
        {
            "id": 9876543210,
            "total_price": "75.50",
            "currency": "USD",
            "line_items": [
                {"name": "Stylish Mug", "price": "15.50", "quantity": 1},
                {"name": "Logo Sticker Pack", "price": "10.00", "quantity": 6},
            ],
        },
    ]
}

MOCK_META_ADS_RESPONSE = {
    "campaigns": [
        {
            "id": "camp123",
            "name": "Summer Sale Campaign",
            "spend": 5000,
            "impressions": 100000,
        },
        {
            "id": "camp456",
            "name": "New Product Launch",
            "spend": 12000,
            "impressions": 250000,
        },
    ]
}

MOCK_TIKTOK_SHOP_RESPONSE = {"store_revenue": {"total": 2500.75, "currency": "USD"}}
