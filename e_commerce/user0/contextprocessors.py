



from user0.models import OrderItem


def revenue_calculator(request):
    revenue = 0
    tax = 0
    total_revenue = 0
    try:
        order_items = OrderItem.objects.all()
        for item in order_items:
            revenue += item.item_total

        return dict(revenue=revenue)

    except OrderItem.DoesNotExist:
        pass

    