# Custom filters and functions for Jinja2 templates.
def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def eur(value):
    """Format value as EUR."""
    return f"€{value:,.2f}"

def discount(value, discount):
    """Calculate discount and format value as EUR."""
    return f"€{value - (value * discount / 100):,.2f}"