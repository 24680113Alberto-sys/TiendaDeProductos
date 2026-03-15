

import flet as ft

products = [
    {
        "id": 1,
        "nombre": "MacBook Pro M4",
        "descripcion": "Laptop de alto rendimiento con chip Apple M4, 16 GB RAM y 512 GB SSD.",
        "precio": 19999.99,
        "categoria": "Laptops",
        "ruta_imagen": "images.jpeg",
    },
    {
        "id": 2,
        "nombre": "Samsung Galaxy S25",
        "descripcion": "Smartphone 6.2\" AMOLED 120 Hz, 8 GB RAM y cámara de 50 MP con IA.",
        "precio": 20899.99,
        "categoria": "Smartphones",
        "ruta_imagen": "galaxy.jpeg",
    },
    {
        "id": 3,
        "nombre": "Sony WH-1000XM5",
        "descripcion": "Audífonos inalámbricos con cancelación activa de ruido y 30 h de batería.",
        "precio": 1349.99,
        "categoria": "Audio",
        "ruta_imagen": "sony.jpeg",
    },
    {
        "id": 4,
        "nombre": "iPad Air M4",
        "descripcion": "Tablet 11\" con chip M4, compatible con Apple Pencil y Magic Keyboard.",
        "precio": 6749.99,
        "categoria": "Tablets",
        "ruta_imagen": "ipad.jpeg",
    },
    {
        "id": 5,
        "nombre": "LG UltraWide 34\"",
        "descripcion": "Monitor curvo 34\" UWQHD a 144 Hz con AMD FreeSync Premium.",
        "precio": 4599.99,
        "categoria": "Monitores",
        "ruta_imagen": "monitor.jpeg",
    },
]

CATEGORY_ICONS = {
    "Laptops":     ft.Icons.LAPTOP_ROUNDED,
    "Smartphones": ft.Icons.SMARTPHONE_ROUNDED,
    "Audio":       ft.Icons.HEADPHONES_ROUNDED,
    "Tablets":     ft.Icons.TABLET_ROUNDED,
    "Monitores":   ft.Icons.MONITOR_ROUNDED,
}

CATEGORY_COLORS = {
    "Laptops":     "#1565C0",
    "Smartphones": "#6A1B9A",
    "Audio":       "#00838F",
    "Tablets":     "#E65100",
    "Monitores":   "#2E7D32",
}


