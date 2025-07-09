from manim import *

class DataTypesHierarchy(Scene):
    def construct(self):
        # Title
        title = Text("DATA TYPES", color=WHITE, font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Main branches
        primitive = Text("Primitive", font_size=36).shift(LEFT * 3 + UP * 1)
        non_primitive = Text("Non-Primitive", font_size=36).shift(RIGHT * 3 + UP * 1)
        self.play(FadeIn(primitive), FadeIn(non_primitive))

        # Lines from title to categories
        line1 = Line(title.get_bottom(), primitive.get_top(), color=BLUE)
        line2 = Line(title.get_bottom(), non_primitive.get_top(), color=BLUE)
        self.play(Create(line1), Create(line2))
        self.wait(0.3)

        # Primitive Branch
        non_numeric = Text("Non-Numeric", font_size=30).next_to(primitive, DOWN, buff=1).shift(LEFT * 1.2)
        numeric = Text("Numeric", font_size=30).next_to(primitive, DOWN, buff=1).shift(RIGHT * 1.2)

        self.play(FadeIn(non_numeric), FadeIn(numeric))
        self.play(Create(Line(primitive.get_bottom(), non_numeric.get_top(), color=BLUE)))
        self.play(Create(Line(primitive.get_bottom(), numeric.get_top(), color=BLUE)))

        # Non-Numeric children
        boolean = Text("boolean", font_size=24).next_to(non_numeric, DOWN)
        char = Text("char", font_size=24).next_to(boolean, DOWN)
        self.play(FadeIn(boolean), FadeIn(char))
        self.play(Create(Line(non_numeric.get_bottom(), boolean.get_top(), color=BLUE)))
        self.play(Create(Line(boolean.get_bottom(), char.get_top(), color=BLUE)))

        # Numeric children
        integer = Text("Integer", font_size=28).next_to(numeric, DOWN).shift(LEFT * 1)
        floating = Text("Floating-point", font_size=28).next_to(numeric, DOWN).shift(RIGHT * 1)
        self.play(FadeIn(integer), FadeIn(floating))
        self.play(Create(Line(numeric.get_bottom(), integer.get_top(), color=BLUE)))
        self.play(Create(Line(numeric.get_bottom(), floating.get_top(), color=BLUE)))

        # Integer types
        int_types = ["byte", "short", "int", "long"]
        int_group = VGroup(*[Text(t, font_size=22) for t in int_types]).arrange(DOWN, buff=0.3).next_to(integer, DOWN)
        self.play(*[FadeIn(txt) for txt in int_group])
        self.play(Create(Line(integer.get_bottom(), int_group[0].get_top(), color=BLUE)))

        for i in range(len(int_group) - 1):
            self.play(Create(Line(int_group[i].get_bottom(), int_group[i+1].get_top(), color=BLUE)))

        # Floating-point types
        float_types = ["float", "double"]
        float_group = VGroup(*[Text(t, font_size=22) for t in float_types]).arrange(DOWN, buff=0.3).next_to(floating, DOWN)
        self.play(*[FadeIn(txt) for txt in float_group])
        self.play(Create(Line(floating.get_bottom(), float_group[0].get_top(), color=BLUE)))
        self.play(Create(Line(float_group[0].get_bottom(), float_group[1].get_top(), color=BLUE)))

        # Non-Primitive Branch
        np_types = ["String", "Array", "Classes", "Objects", "Interfaces"]
        np_group = VGroup(*[Text(t, font_size=24) for t in np_types]).arrange(DOWN, buff=0.3).next_to(non_primitive, DOWN)
        self.play(*[FadeIn(txt) for txt in np_group])
        self.play(Create(Line(non_primitive.get_bottom(), np_group[0].get_top(), color=BLUE)))
        for i in range(len(np_group) - 1):
            self.play(Create(Line(np_group[i].get_bottom(), np_group[i+1].get_top(), color=BLUE)))

        # Footer
        footer = Text("©visualcoders", font_size=20, color=GRAY).to_edge(DOWN)
        self.play(FadeIn(footer))
        self.wait(2)
