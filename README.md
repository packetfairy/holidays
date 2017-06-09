# holidays

I was working on this project that called for having an easy way to define
holidays, and to select the appropriate "observed" work day for that holiday
if the holiday should fall over a weekend. I found a couple existing modules
that defined a set of holidays, but I didn't immediately find anything that
was flexible... nothing where I could easily define a set of the days to be
observed for instance (eg: for our purposes, we don't care about Arbor Day).

This, as with all my things, could probably have been written more cleverly,
but it does what I need it to do.

It comes with a predefined set of US observed holidays (those typically
observed by companies in the bay area, in my experience), and can be used to
define any set of holidays using the provided criteria.

Update 2017-06-08 - I realized today that this DOES NOT do everything I think
and want it to do. For example, look at Thanksgiving in 2024. Anyway, you
probably shouldn't use it right now (because so many people are using it!).