# ================================================================
# B. TARJETA DE PRODUCTO
# ================================================================
class ProductCard(ft.Container):

    def __init__(self, product: dict, on_add_to_cart=None):
        super().__init__()
        self.product = product
        self.on_add_to_cart = on_add_to_cart
        self._favorito = False

        self.width = 275
        self.border_radius = ft.BorderRadius.all(20)
        self.bgcolor = ft.Colors.WHITE
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE
        self.padding = 0
        self.shadow = self._shadow_normal()
        self.animate = ft.Animation(180, ft.AnimationCurve.EASE_IN_OUT)
        self.animate_scale = ft.Animation(180, ft.AnimationCurve.EASE_IN_OUT)

        self.content = self._build()

    # -- sombras --------------------------------------------------
    def _shadow_normal(self):
        return ft.BoxShadow(
            spread_radius=0,
            blur_radius=16,
            color=ft.Colors.with_opacity(0.14, ft.Colors.BLACK),
            offset=ft.Offset(0, 6),
        )

    def _shadow_hover(self):
        return ft.BoxShadow(
            spread_radius=2,
            blur_radius=30,
            color=ft.Colors.with_opacity(0.28, ft.Colors.BLUE_900),
            offset=ft.Offset(0, 12),
        )

    # -- hover ----------------------------------------------------
    def _on_hover(self, e):
        hovered = str(e.data).lower() == "true"
        self.shadow = self._shadow_hover() if hovered else self._shadow_normal()
        self.scale  = ft.Scale(scale=1.03 if hovered else 1.0)
        self.update()

    # -- favorito -------------------------------------------------
    def _toggle_fav(self, e, btn: ft.IconButton):
        self._favorito = not self._favorito
        btn.icon = (
            ft.Icons.FAVORITE_ROUNDED
            if self._favorito else ft.Icons.FAVORITE_BORDER_ROUNDED
        )
        btn.icon_color = ft.Colors.RED_500 if self._favorito else ft.Colors.RED_300
        btn.update()

    # -- construcción ---------------------------------------------
    def _build(self) -> ft.Column:
        self.on_hover = self._on_hover

        cat       = self.product.get("categoria", "")
        cat_color = CATEGORY_COLORS.get(cat, "#1565C0")
        cat_icon  = CATEGORY_ICONS.get(cat, ft.Icons.DEVICES_ROUNDED)

        # Badge de categoría
        badge = ft.Container(
            content=ft.Row(
                spacing=4,
                controls=[
                    ft.Icon(cat_icon, size=11, color=ft.Colors.WHITE),
                    ft.Text(cat, size=10, color=ft.Colors.WHITE,
                            weight=ft.FontWeight.W_600),
                ],
            ),
            bgcolor=cat_color,
            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
            border_radius=ft.BorderRadius.only(bottom_right=10),
        )

        # Área de imagen con badge superpuesto
        image_area = ft.Container(
            height=170,
            content=ft.Stack(
                width=275,
                height=170,
                controls=[
                    ft.Container(
                        width=275,
                        height=170,
                        bgcolor=ft.Colors.GREY_100,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Image(
                            src=self.product["ruta_imagen"],
                            width=275,
                            height=170,
                            fit=ft.BoxFit.CONTAIN,
                            error_content=ft.Container(
                                alignment=ft.Alignment(0, 0),
                                content=ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=6,
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.IMAGE_NOT_SUPPORTED_OUTLINED,
                                            size=40,
                                            color=ft.Colors.GREY_400,
                                        ),
                                        ft.Text("Sin imagen", size=11,
                                                color=ft.Colors.GREY_400),
                                    ],
                                ),
                            ),
                        ),
                    ),
                    ft.Container(
                        content=badge,
                        alignment=ft.Alignment(-1, -1),
                    ),
                ],
            ),
        )

        # Cuerpo de texto
        text_body = ft.Container(
            padding=ft.Padding.symmetric(horizontal=16, vertical=14),
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Text(
                        self.product["nombre"],
                        weight=ft.FontWeight.BOLD,
                        size=15,
                        color=ft.Colors.GREY_900,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(
                        self.product["descripcion"],
                        size=11,
                        color=ft.Colors.GREY_600,
                        max_lines=3,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Container(height=4),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                f"$ {self.product['precio']:,.2f} MXN",
                                size=17,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_700,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "Disponible",
                                    size=9,
                                    color=ft.Colors.GREEN_800,
                                    weight=ft.FontWeight.W_600,
                                ),
                                bgcolor=ft.Colors.GREEN_50,
                                padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                                border_radius=10,
                                border=ft.border.all(1, ft.Colors.GREEN_200),
                            ),
                        ],
                    ),
                ],
            ),
        )

        # Botón favorito
        fav_btn = ft.IconButton(
            icon=ft.Icons.FAVORITE_BORDER_ROUNDED,
            icon_color=ft.Colors.RED_300,
            icon_size=22,
            tooltip="Agregar a favoritos",
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.HOVERED: ft.Colors.RED_50},
                shape=ft.CircleBorder(),
            ),
        )
        fav_btn.on_click = lambda e: self._toggle_fav(e, fav_btn)

        # Botón "Al carrito"
        # FIX: ElevatedButton(text=) → ft.Button(content=ft.Row([icon, text]))
        cart_btn = ft.Button(
            content=ft.Row(
                spacing=6,
                tight=True,
                controls=[
                    ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED,
                            color=ft.Colors.WHITE, size=16),
                    ft.Text("Al carrito", color=ft.Colors.WHITE,
                            size=13, weight=ft.FontWeight.W_500),
                ],
            ),
            bgcolor=ft.Colors.BLUE_700,
            elevation=2,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.BLUE_800,
                    ft.ControlState.DEFAULT: ft.Colors.BLUE_700,
                },
                padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            ),
            on_click=lambda e, p=self.product: (
                self.on_add_to_cart(p)
                if self.on_add_to_cart
                else print(f"[Carrito] {p['nombre']} | ${p['precio']:,.2f}")
            ),
        )

        action_bar = ft.Container(
            padding=ft.Padding.only(left=12, right=12, bottom=12, top=6),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[fav_btn, cart_btn],
            ),
        )

        return ft.Column(
            spacing=0,
            controls=[
                image_area,
                ft.Divider(height=1, color=ft.Colors.GREY_200),
                text_body,
                ft.Divider(height=1, color=ft.Colors.GREY_200),
                action_bar,
            ],
        )


