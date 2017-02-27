# fika-analyzer
Gathers statistics from a wiki. Currently, values are hard coded for Fikarummet (the equivalent to the english Teahouse) on sv.wikipedia.org.
The statistics gathered are:

1. Pageviews, for *Wikipedia:Fikarummet* and *Wikipedia:Fikarummet/Frågor*.
  * Uses [RestBASE](https://wikimedia.org/api/rest_v1/#/).
1. Number of users in category *Kategori:Wikipedianer som har fått en inbjudan till fikarummet*.
  * Uses the [action API](https://www.mediawiki.org/wiki/API:Main_page).
  * Users are added to this category when they receive an invitation.
1. Number of questions asked on *Wikipedia:Fikarummet/Frågor*.
  * Uses the action API.
  * Counts the number of sections; a new sections is created when a question is asked.
