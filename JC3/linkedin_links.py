#!/usr/bin/env python3
"""Generate personalized LinkedIn direct search URLs for each friend.

Since LinkedIn was removed from automated search (Feb 2026) due to Google
index staleness, friends receive direct LinkedIn search links instead.
These links open LinkedIn's native job search with the friend's roles and
locations pre-filled.

Usage:
  python3 JC3/linkedin_links.py           # all users
  python3 JC3/linkedin_links.py phil      # one user
  python3 JC3/linkedin_links.py vivienne  # one user

Output: Formatted links + email-ready block for delivery emails.
"""

import sys
import urllib.parse

# ---------------------------------------------------------------------------
# Friend configurations (roles + locations)
# Keep in sync with ONE_CLICK files
# ---------------------------------------------------------------------------

FRIENDS = {
    "joey": {
        "display_name": "Joey Clark",
        "roles": [
            "Chief of Staff",
            "Strategic Operations",
            "Partnerships",
            "Business Development",
        ],
        "locations": [
            "Washington DC",
            "Remote",
            "Lisbon Portugal",
        ],
    },
    "aaron": {
        "display_name": "Aaron Kimson",
        "roles": [
            "L/S Hedge Fund Analyst",
            "Hedge Fund PM",
            "Equity Research",
            "Investment Analyst",
        ],
        "locations": [
            "New York",
            "San Francisco",
            "Chicago",
            "Miami",
            "Boston",
        ],
    },
    "phil": {
        "display_name": "Phil Tassi",
        "roles": [
            "Chief of Staff",
            "Partnerships",
            "Business Development",
        ],
        "locations": [
            "Washington DC",
            "London UK",
        ],
    },
    "vivienne": {
        "display_name": "Vivienne Pham",
        "roles": [
            # Archetype 1: Operator
            "CFO",
            "VP Finance",
            # Archetype 2: Capital Markets
            "Investor Relations",
            # Archetype 3: Ecosystem
            "Business Development",
            "Portfolio Operations",
        ],
        "locations": [
            "New York",
            "Washington DC",
            "Remote",
        ],
    },
    "rosalind": {
        "display_name": "Rosalind",
        "roles": [
            "Chief of Staff",
            "Operations",
        ],
        "locations": [
            "Remote",
        ],
    },
}


def build_linkedin_url(role, location):
    """Build a LinkedIn job search URL with role and location pre-filled."""
    params = {
        "keywords": role,
        "location": location,
        "f_TPR": "r604800",  # past week
    }
    return "https://www.linkedin.com/jobs/search/?" + urllib.parse.urlencode(params)


def generate_links(slug):
    """Generate all LinkedIn search links for a friend."""
    config = FRIENDS[slug]
    name = config["display_name"]
    roles = config["roles"]
    locations = config["locations"]

    print(f"\n{'='*70}")
    print(f"  LinkedIn Search Links — {name}")
    print(f"  {len(roles)} roles × {len(locations)} locations = {len(roles) * len(locations)} links")
    print(f"{'='*70}\n")

    links = []
    for role in roles:
        for location in locations:
            url = build_linkedin_url(role, location)
            links.append((role, location, url))
            print(f"  {role} — {location}")
            print(f"  {url}\n")

    # Email-ready block
    print(f"{'─'*70}")
    print(f"  EMAIL-READY BLOCK (copy-paste into delivery email or xlsx Tab 3)")
    print(f"{'─'*70}\n")

    print(f"LinkedIn Direct Search Links for {name}")
    print(f"(These open LinkedIn's job search with your criteria pre-filled)\n")

    for role, location, url in links:
        print(f"• {role} in {location}")
        print(f"  {url}\n")

    print(f"Tip: Set LinkedIn alerts for these searches to get daily notifications.")

    return links


def main():
    args = [a.lower() for a in sys.argv[1:]]

    if args:
        slug = args[0]
        # Fuzzy match: "phil" matches "phil", "vivienne" matches "vivienne"
        matches = [k for k in FRIENDS if k.startswith(slug)]
        if not matches:
            print(f"User '{slug}' not found. Available: {', '.join(FRIENDS.keys())}")
            sys.exit(1)
        for match in matches:
            generate_links(match)
    else:
        for slug in FRIENDS:
            generate_links(slug)


if __name__ == "__main__":
    main()
