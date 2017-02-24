import logging
import argparse

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


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.DEBUG
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project",
        "-p",
        help="The project to retrieve metrics from, e.g. 'sv.wikipedia.org'.",
        required=True
    )
    parser.add_argument(
        "--pageview-page",
        "-v",
        help=("The page, including namespace, to get pageviews for,"
              "e.g. 'Wikipedia:Fikarummet'."),
        required=True
    )
    parser.add_argument(
        "--start-date",
        "-s",
        help="The start date of the metrics, in the format YYYYMMDD.",
        required=True
    )
    parser.add_argument(
        "--end-date",
        "-e",
        help="The end date of the metrics, in the format YYYYMMDD.",
        required=True
    )
    args = parser.parse_args()
    pageviews = get_pageviews(
        args.project,
        args.pageview_page,
        args.start_date,
        args.end_date
    )
    print("Pageviews: {}".format(pageviews))
