import argparse

from scraping import Scraping


def main(verbose):
    # BURBERRY
    base_url = "https://us.burberry.com/womens-new-arrivals-new-in/"
    urls = [
        base_url,
        base_url + "?start=2&pageSize=120&productsOffset=&cellsOffset=8&cellsLimit=&__lang=en"
    ]

    df_burberry = Scraping(verbose).process(
        urls,
        lambda x: "-p80" in x,
        lambda docs: '-'.join(docs).replace('/', ''),
        "SS2020_Burberry_word_frequency.jpg",
        'burberry'
    )

    # VERSACE
    tail = '/us/en-us/women/new-arrivals/new-in/'
    urls = ["https://www.versace.com" + tail]

    df_versace = Scraping(verbose).process(
        urls,
        lambda x: x.startswith(tail),
        lambda docs: '-'.join([doc.replace(tail, '').split('/')[0] for doc in docs if not doc.startswith(tail + "?")]),
        "SS2020_Versace_word_frequency.jpg",
        'versace'
    )

    print(df_burberry)
    print(df_versace)
    # ...


def parse_args():
    parser = argparse.ArgumentParser(description='Run the best solution')

    parser.add_argument('-v', default=True, help='Do we need to activate all prints?')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args.verbose)
