from traceback import print_tb

import pdfplumber
import os
import pandas as pd
import itertools
import altair as alt
from vega_datasets import data

# URL from which PDF to be downloaded
PDF_URL = 'https://francais-du-monde.org/wp-content/uploads/2022/11/2024-gouvernement-francais-etranger-rapport.pdf'
PDF_LOCAL_FILE = './data/2024-gouvernement-francais-etranger-rapport.pdf'
INPUT_DATA_PICKLE = './data/df.pickle'
MAPPING_COUNTRIES = './data/translate_country_name.txt'
BAR_CHART_COUNTRIES = './fig/bar_chart_countries.png'
GEO_CHART_POPULATION_WORLD = './fig/geo_chart_population_world.png'
GEO_CHART_POPULATION_EUROPE = './fig/geo_chart_population_europe.png'
GEO_CHART_RATE_WORLD = './fig/geo_chart_rate_world.png'
GEO_CHART_RATE_EUROPE = './fig/geo_chart_rate_europe.png'

COUNTRY_LIMIT = 15

class ReportData:
    def __init__(self):
        self.df = self.load_data()

    def get_current_location(self):
        """
        Support function to return the current directly
        :return: prints the current directory
        """
        print(os.getcwd())

    def plot_geo_distribution(self):
        """
        Plots geo chart
        :return: chart of populaton
        """

        countries = alt.topo_feature(data.world_110m.url, "countries")

        country_codes = pd.read_csv(
            "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"
        )

        def plot_inner_geo_chart(filename_save_data, view, data):

            #
            if data == 'population':
                source = 'Population 2023'
                scheme_ = 'reds'
            else:
                source = 'Change 2023/2022 (%)'
                scheme_ = 'blueorange'

            if view=='world':
                direction_ = 'horizontal'
                orient_ = 'bottom-left'
            else:
                direction_ = 'vertical'
                orient_ = 'right'

            # background
            background = alt.Chart(countries).mark_geoshape(fill="lightgray")

            # we transform twice, first from "ISO 3166-1 numeric" to name, then from name to value
            foreground = (
                alt.Chart(countries)
                .mark_geoshape()
                .transform_lookup(
                    lookup="id",
                    from_=alt.LookupData(data=country_codes, key="country-code", fields=["name"]),
                )
                .transform_lookup(
                    lookup="name",
                    from_=alt.LookupData(data=self.df, key="name", fields=[f"{source}"]),
                )
                .encode(
                    fill=alt.Color(
                        f"{source}:Q",
                        scale=alt.Scale(scheme=scheme_),
                        legend=alt.Legend(
                            orient=orient_,
                            direction=direction_,
                            titleColor='black', titleFontSize=14,
                            gradientLength=560, gradientThickness=20)
                    )
                )
            ).properties(
                title={
                          "text": [f"Population of French People outside France in 2023"],
                          "subtitle": ["Government report 2024"],
                          "color": "black",
                          "subtitleColor": "black"
                        }
            )

            if view == 'world':
                chart = (
                    (background + foreground)
                    .properties(width=600, height=600)
                    .project(
                        type="equirectangular"
                    )
                )
            else:
                chart = (
                    (background + foreground)
                    .properties(width=600, height=600)
                    .project(
                        type="equalEarth",
                        scale=800,
                        translate=[200, 1000],
                    )
                )

            chart.save(filename_save_data)

        # World and Europe view
        plot_inner_geo_chart(GEO_CHART_POPULATION_WORLD, 'world', 'population')
        plot_inner_geo_chart(GEO_CHART_POPULATION_EUROPE, 'europe', 'population')

        plot_inner_geo_chart(GEO_CHART_RATE_WORLD, 'world', 'rate')

    def explore_data(self):
        """
        Explore data via charts
        :return: save visualisations to png files
        """

        def plot_inner_chart(df, title_comment):
            """
            Support function to plot inner chart
            :param title_comment: information about the subset of countries, default 15
            :param df: dataframe to plot a bar chart
            :return: a chart object
            """

            base_ = alt.Chart(df).encode(
                     x=alt.X('Population 2023').title(''),
                     y=alt.Y("Country FR").sort('-x').title(''),
                     text='Population 2023',
                     color=alt.condition(alt.datum['Population 2023'] > 100000, alt.value('red'), alt.value('steelblue'))
                 ).properties(
                    title={
                      "text": [f"Population of French People outside France in 2023 {title_comment}"],
                      "subtitle": ["Government report 2024"],
                      "color": "black",
                      "subtitleColor": "black"
                    }
    )
            chart_ = base_.mark_bar() + base_.mark_text(align='left', dx=2)
            return chart_

        chart_top = plot_inner_chart(
                        df=self.df.head(COUNTRY_LIMIT),
                        title_comment=f'(top {COUNTRY_LIMIT})'
                        )
        chart_bottom = plot_inner_chart(
                        df=self.df.tail(COUNTRY_LIMIT),
                        title_comment=f'(bottom {COUNTRY_LIMIT})')

        chart = chart_top | chart_bottom

        chart.save(BAR_CHART_COUNTRIES)


    def load_data(self):
        """ Loads data from a pickle file (if exists) or from a local PDF file
         and transforms to dataframe.
         If a pickle file does not exist, then it will be created.
        :return:  with cleaned data
        """

        # Check if the file exists
        if os.path.exists(INPUT_DATA_PICKLE):
            print("Load from pickle file.")
            return pd.read_pickle(INPUT_DATA_PICKLE)

        else:
            print("Load data from local PDF and pickle.")

            # Open the PDF file and extract tables
            with pdfplumber.open(PDF_LOCAL_FILE) as pdf:

                # Extract tables using list comprehension
                # [expression for item in a list if conditional]
                pdf_tables = [page.extract_table() for page in pdf.pages if page.page_number in [151, 152, 153, 154, 155]]

            # Unpack lists
            pdf_tables = list(itertools.chain(*pdf_tables))

            # Create a dataframe based on PDF table
            df = pd.DataFrame(pdf_tables[3:])
            df.columns = ['Rang', 'Country FR', 'Population 2023', 'Change 2023/2022 (%)', 'col1', 'col2']
            df.drop(['col1', 'col2'], axis=1, inplace=True)

            # Change datatypes
            # Rang, population in 2023; and 2023/2022 are numeric columns
            # - population : remove white space (a thousand separator)
            # - change 2023/2022: remove percentage and replace separator
            df['Population 2023'] = df['Population 2023'].str.replace(' ', '')
            df['Change 2023/2022 (%)'] = df['Change 2023/2022 (%)'].str.replace('%', '')
            df['Change 2023/2022 (%)'] = df['Change 2023/2022 (%)'].str.replace(',', '.')

            # Missing entries
            # Located a deficiency in how pdfplumber operator, append missing values manually.
            df_missing_entries = pd.DataFrame({
                'Rang': ['5', '51', '97', '143'],
                'Country FR': ['Canada', 'Cambodge', 'Slovaquie', 'Zambie'],
                'Population 2023': [108847, 4967, 930, 185],
                'Change 2023/2022 (%)' : [0.65, -0.16, 7.31, -20.54]
                }
            )

            df = pd.concat([df, df_missing_entries])

            # Convert columns  to numeric
            columns_numeric = ['Rang', 'Population 2023', 'Change 2023/2022 (%)']
            df[columns_numeric] = df[columns_numeric].apply(pd.to_numeric)

            # Sort by rang
            # We added some values manually and the rang is not ordered
            df = df.sort_values(by=['Rang'], ascending=True)


            # Country names are in French, create a column with English names
            translate_country = pd.read_csv(MAPPING_COUNTRIES, sep=';')
            df = pd.merge(df, translate_country, on="Country FR")

            # Pickle
            df.to_pickle(INPUT_DATA_PICKLE)

        return df
