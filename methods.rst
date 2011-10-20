

ran v0.1 harvesting only #ows from start until 11:01 am EST Oct 13th

started v0.2 harvesting from 11:02 am EST Oct 13
harvest criteria '#ows', '#occupywallstreet', '#occupywallst', '#occupyws', 'occupywallstr'

v0.3 Started 17:07 13 Oct 2011
- Broke out User information into a seperate TwitterUser table and related tweets to that
- Added TwitterCoordinate and TwitterGeo tables to capture that information when present.

Notes:

    * 15 Oct 2011:  App stopped harvesting when twitter appeared to crash.  Lost data from roughly 7 hours of data from about 16:00 to 23:00 UTC.  Noticed.  Killed hung process and restarted usnig 'screen python manage.py twitterharvest'
    * 19 Oct 2011:  App stoopped harvesting for 18 hours.  Twitter or MySQL appeard to crash.  Restarted
    * 20 Oct 2011 10:23 am:  Modified search criteria to grab tweets with '#ows' or '#occupy' instead of specific
      occupy derivatives.
