import logging
import argparse
from datetime import date

import requests


def get_pageviews(
        project,
        page,
        start_date,
        end_date,
        access="all-access",
        agent="user",
        granularity="daily"
):
    """Get the pageviews for a page."""

    response = send_pageview_request(
        project=project,
        page=page,
        start_date=start_date,
        end_date=end_date,
        access=access,
        agent=agent,
        granularity=granularity
    )
    pageviews = 0
    for item in response["items"]:
        pageviews += item["views"]
    logging.info("Total pageviews: {}.".format(pageviews))
    return pageviews


def send_pageview_request(
        project,
        access,
        agent,
        page,
        granularity,
        start_date,
        end_date
):
    """Send request for pageviews to the API.

    Returns the JSON response for the request, as a dictionary.
    """

    api_base_url = "https://wikimedia.org/api/rest_v1"
    pageview_path = "metrics/pageviews/per-article"
    url = "{base}/{pageview}/{project}/{access}/{agent}/{article}/" \
          "{granularity}/{start}/{end}".format(
              base=api_base_url,
              pageview=pageview_path,
              project=project,
              access=access,
              agent=agent,
              article=page,
              granularity=granularity,
              start=start_date,
              end=end_date
          )
    request = requests.get(url)
    response = request.json()
    logging.debug("Response: {}".format(response))
    return response


def get_number_of_questions():
    """Get the number of questions from the questions page.

    The number of sections are used to count questions.
    """

    response = send_sections_request(
        api_url="https://sv.wikipedia.org/w/api.php",
        page="Wikipedia:Fikarummet/Frågor"
    )
    sections = response["parse"]["sections"]
    number_of_questions = 0
    for section in sections:
        if int(section["level"]) == 2:
            # Each question creates a section of level 2.
            number_of_questions += 1
    return number_of_questions


def send_sections_request(api_url, page):
    """Send a request to the action API, asking for the sections of a page.

    Returns the JSON response for the request, as a dictionary.
    """
    response = requests.get(
        url=api_url,
        params={
            "action": "parse",
            "format": "json",
            "page": page,
            "prop": "sections"
        }
    ).json()
    return response


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.DEBUG
    )
    pageviews = get_pageviews(
        "sv.wikipedia.org",
        "Wikipedia:Fikarummet",
        "20161209",
        date.today().strftime("%Y%m%d")
    )
    print("Pageviews: {}".format(pageviews))
    number_of_questions = get_number_of_questions()
    print("Number of questions: {}".format(number_of_questions))
