from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import mysql.connector
import pandas as pd

# ===========================
# Database connection helper
# ===========================

def get_connection():
    """
    Create a new connection to the ShopSmart MySQL database.
    Adjust user/password/host if your XAMPP config is different.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # set if you use a MySQL password
        database="ShopSmart"
    )

# ===========================
# Data helper functions
# ===========================

def fetch_kpis():
    """
    Fetch simple KPI metrics for the Overview tab.
    Returns a dict with total_revenue, total_orders, total_customers, total_products.
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Total revenue (sum of quantity * unit_price across all order items)
    cur.execute(
        """
        SELECT COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_revenue
        FROM OrderItem oi
        """
    )
    total_revenue = cur.fetchone()["total_revenue"]

    # Total orders
    cur.execute("SELECT COUNT(*) AS total_orders FROM `Order`")
    total_orders = cur.fetchone()["total_orders"]

    # Total customers
    cur.execute("SELECT COUNT(*) AS total_customers FROM Customer")
    total_customers = cur.fetchone()["total_customers"]

    # Total products
    cur.execute("SELECT COUNT(*) AS total_products FROM Product")
    total_products = cur.fetchone()["total_products"]

    cur.close()
    conn.close()

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_products": total_products,
    }


def fetch_categories():
    """
    Fetch all categories for the products dropdown (filter).
    Returns a list of dicts {label, value}.
    """
    conn = get_connection()
    df = pd.read_sql("SELECT category_id, name FROM Category ORDER BY name", conn)
    conn.close()

    return [
        {"label": row["name"], "value": int(row["category_id"])}
        for _, row in df.iterrows()
    ]


def fetch_products_for_dropdown():
    """
    Fetch all products as label/value pairs for write-action dropdowns.
    """
    conn = get_connection()
    df = pd.read_sql("SELECT product_id, name FROM Product ORDER BY name", conn)
    conn.close()

    return [
        {"label": f'{row["name"]} (ID {int(row["product_id"])})',
         "value": int(row["product_id"])}
        for _, row in df.iterrows()
    ]


