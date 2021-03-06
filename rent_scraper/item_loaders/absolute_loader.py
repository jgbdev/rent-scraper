from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose, Join

from rent_scraper.processors.absolute_processor import AbsolutePriceProcessor
from rent_scraper.processors.common_processors import TextSearch, Concatenate, Get, Split


class AbsolutePropertyLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    area_in = Identity()

    street_name_in = Compose(Split(','), Get(0), Get(1))

    postcode_in = Compose(Split(','), Get(0), Get(2))

    price_per_month_in = AbsolutePriceProcessor()

    description_out = Join()

    amenities_in = Concatenate(
            Compose(TextSearch('washing machine'), lambda x: ['Washing machine'] if x else []),
            Compose(TextSearch('parking'), lambda x: ['Parking'] if x else []),
            Compose(TextSearch('dishwasher'), lambda x: ['Dishwasher'] if x else [])
    )
    amenities_out = Identity()

    heating_type_in = Compose(TextSearch('gas'), lambda is_gas: 'gas' if is_gas else 'unknown')

    let_agreed_in = Compose(lambda xs: 'Yes' if any('Let' in x for x in xs) else 'No')