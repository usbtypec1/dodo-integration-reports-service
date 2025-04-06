import datetime
from dataclasses import dataclass
from typing import Self
from zoneinfo import ZoneInfo


@dataclass(frozen=True, slots=True, kw_only=True)
class Period:
    from_date: datetime.datetime
    to_date: datetime.datetime

    @classmethod
    def today_to_this_time(cls, timezone: ZoneInfo | None = None) -> Self:
        """
        Returns the current date and time in the specified timezone.
        If no timezone is provided, it defaults to UTC.
        """
        if timezone is None:
            timezone = ZoneInfo("UTC")

        now = datetime.datetime.now(tz=timezone)

        return cls(
            from_date=now.replace(hour=0, minute=0, second=0, microsecond=0),
            to_date=now,
        )

    def round_to_upper_hour(self) -> Self:
        """
        Rounds the 'to_date' attribute to the next hour.
        """
        rounded_to_date = self.to_date.replace(
            minute=0, second=0, microsecond=0
        ) + datetime.timedelta(hours=1)

        return type(self)(from_date=self.from_date, to_date=rounded_to_date)

    @classmethod
    def week_before_to_this_time(cls, timezone: ZoneInfo | None = None) -> Self:
        """
        Returns the current date and time in the specified timezone.
        If no timezone is provided, it defaults to UTC.
        """
        if timezone is None:
            timezone = ZoneInfo("UTC")

        week_before = datetime.datetime.now(tz=timezone) - datetime.timedelta(
            weeks=1
        )

        from_date = week_before.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        to_date = week_before

        return cls(from_date=from_date, to_date=to_date)