def fetch_low_stock():
    """
    Fetch low-stock products based on Inventory table.
    Returns a DataFrame with product name, quantity_on_hand, reorder_level.
    """
    conn = get_connection()
    query = """
        SELECT p.name,
               i.quantity_on_hand,
               i.reorder_level
        FROM Inventory i
        JOIN Product p ON i.product_id = p.product_id
        WHERE i.quantity_on_hand < i.reorder_level
        ORDER BY i.quantity_on_hand ASC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# ===========================
# Layout helper components
# ===========================

def kpi_card(title, value_str):
    """
    Simple card to display KPI metrics in the overview tab.
    """
    return html.Div(
        style={
            "border": "1px solid #ddd",
            "borderRadius": "8px",
            "padding": "12px 16px",
            "minWidth": "180px",
            "boxShadow": "0 1px 3px rgba(0,0,0,0.08)",
            "backgroundColor": "#fff",
        },
        children=[
            html.Div(title, style={"fontSize": "13px", "color": "#777"}),
            html.Div(value_str, style={"fontSize": "22px", "fontWeight": "bold"}),
        ],
    )


def overview_layout():
    """
    Layout for the Overview tab.
    KPIs are fetched live from the database each time the tab is viewed.
    """
    kpis = fetch_kpis()

    # Format total_revenue as currency
    total_revenue_str = f"${kpis['total_revenue']:,.2f}"
    total_orders_str = f"{kpis['total_orders']:,}"
    total_customers_str = f"{kpis['total_customers']:,}"
    total_products_str = f"{kpis['total_products']:,}"

    return html.Div(
        children=[
            html.Div(
                style={"display": "flex", "gap": "20px", "flexWrap": "wrap"},
                children=[
                    kpi_card("Total Revenue", total_revenue_str),
                    kpi_card("Total Orders", total_orders_str),
                    kpi_card("Total Customers", total_customers_str),
                    kpi_card("Total Products", total_products_str),
                ],
            ),
            html.P(
                "Overview of key ShopSmart performance metrics. "
                "These values are calculated from the underlying MySQL ShopSmart database.",
                style={"marginTop": "20px", "color": "#555"},
            ),
        ]
    )


def sales_layout():
    """
    Layout for the Sales tab: date filter + revenue by category chart
    + 'Create Demo Order' write-action.
    """
    return html.Div(
        children=[
            html.Div(
                style={"marginBottom": "20px"},
                children=[
                    html.Label("Filter by order date:", style={"marginRight": "10px"}),
                    dcc.DatePickerRange(
                        id="rev-date-range",
                        display_format="YYYY-MM-DD",
                    ),
                ],
            ),
            dcc.Graph(id="rev-by-category-graph"),

            html.Hr(style={"margin": "30px 0"}),

            html.H3("Simulate Customer Order (Demo Action)"),
            html.P(
                "Create a demo order for a selected product. "
                "This will insert into Order and OrderItem, trigger inventory deduction "
                "and order total recalculation, and update the revenue chart.",
                style={"color": "#555"},
            ),
            html.Div(
                style={"display": "flex", "gap": "10px", "alignItems": "center", "flexWrap": "wrap"},
                children=[
                    html.Label("Product:", style={"minWidth": "70px"}),
                    dcc.Dropdown(
                        id="demo-order-product",
                        options=fetch_products_for_dropdown(),
                        placeholder="Select a product",
                        style={"width": "260px"},
                    ),
                    html.Label("Quantity:", style={"marginLeft": "10px"}),
                    dcc.Input(
                        id="demo-order-qty",
                        type="number",
                        min=1,
                        step=1,
                        value=1,
                        style={"width": "100px"},
                    ),
                    html.Button(
                        "Create Demo Order",
                        id="demo-order-button",
                        n_clicks=0,
                        style={"marginLeft": "10px"},
                    ),
                ],
            ),
            html.Div(id="demo-order-status", style={"marginTop": "10px", "color": "#007700"}),
        ]
    )


def products_layout():
    """
    Layout for the Products tab: category filter + ratings chart
    + 'Add Review' write-action.
    """
    return html.Div(
        children=[
            html.Div(
                style={"marginBottom": "10px"},
                children=[
                    html.Label("Filter by category:", style={"marginRight": "10px"}),
                    dcc.Dropdown(
                        id="rating-category-filter",
                        placeholder="All categories",
                        clearable=True,
                        style={"width": "300px"},
                    ),
                ],
            ),
            dcc.Graph(id="product-ratings-graph"),

            html.Hr(style={"margin": "30px 0"}),

            html.H3("Add Product Review (Demo Action)"),
            html.P(
                "Simulate a customer adding a review. "
                "This inserts into the Review table, triggers a rating recalculation, "
                "and updates the ratings chart.",
                style={"color": "#555"},
            ),
            html.Div(
                style={"display": "flex", "flexDirection": "column", "gap": "8px", "maxWidth": "500px"},
                children=[
                    html.Div(
                        style={"display": "flex", "gap": "10px", "alignItems": "center"},
                        children=[
                            html.Label("Product:", style={"minWidth": "70px"}),
                            dcc.Dropdown(
                                id="review-product",
                                options=fetch_products_for_dropdown(),
                                placeholder="Select a product",
                                style={"flex": 1},
                            ),
                        ],
                    ),
                    html.Div(
                        style={"display": "flex", "gap": "10px", "alignItems": "center"},
                        children=[
                            html.Label("Rating (1–5):", style={"minWidth": "100px"}),
                            dcc.RadioItems(
                                id="review-rating",
                                options=[{"label": str(i), "value": i} for i in range(1, 6)],
                                value=5,  # default selected rating
                                labelStyle={"display": "inline-block", "marginRight": "10px"},
                            ),
                        ],
                    ),
                    # html.Div(
                    #     style={"display": "flex", "gap": "10px", "alignItems": "center"},
                    #     children=[
                    #         html.Label("Rating (1–5):", style={"minWidth": "100px"}),
                    #         dcc.Slider(
                    #             id="review-rating",
                    #             min=1,
                    #             max=5,
                    #             step=1,
                    #             value=5,
                    #             marks={i: str(i) for i in range(1, 6)},
                    #         ),
                    #     ],
                    # ),
                    dcc.Textarea(
                        id="review-comment",
                        placeholder="Optional comment...",
                        style={"width": "100%", "height": "80px"},
                    ),
                    html.Button("Add Review", id="add-review-button", n_clicks=0),
                    html.Div(id="add-review-status", style={"marginTop": "6px", "color": "#007700"}),
                ],
            ),
        ]
    )


def inventory_layout():
    """
    Layout for the Inventory tab: restock action + low stock table.
    """
    return html.Div(
        children=[
            html.H3("Restock Inventory (Merchant Action)"),
            html.P(
                "Select a product and quantity to restock. "
                "This updates Inventory and refreshes the low-stock alerts.",
                style={"color": "#555"},
            ),
            html.Div(
                style={"display": "flex", "gap": "10px", "alignItems": "center", "flexWrap": "wrap"},
                children=[
                    html.Label("Product:", style={"minWidth": "70px"}),
                    dcc.Dropdown(
                        id="restock-product",
                        options=fetch_products_for_dropdown(),
                        placeholder="Select a product",
                        style={"width": "260px"},
                    ),
                    html.Label("Quantity to add:", style={"marginLeft": "10px"}),
                    dcc.Input(
                        id="restock-amount",
                        type="number",
                        min=1,
                        step=1,
                        value=10,
                        style={"width": "120px"},
                    ),
                    html.Button(
                        "Restock",
                        id="restock-button",
                        n_clicks=0,
                        style={"marginLeft": "10px"},
                    ),
                ],
            ),
            html.Div(id="restock-status", style={"marginTop": "10px", "color": "#007700"}),

            html.Hr(style={"margin": "30px 0"}),

            html.H3("Low Stock Alerts"),
            html.P(
                "Products with quantity on hand below their reorder level.",
                style={"color": "#555"},
            ),
            dash_table.DataTable(
                id="low-stock-table",
                columns=[
                    {"name": "Product", "id": "name"},
                    {"name": "Quantity On Hand", "id": "quantity_on_hand"},
                    {"name": "Reorder Level", "id": "reorder_level"},
                ],
                style_table={"marginTop": "10px", "maxWidth": "600px"},
                style_cell={"textAlign": "left", "padding": "6px"},
                style_header={
                    "fontWeight": "bold",
                    "backgroundColor": "#f5f5f5",
                },
            ),
        ]
    )


# ===========================
# Dash app setup
# ===========================

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # for deployment if needed

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "padding": "20px", "backgroundColor": "#fafafa"},
    children=[
        html.Div(
            style={"marginBottom": "20px"},
            children=[
                html.H1("ShopSmart Analytics", style={"marginBottom": "0px"}),
                html.P(
                    "E-commerce dashboard powered by the ShopSmart MySQL database",
                    style={"color": "#555", "marginTop": "4px"},
                ),
            ],
        ),
        dcc.Tabs(
            id="main-tabs",
            value="tab-overview",
            children=[
                dcc.Tab(label="Overview", value="tab-overview"),
                dcc.Tab(label="Sales", value="tab-sales"),
                dcc.Tab(label="Products", value="tab-products"),
                dcc.Tab(label="Inventory", value="tab-inventory"),
            ],
        ),
        html.Div(id="tab-content", style={"marginTop": "20px"}),
    ],
)


# ===========================
# Callbacks
# ===========================

@app.callback(
    Output("tab-content", "children"),
    Input("main-tabs", "value"),
)
def render_tab(tab_value):
    """
    Render the content of the currently selected tab.
    """
    if tab_value == "tab-overview":
        return overview_layout()
    elif tab_value == "tab-sales":
        return sales_layout()
    elif tab_value == "tab-products":
        return products_layout()
    elif tab_value == "tab-inventory":
        return inventory_layout()
    return html.Div("Unknown tab")


@app.callback(
    Output("rev-by-category-graph", "figure"),
    Input("rev-date-range", "start_date"),
    Input("rev-date-range", "end_date"),
    # Input("demo-order-button", "n_clicks"),
    Input("main-tabs", "value"),
)
def update_revenue_by_category(start_date, end_date, tab_value):
    """
    Update the revenue by category chart based on the selected date range.
    If no dates are chosen, show all orders.
    The demo-order button is included as an input so the chart refreshes
    after a new demo order is created.
    """
    if tab_value != "tab-sales":
        raise PreventUpdate
    conn = get_connection()
    query = """
        SELECT c.name AS category,
               SUM(oi.quantity * oi.unit_price) AS revenue
        FROM `Order` o
        JOIN OrderItem oi ON o.order_id = oi.order_id
        JOIN Product p ON oi.product_id = p.product_id
        JOIN Category c ON p.category_id = c.category_id
        WHERE (%s IS NULL OR o.order_date >= %s)
          AND (%s IS NULL OR o.order_date <= %s)
        GROUP BY c.name
        ORDER BY revenue DESC;
    """
    params = (start_date, start_date, end_date, end_date)
    df = pd.read_sql(query, conn, params=params)
    conn.close()

    if df.empty:
        x_vals = []
        y_vals = []
    else:
        x_vals = df["category"]
        y_vals = df["revenue"]

    figure = {
        "data": [
            {
                "type": "bar",
                "x": x_vals,
                "y": y_vals,
            }
        ],
        "layout": {
            "title": "Revenue by Category",
            "yaxis": {"title": "Revenue"},
            "xaxis": {"title": "Category"},
        },
    }
    return figure


@app.callback(
    Output("rating-category-filter", "options"),
    Input("main-tabs", "value"),
)
def populate_category_dropdown(tab_value):
    """
    Populate the category dropdown when the Products tab is selected.
    """
    if tab_value != "tab-products":
        return []
    return fetch_categories()


@app.callback(
    Output("product-ratings-graph", "figure"),
    Input("rating-category-filter", "value"),
    Input("add-review-button", "n_clicks"),
)
def update_product_ratings(category_id, n_clicks_add_review):
    """
    Update the product ratings chart, optionally filtering by category.
    Uses Product.avg_rating and Product.review_count, which are maintained
    by triggers and the initial backfill query.
    The add-review button triggers a refresh after a new review is added.
    """
    conn = get_connection()
    base_query = """
        SELECT p.name,
               p.avg_rating,
               p.review_count
        FROM Product p
    """
    params = None
    if category_id:
        base_query += " WHERE p.category_id = %s"
        params = (category_id,)

    base_query += " ORDER BY p.name;"

    df = pd.read_sql(base_query, conn, params=params)
    conn.close()

    if df.empty:
        x_vals = []
        y_vals = []
        text_vals = []
    else:
        x_vals = df["name"]
        y_vals = df["avg_rating"]
        text_vals = [f"Reviews: {int(rc)}" for rc in df["review_count"]]

    figure = {
        "data": [
            {
                "type": "bar",
                "x": x_vals,
                "y": y_vals,
                "text": text_vals,
                "textposition": "auto",
            }
        ],
        "layout": {
            "title": "Average Rating by Product",
            "yaxis": {"title": "Average Rating (1–5)", "range": [0, 5]},
            "xaxis": {"title": "Product"},
        },
    }
    return figure


@app.callback(
    Output("low-stock-table", "data"),
    Input("main-tabs", "value"),
    Input("restock-button", "n_clicks"),
    Input("demo-order-button", "n_clicks"),
)
def update_low_stock_table(tab_value, n_clicks_restock, n_clicks_demo_order):
    """
    Populate the low-stock table whenever the Inventory tab is active,
    and refresh after restock or demo-order actions.
    """
    if tab_value != "tab-inventory":
        return []
    df = fetch_low_stock()
    return df.to_dict("records")


# ===========================
# Write-action callbacks
# ===========================

@app.callback(
    Output("restock-status", "children"),
    Input("restock-button", "n_clicks"),
    State("restock-product", "value"),
    State("restock-amount", "value"),
    prevent_initial_call=True,
)
def restock_product(n_clicks, product_id, amount):
    """
    Restock a product by adding the specified quantity to Inventory.
    """
    if not product_id or not amount or amount <= 0:
        return "Please select a product and enter a positive quantity."

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Get product name for nicer status message
        cur.execute("SELECT name FROM Product WHERE product_id = %s", (product_id,))
        row = cur.fetchone()
        product_name = row[0] if row else f"ID {product_id}"

        # Update inventory directly (you could call sp_restock_product here instead)
        cur.execute(
            """
            UPDATE Inventory
            SET quantity_on_hand = quantity_on_hand + %s,
                last_restocked_at = NOW()
            WHERE product_id = %s
            """,
            (int(amount), int(product_id)),
        )
        conn.commit()
        cur.close()
        conn.close()

        return f"Restocked '{product_name}' by {int(amount)} units."
    except Exception as e:
        return f"Error during restock: {e}"


@app.callback(
    Output("demo-order-status", "children"),
    Input("demo-order-button", "n_clicks"),
    State("demo-order-product", "value"),
    State("demo-order-qty", "value"),
    prevent_initial_call=True,
)
def create_demo_order(n_clicks, product_id, qty):
    """
    Create a demo order:
      - Inserts into Order (fixed demo customer_id = 1)
      - Inserts into OrderItem using Product.price
      - Inserts Payment with total_amount
      - Triggers will update total_amount and inventory
    """
    if not product_id or not qty or qty <= 0:
        return "Please select a product and enter a positive quantity."

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Use demo customer_id = 1 for simplicity
        demo_customer_id = 1

        # 1) Insert into Order
        cur.execute(
            """
            INSERT INTO `Order` (customer_id, order_date, status, total_amount)
            VALUES (%s, NOW(), %s, 0)
            """,
            (demo_customer_id, "PENDING"),
        )
        order_id = cur.lastrowid

        # 2) Get unit price from Product
        cur.execute(
            "SELECT name, price FROM Product WHERE product_id = %s",
            (product_id,),
        )
        row = cur.fetchone()
        if not row:
            conn.rollback()
            cur.close()
            conn.close()
            return "Selected product not found."

        product_name, unit_price = row

        # 3) Insert into OrderItem
        cur.execute(
            """
            INSERT INTO OrderItem (order_id, product_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
            """,
            (order_id, int(product_id), int(qty), unit_price),
        )

        # Triggers should now update Order.total_amount and Inventory.

        # 4) Retrieve updated total_amount for payment
        cur.execute(
            "SELECT total_amount FROM `Order` WHERE order_id = %s",
            (order_id,),
        )
        row = cur.fetchone()
        total_amount = row[0] if row else unit_price * qty

        # 5) Insert Payment (simulate successful payment)
        cur.execute(
            """
            INSERT INTO Payment (order_id, method, amount, status, paid_at)
            VALUES (%s, 'CARD', %s, 'PAID', NOW())
            """,
            (order_id, total_amount),
        )


        conn.commit()
        cur.close()
        conn.close()

        return (
            f"Created demo order #{order_id} for {int(qty)} x '{product_name}'. "
            f"Total amount: ${total_amount:,.2f}."
        )
    except Exception as e:
        return f"Error creating demo order: {e}"


@app.callback(
    Output("add-review-status", "children"),
    Input("add-review-button", "n_clicks"),
    State("review-product", "value"),
    State("review-rating", "value"),
    State("review-comment", "value"),
    prevent_initial_call=True,
)
def add_review(n_clicks, product_id, rating, comment):
    """
    Add a review for a selected product.
    Uses a fixed demo customer_id to keep things simple.
    """
    if not product_id or not rating:
        return "Please select a product and rating."

    # Simple clamp for safety
    rating = max(1, min(5, int(rating)))

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Use a dedicated demo customer for reviews (e.g., customer_id = 2)
        demo_customer_id = 2

        # Get product name for nicer message
        cur.execute("SELECT name FROM Product WHERE product_id = %s", (product_id,))
        row = cur.fetchone()
        product_name = row[0] if row else f"ID {product_id}"

        # Insert review (your UNIQUE(product_id, customer_id) constraint still applies)
        cur.execute(
            """
            INSERT INTO Review (product_id, customer_id, rating, comment)
            VALUES (%s, %s, %s, %s)
            """,
            (int(product_id), demo_customer_id, rating, comment or ""),
        )

        # Trigger should recompute avg_rating and review_count for this product
        conn.commit()
        cur.close()
        conn.close()

        return f"Added review (rating {rating}) for '{product_name}'."
    except mysql.connector.IntegrityError as e:
        # Likely violating UNIQUE(product_id, customer_id)
        return (
            "This demo customer has already reviewed that product. "
            "Try a different product."
        )
    except Exception as e:
        return f"Error adding review: {e}"


# ===========================
# Run the app
# ===========================

if __name__ == "__main__":
    app.run_server(debug=True)
