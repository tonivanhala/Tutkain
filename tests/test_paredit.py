from unittest import skip

from .util import ViewTestCase


class TestParedit(ViewTestCase):
    def test_forward_backward(self):
        self.set_view_content('(foo (bar) baz "qux" 1/2 ::quux/quuz)')
        self.set_selections((0, 0))
        self.view.run_command("tutkain_paredit_forward")
        self.assertEquals([(37, 37)], self.selections())
        self.view.run_command("tutkain_paredit_backward")
        self.assertEquals([(0, 0)], self.selections())
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_forward")
        self.assertEquals([(4, 4)], self.selections())
        self.view.run_command("tutkain_paredit_forward")
        self.assertEquals([(10, 10)], self.selections())
        self.view.run_command("tutkain_paredit_forward")
        self.assertEquals([(14, 14)], self.selections())
        self.view.run_command("tutkain_paredit_forward")
        self.assertEquals([(20, 20)], self.selections())
        self.view.run_command("tutkain_paredit_forward")
        self.assertEquals([(24, 24)], self.selections())
        self.view.run_command("tutkain_paredit_forward")
        self.assertEquals([(36, 36)], self.selections())
        self.view.run_command("tutkain_paredit_forward")
        self.assertEquals([(37, 37)], self.selections())

        # Going forward may not be the answer. Maybe I should go back.
        self.view.run_command("tutkain_paredit_backward")
        self.assertEquals([(0, 0)], self.selections())
        self.view.run_command("tutkain_paredit_forward")
        self.assertEquals([(37, 37)], self.selections())
        self.set_selections((36, 36))
        self.view.run_command("tutkain_paredit_backward")
        self.assertEquals([(25, 25)], self.selections())
        self.view.run_command("tutkain_paredit_backward")
        self.assertEquals([(21, 21)], self.selections())
        self.view.run_command("tutkain_paredit_backward")
        self.assertEquals([(15, 15)], self.selections())
        self.view.run_command("tutkain_paredit_backward")
        self.assertEquals([(11, 11)], self.selections())
        self.view.run_command("tutkain_paredit_backward")
        self.assertEquals([(5, 5)], self.selections())
        self.view.run_command("tutkain_paredit_backward")
        self.assertEquals([(1, 1)], self.selections())
        self.view.run_command("tutkain_paredit_backward")
        self.assertEquals([(0, 0)], self.selections())

    def test_open_round(self):
        self.set_view_content("(a b c d)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_open_round")
        self.assertEquals("(a b () c d)", self.view_content())
        self.assertEquals(self.selections(), [(6, 6)])

    def test_open_round_next_to_whitespace(self):
        self.set_view_content("(a b c d)")
        self.set_selections((9, 9))
        self.view.run_command("tutkain_paredit_open_round")
        self.assertEquals("(a b c d)()", self.view_content())
        self.assertEquals(self.selections(), [(10, 10)])

    def test_open_round_inside_string(self):
        self.set_view_content('(foo "bar baz" quux)')
        self.set_selections((10, 10))
        self.view.run_command("tutkain_paredit_open_round")
        self.assertEquals('(foo "bar (baz" quux)', self.view_content())
        self.assertEquals(self.selections(), [(11, 11)])

    def test_open_round_multiple_cursors(self):
        self.set_view_content("(a b c d) (e f g h)")
        self.set_selections((5, 5), (15, 15))
        self.view.run_command("tutkain_paredit_open_round")
        self.assertEquals("(a b () c d) (e f () g h)", self.view_content())
        self.assertEquals(self.selections(), [(6, 6), (19, 19)])

    def test_open_round_selection(self):
        self.set_view_content("(a b c)")
        self.set_selections((3, 4))
        self.view.run_command("tutkain_paredit_open_round")
        self.assertEquals("(a (b) c)", self.view_content())
        self.assertEquals(self.selections(), [(4, 4)])

    def test_open_round_before_close_round(self):
        self.set_view_content("(a )")
        self.set_selections((3, 3))
        self.view.run_command("tutkain_paredit_open_round")
        self.assertEquals("(a ())", self.view_content())
        self.assertEquals(self.selections(), [(4, 4)])

    def test_open_round_before_close_square(self):
        self.set_view_content("(a [b ])")
        self.set_selections((6, 6))
        self.view.run_command("tutkain_paredit_open_round")
        self.assertEquals("(a [b ()])", self.view_content())
        self.assertEquals(self.selections(), [(7, 7)])

    def test_close_round(self):
        self.set_view_content("(a )")
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_close_round")
        self.assertEquals("(a)", self.view_content())
        self.assertEquals(self.selections(), [(3, 3)])

        self.set_view_content('(a "b")')
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_close_round")
        self.assertEquals('(a "b")', self.view_content())
        self.assertEquals(self.selections(), [(7, 7)])

    def test_close_round_in_string(self):
        self.set_view_content('(a "b")')
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_close_round")
        self.assertEquals('(a "b)")', self.view_content())
        self.assertEquals(self.selections(), [(6, 6)])

    def test_close_round_multiple_cursors(self):
        self.set_view_content("(a ) (b )")
        self.set_selections((2, 2), (7, 7))
        self.view.run_command("tutkain_paredit_close_round")
        self.assertEquals("(a) (b)", self.view_content())
        self.assertEquals(self.selections(), [(3, 3), (7, 7)])

    def test_open_square(self):
        self.set_view_content("(a b c d)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_open_square")
        self.assertEquals("(a b [] c d)", self.view_content())
        self.assertEquals(self.selections(), [(6, 6)])

    def test_close_square(self):
        self.set_view_content("[a ]")
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_close_square")
        self.assertEquals("[a]", self.view_content())
        self.assertEquals(self.selections(), [(3, 3)])

    def test_open_curly(self):
        self.set_view_content("(a b c d)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_open_curly")
        self.assertEquals("(a b {} c d)", self.view_content())
        self.assertEquals(self.selections(), [(6, 6)])

    def test_close_curly(self):
        self.set_view_content("{a b }")
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_close_curly")
        self.assertEquals("{a b}", self.view_content())
        self.assertEquals(self.selections(), [(5, 5)])

    def test_double_quote_simple(self):
        self.set_selections((0, 0))
        self.view.run_command("tutkain_paredit_double_quote")
        self.assertEquals('""', self.view_content())
        self.assertEquals(self.selections(), [(1, 1)])

    def test_double_quote_selection(self):
        self.set_view_content("(foo)")
        self.set_selections((1, 4))
        self.view.run_command("tutkain_paredit_double_quote")
        self.assertEquals('("foo")', self.view_content())
        self.assertEquals(self.selections(), [(2, 5)])

    def test_double_quote_selection_across_sexps(self):
        self.set_view_content("(foo) (bar)")
        self.set_selections((4, 9))
        self.view.run_command("tutkain_paredit_double_quote")
        self.assertEquals('(foo"") (bar)', self.view_content())
        self.assertEquals(self.selections(), [(5, 5)])

    def test_double_quote_inside_string(self):
        self.set_view_content('" "')
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_double_quote")
        self.assertEquals('"\\" "', self.view_content())
        self.assertEquals(self.selections(), [(3, 3)])

    def test_double_quote_next_to_left_double_quote(self):
        self.set_view_content('""')
        self.set_selections((0, 0))
        self.view.run_command("tutkain_paredit_double_quote")
        self.assertEquals('""', self.view_content())
        self.assertEquals(self.selections(), [(1, 1)])

    def test_double_quote_next_to_right_double_quote(self):
        self.set_view_content('""')
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_double_quote")
        self.assertEquals('""', self.view_content())
        self.assertEquals(self.selections(), [(2, 2)])

    def test_double_quote_inside_comment(self):
        self.set_view_content("; ")
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_double_quote")
        self.assertEquals('; "', self.view_content())
        self.assertEquals(self.selections(), [(3, 3)])

    def test_double_quote_multiple_cursors(self):
        self.set_view_content(" ")
        self.set_selections((0, 0), (1, 1))
        self.view.run_command("tutkain_paredit_double_quote")
        self.assertEquals('"" ""', self.view_content())
        self.assertEquals(self.selections(), [(1, 1), (4, 4)])
        self.view.run_command(("tutkain_paredit_double_quote"))
        self.assertEquals(self.selections(), [(2, 2), (5, 5)])

    def test_forward_slurp_word(self):
        self.set_view_content("(a (b) c)")
        self.set_selections((3, 3))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(a (b) c)", self.view_content())
        self.set_view_content("(a (b) c)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(a (b c))", self.view_content())
        self.assertEquals(self.selections(), [(5, 5)])
        self.set_view_content("(a (b ) c)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(a (b c))", self.view_content())
        self.assertEquals(self.selections(), [(5, 5)])

    def test_forward_slurp_numbers(self):
        self.set_view_content("(a (b) 1/2)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(a (b 1/2))", self.view_content())
        self.set_view_content("(a (b) 0.2)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(a (b 0.2))", self.view_content())

    def test_forward_slurp_indent(self):
        self.set_view_content("(a (b    ) {:c    :d})")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(a (b {:c :d}))", self.view_content())
        self.assertEquals(self.selections(), [(5, 5)])

        self.set_view_content("(a (b))\n(c)")
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(a (b)\n  (c))", self.view_content())
        self.assertEquals(self.selections(), [(2, 2)])

    def test_forward_slurp_set(self):
        self.set_view_content("(a (b) #{1 2 3})")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(a (b #{1 2 3}))", self.view_content())
        self.assertEquals(self.selections(), [(5, 5)])

    def test_forward_slurp_string(self):
        self.set_view_content('"a" b')
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals('"a b"', self.view_content())
        self.assertEquals(self.selections(), [(2, 2)])

    def test_forward_slurp_quoted_symbol(self):
        self.set_view_content("""(foo (bar) 'baz)""")
        self.set_selections((9, 9))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("""(foo (bar 'baz))""", self.view_content())
        self.assertEquals(self.selections(), [(9, 9)])

    def test_forward_slurp_var_quoted_symbol(self):
        self.set_view_content("""(foo (bar) #'baz)""")
        self.set_selections((9, 9))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("""(foo (bar #'baz))""", self.view_content())
        self.assertEquals(self.selections(), [(9, 9)])

    def test_forward_slurp_nested(self):
        self.set_view_content("(([a]) b)")
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(([a] b))", self.view_content())
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(([a b]))", self.view_content())
        self.assertEquals(self.selections(), [(4, 4)])

    def test_forward_slurp_sexp_boundary(self):
        self.set_view_content("(a (b))")
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(a (b))", self.view_content())
        self.assertEquals([(2, 2)], self.selections())

    def test_forward_slurp_comment(self):
        self.set_view_content("(a (b)\n  ;; c\n  (d))")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(a (b\n     ;; c\n     (d)))", self.view_content())
        self.assertEquals([(5, 5)], self.selections())

    def test_forward_slurp_discard(self):
        self.set_view_content("(foo (bar) #_(baz))")
        self.set_selections((9, 9))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(foo (bar #_(baz)))", self.view_content())
        self.assertEquals([(9, 9)], self.selections())

    def test_forward_slurp_reader_conditional(self):
        self.set_view_content("(foo (bar) #?(:cljs baz))")
        self.set_selections((9, 9))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(foo (bar #?(:cljs baz)))", self.view_content())
        self.assertEquals([(9, 9)], self.selections())

    def test_forward_slurp_multiple_cursors(self):
        self.set_view_content("(a (b) c) (d (e) f)")
        self.set_selections((5, 5), (15, 15))
        self.view.run_command("tutkain_paredit_forward_slurp")
        self.assertEquals("(a (b c)) (d (e f))", self.view_content())
        self.assertEquals(self.selections(), [(5, 5), (15, 15)])

    def test_backward_slurp_word(self):
        self.set_view_content("(a #{b} c)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("(#{a b} c)", self.view_content())
        self.assertEquals(self.selections(), [(5, 5)])
        self.set_view_content("(a ( b) c)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("((a b) c)", self.view_content())
        self.assertEquals(self.selections(), [(5, 5)])

    def test_backward_slurp_comment(self):
        self.set_view_content("(a\n  (b)\n  ;; c\n  (d))")
        self.set_selections((19, 19))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("(a\n  ((b)\n   ;; c\n   d))", self.view_content())
        self.assertEquals(self.selections(), [(19, 19)])

    def test_backward_slurp_discard(self):
        self.set_view_content("(foo #_(bar) (baz))")
        self.set_selections((14, 14))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("(foo (#_(bar) baz))", self.view_content())
        self.assertEquals([(14, 14)], self.selections())

    def test_backward_slurp_reader_conditional(self):
        self.set_view_content("(foo #?(:cljs bar) (baz))")
        self.set_selections((20, 20))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("(foo (#?(:cljs bar) baz))", self.view_content())
        self.assertEquals([(20, 20)], self.selections())

    def test_backward_slurp_numbers(self):
        self.set_view_content("(1/2 (b))")
        self.set_selections((6, 6))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("((1/2 b))", self.view_content())
        self.set_view_content("(0.2 (b))")
        self.set_selections((6, 6))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("((0.2 b))", self.view_content())

    @skip("")
    def test_backward_slurp_indent(self):
        self.set_view_content("({:c    :d} (b    ))")
        self.set_selections((14, 14))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("(({:c :d} b))", self.view_content())
        self.assertEquals(self.selections(), [(11, 11)])

    def test_backward_slurp_string(self):
        self.set_view_content('b "a"')
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals('"b a"', self.view_content())
        self.assertEquals(self.selections(), [(4, 4)])

    def test_backward_slurp_quoted_symbol(self):
        self.set_view_content("""(foo (bar) 'baz (quux))""")
        self.set_selections((17, 17))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("""(foo (bar) ('baz quux))""", self.view_content())
        self.assertEquals(self.selections(), [(17, 17)])

    def test_backward_slurp_var_quoted_symbol(self):
        self.set_view_content("""(foo (bar) #'baz (quux))""")
        self.set_selections((18, 18))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("""(foo (bar) (#'baz quux))""", self.view_content())
        self.assertEquals(self.selections(), [(18, 18)])

    def test_backward_slurp_nested(self):
        self.set_view_content("(b ([a]))")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("((b [a]))", self.view_content())
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("(([b a]))", self.view_content())
        self.assertEquals(self.selections(), [(5, 5)])

    def test_backward_slurp_sexp_boundary(self):
        self.set_view_content("((b) a)")
        self.set_selections((6, 6))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("((b) a)", self.view_content())
        self.assertEquals([(6, 6)], self.selections())

    def test_backward_slurp_multiple_cursors(self):
        self.set_view_content("(a (b) c) (d (e) f)")
        self.set_selections((4, 4), (14, 14))
        self.view.run_command("tutkain_paredit_backward_slurp")
        self.assertEquals("((a b) c) ((d e) f)", self.view_content())
        self.assertEquals(self.selections(), [(4, 4), (14, 14)])

    def test_forward_barf_word(self):
        self.set_view_content("(a (b c))")
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_forward_barf")
        self.assertEquals("(a (b) c)", self.view_content())
        self.assertEquals(self.selections(), [(4, 4)])
        self.view.run_command("tutkain_paredit_forward_barf")
        self.assertEquals("(a () b c)", self.view_content())
        self.assertEquals(self.selections(), [(4, 4)])
        self.view.run_command("tutkain_paredit_forward_barf")
        self.assertEquals("(a () b) c", self.view_content())
        self.assertEquals(self.selections(), [(4, 4)])

    def test_forward_barf_empty(self):
        self.set_view_content("(a () c)")
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_forward_barf")
        self.assertEquals("(a ()) c", self.view_content())
        self.assertEquals(self.selections(), [(4, 4)])

    def test_forward_barf_set(self):
        self.set_view_content("(a (b #{1 2 3}))")
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_forward_barf")
        self.assertEquals("(a (b) #{1 2 3})", self.view_content())
        self.assertEquals(self.selections(), [(4, 4)])

    def test_forward_barf_string(self):
        self.set_view_content('"a b"')
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_forward_barf")
        self.assertEquals('"a" b', self.view_content())
        self.assertEquals(self.selections(), [(1, 1)])
        self.view.run_command("tutkain_paredit_forward_barf")
        self.assertEquals('"" a b', self.view_content())
        self.assertEquals(self.selections(), [(1, 1)])

    def test_forward_barf_multiple_cursors(self):
        self.set_view_content("(a (b c)) (d (e f))")
        self.set_selections((4, 4), (14, 14))
        self.view.run_command("tutkain_paredit_forward_barf")
        self.assertEquals("(a (b) c) (d (e) f)", self.view_content())
        self.assertEquals(self.selections(), [(4, 4), (14, 14)])

    # TODO: I'm not asserting selections here because I haven't figured out how to ensure the
    # "correct" cursor position after running Paredit commands. It's especially tricky when
    # whitespace pruning is involved.
    def test_backward_barf_word(self):
        self.set_view_content("((a b) c)")
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_backward_barf")
        self.assertEquals("(a (b) c)", self.view_content())
        self.view.run_command("tutkain_paredit_backward_barf")
        self.assertEquals("(a b () c)", self.view_content())
        self.set_selections((6, 6))
        self.view.run_command("tutkain_paredit_backward_barf")
        self.assertEquals("a (b () c)", self.view_content())

    def test_backward_barf_empty(self):
        self.set_view_content("(a () c)")
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_backward_barf")
        self.assertEquals("a (() c)", self.view_content())

    def test_backward_barf_set(self):
        self.set_view_content("((#{1 2 3} b) c)")
        self.set_selections((10, 10))
        self.view.run_command("tutkain_paredit_backward_barf")
        self.assertEquals("(#{1 2 3} (b) c)", self.view_content())
        self.set_view_content("(a #{1 2 3} b)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_backward_barf")
        self.assertEquals("(a 1 #{2 3} b)", self.view_content())

    def test_backward_barf_string(self):
        self.set_view_content('"a b"')
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_backward_barf")
        self.assertEquals('a "b"', self.view_content())
        self.set_selections((3, 3))
        self.view.run_command("tutkain_paredit_backward_barf")
        self.assertEquals('a b ""', self.view_content())

    def test_backward_barf_multiple_cursors(self):
        self.set_view_content("((a b) c) ((d e) f)")
        self.set_selections((2, 2), (12, 12))
        self.view.run_command("tutkain_paredit_backward_barf")
        self.assertEquals("(a (b) c) (d (e) f)", self.view_content())

    def test_wrap_round(self):
        self.set_view_content("(foo bar baz)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("(foo (bar) baz)", self.view_content())
        self.assertEquals([(6, 6)], self.selections())

        self.set_view_content("(foo [bar] baz)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("(foo ([bar]) baz)", self.view_content())

        self.set_view_content("(foo [bar] baz)")
        self.set_selections((10, 10))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("(foo ([bar]) baz)", self.view_content())

        self.set_view_content("")
        self.set_selections((0, 0))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("()", self.view_content())
        self.assertEquals([(1, 1)], self.selections())

        self.set_view_content("  ")
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals(" () ", self.view_content())
        self.assertEquals([(2, 2)], self.selections())

        self.set_view_content("(foo bar baz) (qux quux quuz)")
        self.set_selections((5, 5), (19, 19))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("(foo (bar) baz) (qux (quux) quuz)", self.view_content())
        self.assertEquals([(6, 6), (22, 22)], self.selections())

        self.set_view_content("(foo  bar)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("(foo () bar)", self.view_content())
        self.assertEquals([(6, 6)], self.selections())

        self.set_view_content(":foo/bar")
        self.set_selections((0, 0))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("(:foo/bar)", self.view_content())
        self.assertEquals([(1, 1)], self.selections())

        self.set_view_content(":foo/bar")
        self.set_selections((8, 8))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("(:foo/bar)", self.view_content())
        self.assertEquals([(10, 10)], self.selections())

        self.set_view_content("(+ 1/2 2/2)")
        self.set_selections((3, 3))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("(+ (1/2) 2/2)", self.view_content())
        self.assertEquals([(4, 4)], self.selections())

        self.set_view_content("(+ 1/2 2/2)")
        self.set_selections((6, 6))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("(+ (1/2) 2/2)", self.view_content())
        self.assertEquals([(8, 8)], self.selections())

        self.set_view_content("#(foo bar)")
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("#((foo bar))", self.view_content())
        self.assertEquals([(2, 2)], self.selections())

        self.set_view_content("""(foo '[bar :baz quux])""")
        self.set_selections((16, 16))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("""(foo '[bar :baz (quux)])""", self.view_content())
        self.assertEquals([(17, 17)], self.selections())

        self.set_view_content("""a b""")
        self.set_selections((0, 3))
        self.view.run_command("tutkain_paredit_wrap_round")
        self.assertEquals("""(a b)""", self.view_content())
        self.assertEquals([(1, 4)], self.selections())

    def test_wrap_square(self):
        self.set_view_content("(foo bar baz)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_wrap_square")
        self.assertEquals("(foo [bar] baz)", self.view_content())
        self.assertEquals([(6, 6)], self.selections())

    def test_backward_delete(self):
        self.set_view_content('("zot" quux)')
        self.set_selections((8, 8))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals('("zot" uux)', self.view_content())
        self.assertEquals([(7, 7)], self.selections())

        self.set_view_content('("zot" quux)')
        self.set_selections((6, 6))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals('("zot" quux)', self.view_content())
        self.assertEquals([(5, 5)], self.selections())
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals('("zo" quux)', self.view_content())
        self.assertEquals([(4, 4)], self.selections())

        self.set_view_content("(foo bar) (baz quux)")
        self.set_selections((9, 9), (21, 21))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals("(foo bar) (baz quux)", self.view_content())
        self.assertEquals([(8, 8), (19, 19)], self.selections())
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals("(foo ba) (baz quu)", self.view_content())
        self.assertEquals([(7, 7), (17, 17)], self.selections())

        self.set_view_content('("")')
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals("()", self.view_content())
        self.assertEquals([(1, 1)], self.selections())
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals("", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

        self.set_view_content("()")
        self.set_selections((0, 0))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals("()", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

        self.set_view_content("()")
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals("()", self.view_content())
        self.assertEquals([(1, 1)], self.selections())
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals("", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

        self.set_view_content("(a)")
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals("(a)", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

        self.set_view_content("(a)")
        self.set_selections((0, 3))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals("", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

        self.set_view_content("(a)(b)")
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals("(a)(b)", self.view_content())
        self.assertEquals([(3, 3)], self.selections())

        self.set_view_content('("()")')
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals('("(")', self.view_content())
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals('("")', self.view_content())

        self.set_view_content("#{}")
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals("", self.view_content())

        self.set_view_content('"\\""')
        self.set_selections((3, 3))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals('""', self.view_content())

        self.set_view_content('"a"')
        self.set_selections((3, 3))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals('"a"', self.view_content())

        self.set_view_content(";; a b")
        self.set_selections((6, 6))
        self.view.run_command("tutkain_paredit_backward_delete")
        self.assertEquals(";; a ", self.view_content())

    def test_forward_delete(self):
        self.set_view_content('("zot" quux)')
        self.set_selections((7, 7))
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals('("zot" uux)', self.view_content())
        self.assertEquals([(7, 7)], self.selections())

        self.set_view_content('("zot" quux)')
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals('("zot" quux)', self.view_content())
        self.assertEquals([(6, 6)], self.selections())
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals('("zot"quux)', self.view_content())
        self.assertEquals([(6, 6)], self.selections())

        self.set_view_content("(foo bar) (baz quux)")
        self.set_selections((7, 7), (18, 18))
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals("(foo ba) (baz quu)", self.view_content())
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals("(foo ba) (baz quu)", self.view_content())
        self.assertEquals([(8, 8), (18, 18)], self.selections())

        self.set_view_content('("")')
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals("()", self.view_content())
        self.assertEquals([(1, 1)], self.selections())
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals("", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

        self.set_view_content("()")
        self.set_selections((0, 0))
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals("()", self.view_content())
        self.assertEquals([(1, 1)], self.selections())
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals("", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

        self.set_view_content("(a)")
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals("(a)", self.view_content())
        self.assertEquals([(3, 3)], self.selections())

        self.set_view_content("(a)")
        self.set_selections((0, 3))
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals("", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

        self.set_view_content('("()")')
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals('(")")', self.view_content())
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals('("")', self.view_content())

        self.set_view_content("#(a b)")
        self.set_selections((0, 0))
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals("(a b)", self.view_content())

        self.set_view_content("#{}")
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals("", self.view_content())

        self.set_view_content('"\\""')
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals('""', self.view_content())

        self.set_view_content("(defn foo [bar] (fn [baz quux]))")
        self.set_selections((30, 30))
        self.view.run_command("tutkain_paredit_forward_delete")
        self.assertEquals("(defn foo [bar] (fn [baz quux]))", self.view_content())
        self.assertEquals([(31, 31)], self.selections())

    def test_raise_sexp(self):
        self.set_view_content("(def f (fn [] body))")
        self.set_selections((14, 14))
        self.view.run_command("tutkain_paredit_raise_sexp")
        self.assertEquals("(def f body)", self.view_content())

        self.set_view_content('(a "b")')
        self.set_selections((3, 3))
        self.view.run_command("tutkain_paredit_raise_sexp")
        self.assertEquals('"b"', self.view_content())
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_raise_sexp")
        self.assertEquals('"b"', self.view_content())

        self.set_view_content("(a\n(b\n(c)))")
        self.set_selections((6, 6))
        self.view.run_command("tutkain_paredit_raise_sexp")
        self.assertEquals("(a\n  (c))", self.view_content())
        self.assertEquals([(5, 5)], self.selections())

        self.set_view_content("(and foo?)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_raise_sexp")
        self.assertEquals("foo?", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

        self.set_view_content('(foo #bar/baz "quux")')
        self.set_selections((5, 13))
        self.view.run_command("tutkain_paredit_raise_sexp")
        self.assertEquals("#bar/baz", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

    def test_splice_sexp(self):
        self.set_view_content("(a (b c) d) (e (f g) h)")
        self.set_selections((5, 5), (17, 17))
        self.view.run_command("tutkain_paredit_splice_sexp")
        self.assertEquals("(a b c d) (e f g h)", self.view_content())
        self.assertEquals([(4, 4), (14, 14)], self.selections())

        self.set_view_content("#{1 2 3}")
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_splice_sexp")
        self.assertEquals("1 2 3", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

        self.set_view_content('"a b"')
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_splice_sexp")
        self.assertEquals("a b", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

    def test_comment_dwim(self):
        self.set_view_content("(a b c)")
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_comment_dwim")
        self.assertEquals("(a b c) ; ", self.view_content())
        self.set_view_content("(a b\n c)")
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_comment_dwim")
        self.assertEquals("(a b ; \n c)", self.view_content())

    def test_semicolon(self):
        self.set_view_content("(a b)")
        self.set_selections((0, 0))
        self.view.run_command("tutkain_paredit_semicolon")
        self.assertEquals(" ;(a b)", self.view_content())
        self.assertEquals([(2, 2)], self.selections())

        self.set_view_content("(a b)")
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_semicolon")
        self.assertEquals("(;a b\n)", self.view_content())
        self.assertEquals([(2, 2)], self.selections())

        self.set_view_content("(a b)")
        self.set_selections((3, 3))
        self.view.run_command("tutkain_paredit_semicolon")
        self.assertEquals("(a ;b\n)", self.view_content())
        self.assertEquals([(4, 4)], self.selections())

        self.set_view_content("(a b)")
        self.set_selections((4, 4))
        self.view.run_command("tutkain_paredit_semicolon")
        self.assertEquals("(a b ;\n)", self.view_content())
        self.assertEquals([(6, 6)], self.selections())

        self.set_view_content("(a b)(c d)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_semicolon")
        self.assertEquals("(a b);(c d)", self.view_content())
        self.assertEquals([(6, 6)], self.selections())

        self.set_view_content("(a b)(c d)")
        self.set_selections((3, 3), (8, 8))
        self.view.run_command("tutkain_paredit_semicolon")
        self.assertEquals("(a ;b\n)(c ;d\n)", self.view_content())
        self.assertEquals([(4, 4), (11, 11)], self.selections())

    def test_splice_sexp_killing_forward(self):
        self.set_view_content("(a (b c d) e) (f g (h i j) k)")
        self.set_selections((6, 6), (24, 24))
        self.view.run_command("tutkain_paredit_splice_sexp_killing_forward")
        self.assertEquals("(a b e) (f g h i k)", self.view_content())
        self.assertEquals([(3, 3), (16, 16)], self.selections())

        self.set_view_content("()")
        self.set_selections((0, 0))
        self.view.run_command("tutkain_paredit_splice_sexp_killing_forward")
        self.assertEquals("()", self.view_content())
        self.set_view_content("()")
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_splice_sexp_killing_forward")
        self.assertEquals("", self.view_content())
        self.set_view_content("()")
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_splice_sexp_killing_forward")
        self.assertEquals("()", self.view_content())

    def test_splice_sexp_killing_backward(self):
        self.set_view_content("(a (b c d) e) (f g (h i j) k)")
        self.set_selections((8, 8), (22, 22))
        self.view.run_command("tutkain_paredit_splice_sexp_killing_backward")
        self.assertEquals("(a d e) (f g i j k)", self.view_content())
        self.assertEquals([(3, 3), (13, 13)], self.selections())

        self.set_view_content("()")
        self.set_selections((0, 0))
        self.view.run_command("tutkain_paredit_splice_sexp_killing_backward")
        self.assertEquals("()", self.view_content())
        self.set_view_content("()")
        self.set_selections((1, 1))
        self.view.run_command("tutkain_paredit_splice_sexp_killing_backward")
        self.assertEquals("", self.view_content())
        self.set_view_content("()")
        self.set_selections((2, 2))
        self.view.run_command("tutkain_paredit_splice_sexp_killing_backward")
        self.assertEquals("()", self.view_content())

    def test_backward_kill_form(self):
        self.set_view_content("(foo ::bar baz)")
        self.set_selections((8, 8))
        self.view.run_command("tutkain_paredit_backward_kill_form")
        self.assertEquals("(foo  baz)", self.view_content())
        self.assertEquals([(5, 5)], self.selections())
        self.set_view_content('"foo bar baz"')
        self.set_selections((8, 8))
        self.view.run_command("tutkain_paredit_backward_kill_form")
        self.assertEquals('"foo  baz"', self.view_content())
        self.assertEquals([(5, 5)], self.selections())
        self.set_view_content("; foo bar baz")
        self.set_selections((9, 9))
        self.view.run_command("tutkain_paredit_backward_kill_form")
        self.assertEquals("; foo  baz", self.view_content())
        self.assertEquals([(6, 6)], self.selections())
        self.set_view_content("(foo ::bar baz)")
        self.set_selections((15, 0))
        self.view.run_command("tutkain_paredit_backward_kill_form")
        self.assertEquals("", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

    def test_forward_kill_form(self):
        self.set_view_content("(foo ::bar baz)")
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_forward_kill_form")
        self.assertEquals("(foo  baz)", self.view_content())
        self.assertEquals([(5, 5)], self.selections())
        self.set_view_content('"foo bar baz"')
        self.set_selections((5, 5))
        self.view.run_command("tutkain_paredit_forward_kill_form")
        self.assertEquals('"foo  baz"', self.view_content())
        self.assertEquals([(5, 5)], self.selections())
        self.set_view_content("; foo bar baz")
        self.set_selections((6, 6))
        self.view.run_command("tutkain_paredit_forward_kill_form")
        self.assertEquals("; foo  baz", self.view_content())
        self.assertEquals([(6, 6)], self.selections())
        self.set_view_content("(foo ::bar baz)")
        self.set_selections((0, 15))
        self.view.run_command("tutkain_paredit_forward_kill_form")
        self.assertEquals("", self.view_content())
        self.assertEquals([(0, 0)], self.selections())

    def test_move_form(self):
        self.set_view_content('(foo (bar) baz "qux" 1/2 ::quux/quuz)')
        self.set_selections((25, 25))
        self.view.run_command("tutkain_paredit_backward_move_form")
        self.assertEquals('(foo (bar) baz "qux" ::quux/quuz 1/2)', self.view_content())
        self.assertEquals([(21, 21)], self.selections())
        self.view.run_command("tutkain_paredit_backward_move_form")
        self.assertEquals('(foo (bar) baz ::quux/quuz "qux" 1/2)', self.view_content())
        self.assertEquals([(15, 15)], self.selections())
        self.view.run_command("tutkain_paredit_backward_move_form")
        self.assertEquals('(foo (bar) ::quux/quuz baz "qux" 1/2)', self.view_content())
        self.assertEquals([(11, 11)], self.selections())
        self.view.run_command("tutkain_paredit_backward_move_form")
        self.assertEquals('(foo ::quux/quuz (bar) baz "qux" 1/2)', self.view_content())
        self.assertEquals([(5, 5)], self.selections())
        self.view.run_command("tutkain_paredit_backward_move_form")
        self.assertEquals('(::quux/quuz foo (bar) baz "qux" 1/2)', self.view_content())
        self.assertEquals([(1, 1)], self.selections())

        # There and back again.
        self.view.run_command("tutkain_paredit_forward_move_form")
        self.assertEquals('(foo ::quux/quuz (bar) baz "qux" 1/2)', self.view_content())
        self.assertEquals([(5, 5)], self.selections())
        self.view.run_command("tutkain_paredit_forward_move_form")
        self.assertEquals('(foo (bar) ::quux/quuz baz "qux" 1/2)', self.view_content())
        self.assertEquals([(11, 11)], self.selections())
        self.view.run_command("tutkain_paredit_forward_move_form")
        self.assertEquals('(foo (bar) baz ::quux/quuz "qux" 1/2)', self.view_content())
        self.assertEquals([(15, 15)], self.selections())
        self.view.run_command("tutkain_paredit_forward_move_form")
        self.assertEquals('(foo (bar) baz "qux" ::quux/quuz 1/2)', self.view_content())
        self.assertEquals([(21, 21)], self.selections())
        self.view.run_command("tutkain_paredit_forward_move_form")

        # Newlines
        self.set_view_content("(->\n  (foo)\n  (bar)\n  (baz))")
        self.set_selections((22, 22))
        self.view.run_command("tutkain_paredit_backward_move_form")
        self.assertEquals("(->\n  (foo)\n  (baz)\n  (bar))", self.view_content())
        self.assertEquals([(14, 14)], self.selections())
        self.view.run_command("tutkain_paredit_backward_move_form")
        self.assertEquals("(->\n  (baz)\n  (foo)\n  (bar))", self.view_content())
        self.assertEquals([(6, 6)], self.selections())
        self.view.run_command("tutkain_paredit_backward_move_form")
        self.assertEquals("((baz)\n  ->\n  (foo)\n  (bar))", self.view_content())
        self.assertEquals([(1, 1)], self.selections())
        self.view.run_command("tutkain_paredit_backward_move_form")
        self.assertEquals("((baz)\n  ->\n  (foo)\n  (bar))", self.view_content())
        self.assertEquals([(1, 1)], self.selections())

        # Round trippin'
        self.view.run_command("tutkain_paredit_forward_move_form")
        self.assertEquals("(->\n  (baz)\n  (foo)\n  (bar))", self.view_content())
        self.assertEquals([(6, 6)], self.selections())
        self.view.run_command("tutkain_paredit_forward_move_form")
        self.assertEquals("(->\n  (foo)\n  (baz)\n  (bar))", self.view_content())
        self.assertEquals([(14, 14)], self.selections())
        self.view.run_command("tutkain_paredit_forward_move_form")
        self.assertEquals("(->\n  (foo)\n  (bar)\n  (baz))", self.view_content())
        self.assertEquals([(22, 22)], self.selections())
        self.view.run_command("tutkain_paredit_forward_move_form")
        self.assertEquals("(->\n  (foo)\n  (bar)\n  (baz))", self.view_content())
        self.assertEquals([(22, 22)], self.selections())

    def test_thread_first(self):
        self.set_view_content("(inc (dec (* 2 (/ 4 10))))")
        self.set_selections((18, 18))
        self.view.run_command("tutkain_paredit_thread_first")
        self.assertEquals("(inc (dec (* 2 (-> 4 (/ 10)))))", self.view_content())
        self.assertEquals([(15, 15)], self.selections())
        self.view.run_command("tutkain_paredit_thread_first")
        self.assertEquals("(inc (dec (-> 4 (/ 10) (* 2))))", self.view_content())
        self.assertEquals([(10, 10)], self.selections())
        self.view.run_command("tutkain_paredit_thread_first")
        self.assertEquals("(inc (-> 4 (/ 10) (* 2) (dec)))", self.view_content())
        self.assertEquals([(5, 5)], self.selections())
        self.view.run_command("tutkain_paredit_thread_first")
        self.assertEquals("(-> 4 (/ 10) (* 2) (dec) (inc))", self.view_content())
        self.assertEquals([(0, 0)], self.selections())
