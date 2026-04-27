"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import requests
from typing import List, Dict, Any


class State(rx.State):
    products: List[Dict[str, Any]] = []
    loading: bool = False
    ai_text: str = ""
    show_modal: bool = False

    selected_product: Dict[str, Any] = {}

    @rx.event
    def fetch_products(self):
        self.loading = True

        try:
            url = "https://fakestoreapi.com/products/category/electronics"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # ✅ SAFE REFRESH PATTERN (forces UI update)
                self.products = []
                self.products = list(data)

            else:
                self.products = []

        except Exception as e:
            print("Fetch error:", e)
            self.products = []

        self.loading = False

    @rx.event
    def set_product(self, product: Dict):
        self.selected_product = product

    @rx.event
    def explain_product(self):
        p = self.selected_product
        self.ai_text = (
            f"{p.get('title')} costs ${p.get('price')}.\n\n"
            f"{p.get('description')}"
        )
        self.show_modal = True

    @rx.event
    def close_modal(self):
        self.show_modal = False


# 🎨 Product Card
def product_card(product):
    return rx.box(
        rx.vstack(
            rx.image(
                src=product.get("image", ""),
                height="140px",
                object_fit="contain",
            ),

            rx.text(
                product.get("title", ""),
                font_weight="bold",
                font_size="0.9rem",
                no_of_lines=2,
                text_align="center",
            ),

            rx.text(
                f"${product.get('price', '')}",
                color="limegreen",
                font_weight="bold",
                font_size="1.1rem",
            ),

            rx.button(
                "Explain",
                width="100%",
                color_scheme="purple",
                on_click=[
                    State.set_product(product),
                    State.explain_product
                ],
            ),

            spacing="3",
            align="center",
            width="100%",
        ),

        padding="15px",
        border_radius="16px",
        bg=rx.cond(rx.color_mode == "dark", "#1e1e1e", "white"),
        box_shadow="lg",

        _hover={
            "transform": "scale(1.05)",
            "transition": "0.2s",
        },
    )


# 🌐 Main UI
def index() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.color_mode.button(position="top-right"),

            rx.heading(
                "Electronics Dashboard ⚡",
                size="8",
                color=rx.cond(rx.color_mode == "dark", "white", "black"),
            ),

            rx.text(
                "Browse electronics with AI-powered insights",
                color="gray",
            ),

            rx.button(
                rx.cond(State.loading, "Loading...", "Load Products"),
                on_click=State.fetch_products,
                is_loading=State.loading,
                color_scheme="blue",
                size="3",
            ),

            # ✅ FIXED CONDITION (IMPORTANT)
            rx.cond(
                State.loading,
                rx.text("Loading products...", color="gray"),

                rx.cond(
                    State.products.length() == 0,
                    rx.text("Click the button to load products 👆", color="gray"),

                    rx.grid(
                        rx.foreach(State.products, product_card),
                        columns="3",
                        spacing="6",
                        width="100%",
                    ),
                ),
            ),

            rx.dialog.root(
                rx.dialog.content(
                    rx.vstack(
                        rx.heading("Product Insight 🤖"),
                        rx.text(State.ai_text),
                        rx.button("Close", on_click=State.close_modal),
                        spacing="4",
                    )
                ),
                open=State.show_modal,
            ),

            spacing="6",
            align="center",
            width="100%",
        ),

        bg=rx.cond(
            rx.color_mode == "dark",
            "linear-gradient(135deg, #0f172a, #1e293b)",
            "#f5f5f5",
        ),

        min_height="100vh",
        padding="30px",
    )


app = rx.App()
app.add_page(index)