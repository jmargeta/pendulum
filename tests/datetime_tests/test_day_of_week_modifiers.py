import pendulum
from pendulum import DateTime
from pendulum.exceptions import DateTimeException

from .. import AbstractTestCase


class DayOfWeekModifiersTest(AbstractTestCase):

    def test_set_weekend_days_invalid_value(self):
        self.assertRaises(ValueError, DateTime.set_weekend_days, [7])

    def test_get_weekend_days(self):
        self.assertEqual(
            [pendulum.SATURDAY, pendulum.SUNDAY],
            DateTime.get_weekend_days()
        )
        DateTime.set_weekend_days([pendulum.FRIDAY, pendulum.SATURDAY])
        self.assertEqual(
            [pendulum.FRIDAY, pendulum.SATURDAY],
            DateTime.get_weekend_days()
        )
        DateTime.set_weekend_days([pendulum.SATURDAY, pendulum.SUNDAY])

    def test_set_week_ends_at_invalid_value(self):
        self.assertRaises(ValueError, DateTime.set_week_ends_at, 7)

    def test_get_week_ends_at(self):
        DateTime.set_week_ends_at(pendulum.SATURDAY)
        self.assertEqual(DateTime.get_week_ends_at(), pendulum.SATURDAY)
        DateTime.set_week_ends_at(pendulum.SUNDAY)

    def test_set_week_starts_at_invalid_value(self):
        self.assertRaises(ValueError, DateTime.set_week_starts_at, 7)

    def test_get_week_starts_at(self):
        DateTime.set_week_starts_at(pendulum.TUESDAY)
        self.assertEqual(DateTime.get_week_starts_at(), pendulum.TUESDAY)
        DateTime.set_week_starts_at(pendulum.MONDAY)

    def test_start_of_week(self):
        d = DateTime(1980, 8, 7, 12, 11, 9).start_of('week')
        self.assertDateTime(d, 1980, 8, 4, 0, 0, 0)

    def test_start_of_week_from_week_start(self):
        d = DateTime(1980, 8, 4).start_of('week')
        self.assertDateTime(d, 1980, 8, 4, 0, 0, 0)

    def test_start_of_week_crossing_year_boundary(self):
        d = DateTime.create(2014, 1, 1).start_of('week')
        self.assertDateTime(d, 2013, 12, 30, 0, 0, 0)

    def test_end_of_week(self):
        d = DateTime(1980, 8, 7, 12, 11, 9).end_of('week')
        self.assertDateTime(d, 1980, 8, 10, 23, 59, 59)

    def test_end_of_week_from_week_end(self):
        d = DateTime(1980, 8, 10).end_of('week')
        self.assertDateTime(d, 1980, 8, 10, 23, 59, 59)

    def test_end_of_week_crossing_year_boundary(self):
        d = DateTime.create(2013, 12, 31).end_of('week')
        self.assertDateTime(d, 2014, 1, 5, 23, 59, 59)

    def test_next(self):
        d = DateTime.create(1975, 5, 21).next()
        self.assertDateTime(d, 1975, 5, 28, 0, 0, 0)

    def test_next_monday(self):
        d = DateTime.create(1975, 5, 21).next(pendulum.MONDAY)
        self.assertDateTime(d, 1975, 5, 26, 0, 0, 0)

    def test_next_saturday(self):
        d = DateTime.create(1975, 5, 21).next(6)
        self.assertDateTime(d, 1975, 5, 24, 0, 0, 0)

    def test_next_keep_time(self):
        d = DateTime.create(1975, 5, 21, 12).next()
        self.assertDateTime(d, 1975, 5, 28, 0, 0, 0)

        d = DateTime.create(1975, 5, 21, 12).next(keep_time=True)
        self.assertDateTime(d, 1975, 5, 28, 12, 0, 0)

    def test_previous(self):
        d = DateTime.create(1975, 5, 21).previous()
        self.assertDateTime(d, 1975, 5, 14, 0, 0, 0)

    def test_previous_monday(self):
        d = DateTime.create(1975, 5, 21).previous(pendulum.MONDAY)
        self.assertDateTime(d, 1975, 5, 19, 0, 0, 0)

    def test_previous_saturday(self):
        d = DateTime.create(1975, 5, 21).previous(6)
        self.assertDateTime(d, 1975, 5, 17, 0, 0, 0)

    def test_previous_keep_time(self):
        d = DateTime.create(1975, 5, 21, 12).previous()
        self.assertDateTime(d, 1975, 5, 14, 0, 0, 0)

        d = DateTime.create(1975, 5, 21, 12).previous(keep_time=True)
        self.assertDateTime(d, 1975, 5, 14, 12, 0, 0)

    def test_first_day_of_month(self):
        d = DateTime.create(1975, 11, 21).first_of('month', )
        self.assertDateTime(d, 1975, 11, 1, 0, 0, 0)

    def test_first_wednesday_of_month(self):
        d = DateTime.create(1975, 11, 21).first_of('month', pendulum.WEDNESDAY)
        self.assertDateTime(d, 1975, 11, 5, 0, 0, 0)

    def test_first_friday_of_month(self):
        d = DateTime.create(1975, 11, 21).first_of('month', 5)
        self.assertDateTime(d, 1975, 11, 7, 0, 0, 0)

    def test_last_day_of_month(self):
        d = DateTime.create(1975, 12, 5).last_of('month', )
        self.assertDateTime(d, 1975, 12, 31, 0, 0, 0)

    def test_last_tuesday_of_month(self):
        d = DateTime.create(1975, 12, 1).last_of('month', pendulum.TUESDAY)
        self.assertDateTime(d, 1975, 12, 30, 0, 0, 0)

    def test_last_friday_of_month(self):
        d = DateTime.create(1975, 12, 5).last_of('month', 5)
        self.assertDateTime(d, 1975, 12, 26, 0, 0, 0)

    def test_nth_of_month_outside_scope(self):
        d = DateTime.create(1975, 12, 5)

        self.assertRaises(DateTimeException, d.nth_of, 'month', 6, pendulum.MONDAY)

    def test_nth_of_month_outside_year(self):
        d = DateTime.create(1975, 12, 5)

        self.assertRaises(DateTimeException, d.nth_of, 'month', 55, pendulum.MONDAY)

    def test_nth_of_month_first(self):
        d = DateTime.create(1975, 12, 5).nth_of('month', 1, pendulum.MONDAY)

        self.assertDateTime(d, 1975, 12, 1, 0, 0, 0)

    def test_2nd_monday_of_month(self):
        d = DateTime.create(1975, 12, 5).nth_of('month', 2, pendulum.MONDAY)

        self.assertDateTime(d, 1975, 12, 8, 0, 0, 0)

    def test_3rd_wednesday_of_month(self):
        d = DateTime.create(1975, 12, 5).nth_of('month', 3, 3)

        self.assertDateTime(d, 1975, 12, 17, 0, 0, 0)

    def test_first_day_of_quarter(self):
        d = DateTime.create(1975, 11, 21).first_of('quarter', )
        self.assertDateTime(d, 1975, 10, 1, 0, 0, 0)

    def test_first_wednesday_of_quarter(self):
        d = DateTime.create(1975, 11, 21).first_of('quarter', pendulum.WEDNESDAY)
        self.assertDateTime(d, 1975, 10, 1, 0, 0, 0)

    def test_first_friday_of_quarter(self):
        d = DateTime.create(1975, 11, 21).first_of('quarter', 5)
        self.assertDateTime(d, 1975, 10, 3, 0, 0, 0)

    def test_first_of_quarter_from_a_day_that_will_not_exist_in_the_first_month(self):
        d = DateTime.create(2014, 5, 31).first_of('quarter', )
        self.assertDateTime(d, 2014, 4, 1, 0, 0, 0)

    def test_last_day_of_quarter(self):
        d = DateTime.create(1975, 8, 5).last_of('quarter', )
        self.assertDateTime(d, 1975, 9, 30, 0, 0, 0)

    def test_last_tuesday_of_quarter(self):
        d = DateTime.create(1975, 8, 5).last_of('quarter', pendulum.TUESDAY)
        self.assertDateTime(d, 1975, 9, 30, 0, 0, 0)

    def test_last_friday_of_quarter(self):
        d = DateTime.create(1975, 8, 5).last_of('quarter', pendulum.FRIDAY)
        self.assertDateTime(d, 1975, 9, 26, 0, 0, 0)

    def test_last_day_of_quarter_that_will_not_exist_in_the_last_month(self):
        d = DateTime.create(2014, 5, 31).last_of('quarter', )
        self.assertDateTime(d, 2014, 6, 30, 0, 0, 0)

    def test_nth_of_quarter_outside_scope(self):
        d = DateTime.create(1975, 1, 5)

        self.assertRaises(DateTimeException, d.nth_of, 'quarter', 20, pendulum.MONDAY)

    def test_nth_of_quarter_outside_year(self):
        d = DateTime.create(1975, 1, 5)

        self.assertRaises(DateTimeException, d.nth_of, 'quarter', 55, pendulum.MONDAY)

    def test_nth_of_quarter_first(self):
        d = DateTime.create(1975, 12, 5).nth_of('quarter', 1, pendulum.MONDAY)

        self.assertDateTime(d, 1975, 10, 6, 0, 0, 0)

    def test_nth_of_quarter_from_a_day_that_will_not_exist_in_the_first_month(self):
        d = DateTime.create(2014, 5, 31).nth_of('quarter', 2, pendulum.MONDAY)
        self.assertDateTime(d, 2014, 4, 14, 0, 0, 0)

    def test_2nd_monday_of_quarter(self):
        d = DateTime.create(1975, 8, 5).nth_of('quarter', 2, pendulum.MONDAY)
        self.assertDateTime(d, 1975, 7, 14, 0, 0, 0)

    def test_3rd_wednesday_of_quarter(self):
        d = DateTime.create(1975, 8, 5).nth_of('quarter', 3, 3)
        self.assertDateTime(d, 1975, 7, 16, 0, 0, 0)

    def test_first_day_of_year(self):
        d = DateTime.create(1975, 11, 21).first_of('year', )
        self.assertDateTime(d, 1975, 1, 1, 0, 0, 0)

    def test_first_wednesday_of_year(self):
        d = DateTime.create(1975, 11, 21).first_of('year', pendulum.WEDNESDAY)
        self.assertDateTime(d, 1975, 1, 1, 0, 0, 0)

    def test_first_friday_of_year(self):
        d = DateTime.create(1975, 11, 21).first_of('year', 5)
        self.assertDateTime(d, 1975, 1, 3, 0, 0, 0)

    def test_last_day_of_year(self):
        d = DateTime.create(1975, 8, 5).last_of('year', )
        self.assertDateTime(d, 1975, 12, 31, 0, 0, 0)

    def test_last_tuesday_of_year(self):
        d = DateTime.create(1975, 8, 5).last_of('year', pendulum.TUESDAY)
        self.assertDateTime(d, 1975, 12, 30, 0, 0, 0)

    def test_last_friday_of_year(self):
        d = DateTime.create(1975, 8, 5).last_of('year', 5)
        self.assertDateTime(d, 1975, 12, 26, 0, 0, 0)

    def test_nth_of_year_outside_scope(self):
        d = DateTime.create(1975, 1, 5)

        self.assertRaises(DateTimeException, d.nth_of, 'year', 55, pendulum.MONDAY)

    def test_nth_of_year_first(self):
        d = DateTime.create(1975, 12, 5).nth_of('year', 1, pendulum.MONDAY)

        self.assertDateTime(d, 1975, 1, 6, 0, 0, 0)

    def test_2nd_monday_of_year(self):
        d = DateTime.create(1975, 8, 5).nth_of('year', 2, pendulum.MONDAY)
        self.assertDateTime(d, 1975, 1, 13, 0, 0, 0)

    def test_2rd_wednesday_of_year(self):
        d = DateTime.create(1975, 8, 5).nth_of('year', 3, pendulum.WEDNESDAY)
        self.assertDateTime(d, 1975, 1, 15, 0, 0, 0)

    def test_7th_thursday_of_year(self):
        d = DateTime.create(1975, 8, 31).nth_of('year', 7, pendulum.THURSDAY)
        self.assertDateTime(d, 1975, 2, 13, 0, 0, 0)

    def test_first_of_invalid_unit(self):
        d = DateTime.create(1975, 8, 5)

        self.assertRaises(ValueError, d.first_of, 'invalid')

    def test_last_of_invalid_unit(self):
        d = DateTime.create(1975, 8, 5)

        self.assertRaises(ValueError, d.last_of, 'invalid')

    def test_nth_of_invalid_unit(self):
        d = DateTime.create(1975, 8, 5)

        self.assertRaises(ValueError, d.nth_of, 'invalid', 3, pendulum.MONDAY)
