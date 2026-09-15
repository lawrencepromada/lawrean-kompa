from app.models import LineItem, Offer, SourceLocation


def test_line_item_preserves_source_and_values():
    source = SourceLocation(
        page=2,
        text="Business laptops 7 $800 $5,600",
    )

    item = LineItem(
        description="Business laptops",
        quantity=7,
        unit_price=800,
        stated_total=5600,
        source=source,
    )

    assert item.description == "Business laptops"
    assert item.quantity == 7
    assert item.unit_price == 800
    assert item.stated_total == 5600
    assert item.source.page == 2


def test_offer_can_hold_multiple_items():
    source = SourceLocation(
        page=1,
        text="Network switches 2 $300 $600",
    )

    item = LineItem(
        description="Network switches",
        quantity=2,
        unit_price=300,
        stated_total=600,
        source=source,
    )

    offer = Offer(
        filename="original.pdf",
        currency="USD",
        line_items=[item],
        stated_grand_total=600,
    )

    assert len(offer.line_items) == 1
    assert offer.stated_grand_total == 600