# ================================================================
# C. PÁGINA PRINCIPAL
# ================================================================
def main(page: ft.Page):
    page.title   = "TechStore — Catálogo de Productos"
    page.bgcolor = "#EEF2F7"
    page.padding = 0
    page.scroll  = ft.ScrollMode.AUTO
    page.fonts   = {
        "Poppins": "https://fonts.gstatic.com/s/poppins/v21/pxiByp8kv8JHgFVrLCz7Z1xlEA.ttf"
    }
    page.theme = ft.Theme(font_family="Poppins")

    # -- Estado del carrito ---------------------------------------
    cart: list[dict] = []

    cart_count = ft.Text("0", size=10, color=ft.Colors.WHITE,
                         weight=ft.FontWeight.BOLD)
    cart_badge = ft.Container(
        content=cart_count,
        bgcolor=ft.Colors.RED_500,
        width=18, height=18,
        border_radius=9,
        alignment=ft.Alignment(0, 0),
        visible=False,
    )

    def add_to_cart(product: dict):
        cart.append(product)
        cart_badge.visible = True
        cart_count.value   = str(len(cart))

        # FIX: page.snack_bar no existe → page.overlay.append()
        snack = ft.SnackBar(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE,
                            color=ft.Colors.WHITE, size=20),
                    ft.Text(
                        f"  {product['nombre']} agregado al carrito",
                        color=ft.Colors.WHITE, size=13,
                    ),
                ]
            ),
            bgcolor=ft.Colors.BLUE_800,
            duration=2000,
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    # -- Header ---------------------------------------------------
    header = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=["#1565C0", "#1A237E"],
        ),
        padding=ft.Padding.symmetric(horizontal=36, vertical=20),
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=14,
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.DEVICES_ROUNDED,
                                            color=ft.Colors.WHITE, size=28),
                            bgcolor=ft.Colors.with_opacity(0.22, ft.Colors.WHITE),
                            padding=10,
                            border_radius=12,
                        ),
                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text("Tecnologyc store JACG", size=26,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE),
                                
                            ],
                        ),
                    ],
                ),
                # Carrito con badge
                ft.Stack(
                    width=50, height=50,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.SHOPPING_CART_OUTLINED,
                            icon_color=ft.Colors.WHITE,
                            icon_size=28,
                            tooltip="Ver carrito",
                        ),
                        ft.Container(
                            content=cart_badge,
                            alignment=ft.Alignment(1, -1),
                            padding=ft.Padding.only(left=18),
                        ),
                    ],
                ),
            ],
        ),
    )

    # -- Chips de estadísticas ------------------------------------
    def stat_chip(icon, label, value):
        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            border_radius=14,
            shadow=ft.BoxShadow(
                blur_radius=8,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, size=16, color=ft.Colors.BLUE_700),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=7,
                        border_radius=8,
                    ),
                    ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text(value, size=13, weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREY_800),
                            ft.Text(label, size=10, color=ft.Colors.GREY_500),
                        ],
                    ),
                ],
            ),
        )

    stats_bar = ft.Container(
        padding=ft.Padding.symmetric(horizontal=36, vertical=16),
        content=ft.Row(
            wrap=True, spacing=14, run_spacing=10,
            controls=[
                stat_chip(ft.Icons.INVENTORY_2_OUTLINED,  "Productos",     str(len(products))),
                stat_chip(ft.Icons.LOCAL_SHIPPING_OUTLINED,"Envío gratis",  "+$999 MXN"),
                stat_chip(ft.Icons.VERIFIED_OUTLINED,      "Garantía",      "12 meses"),
                stat_chip(ft.Icons.PAYMENT_OUTLINED,       "Pagos seguros", "SSL 256-bit"),
            ],
        ),
    )

    # -- Título de sección ----------------------------------------
    section_title = ft.Container(
        padding=ft.Padding.only(left=36, top=4, bottom=12),
        content=ft.Row(
            spacing=12,
            controls=[
                ft.Container(width=4, height=24,
                             bgcolor=ft.Colors.BLUE_700, border_radius=2),
                ft.Column(
                    spacing=1,
                    controls=[
                        ft.Text("Artículos Destacados", size=19,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_800),
                        ft.Text(f"{len(products)} productos disponibles",
                                size=11, color=ft.Colors.GREY_500),
                    ],
                ),
            ],
        ),
    )

    # -- Grid de tarjetas -----------------------------------------
    cards_grid = ft.Container(
        padding=ft.Padding.symmetric(horizontal=30, vertical=10),
        content=ft.Row(
            wrap=True, spacing=22, run_spacing=22,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ProductCard(product=p, on_add_to_cart=add_to_cart)
                for p in products
            ],
        ),
    )

    # -- Footer ---------------------------------------------------
    # FIX: TextButton("texto") → TextButton(content=ft.Text("texto"))
    footer = ft.Container(
        padding=ft.Padding.symmetric(vertical=20, horizontal=36),
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
            controls=[
                ft.Divider(color=ft.Colors.GREY_300),
                
                ft.Text(
                    "Tecnologyc store JACG ",
                    size=11,
                    color=ft.Colors.GREY_400,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )

    page.add(header, stats_bar, section_title, cards_grid, footer)


# ================================================================
ft.app(target=main, assets_dir="assets")