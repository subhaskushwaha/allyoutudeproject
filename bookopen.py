from manim import *

class AutoBookPageTurn(Scene):
    def construct(self):
        # Book base
        left_page = Rectangle(width=3.5, height=5, color=WHITE, fill_opacity=1).shift(LEFT * 2)
        right_page = Rectangle(width=3.5, height=5, color=WHITE, fill_opacity=1).shift(RIGHT * 2)
        self.play(FadeIn(left_page), FadeIn(right_page))

        # Add some text to left page
        left_text = Text("This is Page 1", font_size=24).move_to(left_page.get_center())
        self.play(Write(left_text))

        # Simulate turning page
        flipping_page = Rectangle(width=3.5, height=5, color=BLUE, fill_opacity=0.7).shift(RIGHT * 2)
        self.play(FadeIn(flipping_page))

        # Page turn animation
        self.play(flipping_page.animate.shift(LEFT * 4), run_time=2)
        self.play(FadeOut(flipping_page))

        # New text on right page
        right_text = Text("Now Page 2", font_size=24).move_to(right_page.get_center())
        self.play(Write(right_text))

        self.wait(2)
