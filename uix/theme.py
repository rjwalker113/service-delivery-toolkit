# theme.py
from kivy.metrics import sp, dp
from kivy.properties import ColorProperty, NumericProperty, StringProperty, ObjectProperty
from kivy.event import EventDispatcher


class ColorNamespace(EventDispatcher):
    # --- Raw Values (Your Existing Palette) ---
    white = ColorProperty((1, 1, 1, 1))
    black = ColorProperty((0, 0, 0, 1))
    grey = ColorProperty((0.5, 0.5, 0.5, 1))
    lightgrey = ColorProperty((0.75, 0.75, 0.75, 1))
    darkgrey = ColorProperty((0.25, 0.25, 0.25, 1))

    primary = ColorProperty((0.015, 0.35, 0.6, 1))
    accent = ColorProperty((0.2, 0.5, 0.9, 1))
    light_shade = ColorProperty((0.85, 0.85, 0.85, 0.5))
    dark_shade = ColorProperty((0.55, 0.55, 0.55, 0.5))

    text = ColorProperty((0.1, 0.1, 0.1, 1))
    text_light = ColorProperty((1, 1, 1, 1))

    # --- Semantic Roles (Mapped to Raw Values) ---
    text_primary = ColorProperty()
    text_secondary = ColorProperty()
    text_inverse = ColorProperty()

    surface = ColorProperty()
    surface_alt = ColorProperty()
    surface_branding = ColorProperty()
    surface_modal = ColorProperty()

    border_subtle = ColorProperty()
    border_strong = ColorProperty()

    accent_primary = ColorProperty()
    accent_hover = ColorProperty()
    accent_muted = ColorProperty()

    error = ColorProperty((1, 0.2, 0.2, 1))
    success = ColorProperty((0.2, 1, 0.2, 1))
    warning = ColorProperty((1, 0.8, 0, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Map semantic roles to raw values
        self.text_primary = self.text
        self.text_secondary = self.grey
        self.text_inverse = self.white

        self.surface = self.white
        self.surface_alt = self.light_shade
        self.surface_branding = self.dark_shade
        self.surface_modal = self.white

        self.border_subtle = self.lightgrey
        self.border_strong = self.darkgrey

        self.accent_primary = self.primary
        self.accent_hover = self.accent
        self.accent_muted = self.light_shade


class FontNamespace(EventDispatcher):
    # Raw font families
    sans = StringProperty("fonts/NotoSans-Regular")
    sans_bold = StringProperty("fonts/NotoSans-SemiBold")
    condensed = StringProperty("fonts/NotoSans_Condensed-Regular")
    condensed_bold = StringProperty("fonts/NotoSans_Condensed-SemiBold")
    mono = StringProperty("fonts/JetBrainsMono-Regular")

    # Raw sizes
    xs = NumericProperty(sp(12))
    sm = NumericProperty(sp(14))
    md = NumericProperty(sp(16))
    lg = NumericProperty(sp(20))
    xl = NumericProperty(sp(24))

    # Semantic roles
    title = ObjectProperty()
    subtitle = ObjectProperty()
    body = ObjectProperty()
    caption = ObjectProperty()
    code = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = {"family": self.condensed_bold, "size": self.xl}
        self.subtitle = {"family": self.condensed, "size": self.lg}
        self.body = {"family": self.sans, "size": self.md}
        self.caption = {"family": self.sans, "size": self.sm}
        self.code = {"family": self.mono, "size": self.sm}


class SizeNamespace(EventDispatcher):
    # Raw values
    padding = NumericProperty(dp(20))
    spacing = NumericProperty(dp(10))
    radius = NumericProperty(dp(22))

    # Semantic roles
    padding_sm = NumericProperty()
    padding_md = NumericProperty()
    padding_lg = NumericProperty()

    spacing_sm = NumericProperty()
    spacing_md = NumericProperty()
    spacing_lg = NumericProperty()

    radius_sm = NumericProperty()
    radius_md = NumericProperty()
    radius_lg = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.padding_sm = dp(8)
        self.padding_md = dp(16)
        self.padding_lg = dp(24)

        self.spacing_sm = dp(6)
        self.spacing_md = dp(12)
        self.spacing_lg = dp(20)

        self.radius_sm = dp(4)
        self.radius_md = dp(8)
        self.radius_lg = dp(12)


class Theme(EventDispatcher):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = ColorNamespace()
        self.font = FontNamespace()
        self.size = SizeNamespace()


theme = Theme()

color = theme.color
font = theme.font
size = theme.size
