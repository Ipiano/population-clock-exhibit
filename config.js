var config = {
  component_dividing_header: "Annual Population Estimates",
  learn_more_link_label: "Learn More",
  share_link_label: "Download and Share",
  view_data_table_link_label: "View Data Table",
  embed_world_footnotes: {
    world_counter: {
      label: "World Population",
      content:
        '<p>World Population Clock Source: U.S. Census Bureau, International Database (demographic data) and USA Trade Online (trade data).</p>\r\n\t\t\t\t<p>Populations shown for the Most Populous Countries and on the world map are projected to July 1, 2022.</p>\r\n                                <p>To learn more about world population projections, go to <a href="https://www.census.gov/data/data-tools/population-clock/world-notes.html">Notes on the World Population Clock</a>.</p>\r\n                                <p>To learn more about international trade data, go to <a href="https://www.census.gov/foreign-trade/guide/index.html">Guide to Foreign Trade Statistics</a>.</p>\r\n\t\t\t\t<p>Coordinated Universal Time (UTC) is the equivalent of Eastern Standard Time (EST) plus 5 hours or Eastern Daylight Saving Time (EDT) plus 4 hours.</p>',
    },
  },
  world_footnotes: {
    label: "About the Population Clock and Population Estimates",
    map: {
      label: "Source and Notes",
      content:
        '<p>Source: U.S. Census Bureau, <a href="https://www.census.gov/programs-surveys/international-programs/about/idb.html">International Database</a> (demographic data) and <a href="http://usatrade.census.gov/">USA Trade Online</a> (trade data).</p>\r\n\t\t\t\t<p>Populations shown for the Most Populous Countries and on the world map are projected to July 1, 2022.</p>\r\n\r\n                                <p>To learn more about world population projections, go to <a href="https://www.census.gov/data/data-tools/population-clock/world-notes.html">Notes on the World Population Clock</a>.</p>\r\n                                <p>To learn more about international trade data, go to <a href="https://www.census.gov/foreign-trade/guide/index.html">Guide to Foreign Trade Statistics</a>.</p>\r\n\r\n\r\n\r\n\r\n\t\t\t\t<p>All trade figures are in U.S. dollars on a nominal basis.</p>\r\n\t\t\t\t<p>Coordinated Universal Time (UTC) is the equivalent of Eastern Standard Time (EST) plus 5 hours or Eastern Daylight Saving Time (EDT) plus 4 hours.</p>',
    },
    country: {
      label: "Source and Notes",
      content:
        '<p>Source: U.S. Census Bureau, <a href="https://www.census.gov/programs-surveys/international-programs/about/idb.html">International Database</a> (demographic data) and <a href="http://usatrade.census.gov">USA Trade Online</a> (trade data); Central Intelligence Agency, The World Fact Book (country reference maps).</p>\r\n\t\t\t\t<p>This application presents data for 228 countries and areas of the world with a 2022 population of 5,000 or more. For eleven of those countries and areas, only demographic data are presented. </p>\r\n\t\t\t\t<p>"Data not available" indicates that data are not available from this application.  In such instances, data may be available elsewhere at the census.gov website.</p>\r\n\t\t\t\t<p>Trade figures presented for France do not include data for overseas departments French Guiana, Guadeloupe, Martinique, Mayotte, and Reunion but do include data for dependencies Saint Barthelemy and Saint Martin.  Trade figures for the United Kingdom include data for crown dependencies Guernsey, Isle of Man, and Jersey.</p>\r\n                                <p>To learn more about world population projections, go to <a href="https://www.census.gov/data/data-tools/population-clock/world-notes.html">Notes on the World Population Clock</a>.</p>\r\n                                <p>To learn more about international trade data, go to <a href="https://www.census.gov/foreign-trade/guide/index.html">Guide to Foreign Trade Statistics</a>.</p>\r\n\t\t\t\t<p>All trade figures are in U.S. dollars on a nominal basis.</p>',
    },
  },
  footnotes: {
    label: "About the Population Clock and Population Estimates",
    counter: {
      label: "U.S. Population",
      content:
        '\r\n                     <p>The U.S. population clock is based on a series of short-term projections for the resident population of the United States. This includes people whose usual residence is in the 50 states and the District of Columbia. These projections do not include members of the Armed Forces overseas, their dependents, or other U.S. citizens residing outside the United States.</p>\r\n                     <p>The projections are based on a monthly series of population estimates starting with the April 1, 2020 resident population from the 2020 Census.</p>\r\n\t\t<p>At the end of each year, a revised series of population estimates from the census date forward is used to update the short-term projections for the population clock. Once the updated series of monthly projections is completed, the daily population clock values are derived by interpolation. Within each calendar month, the daily numerical population change is assumed to be constant, subject to negligible differences caused by rounding.</p>\r\n\t\t\t\t<p>Population estimates produced by the U.S. Census Bureau for the United States, states, metropolitan and micropolitan statistical areas, counties, cities, towns, as well as for Puerto Rico and its municipios can be found on the <a href="//www.census.gov/programs-surveys/popest.html"> Population Estimates</a> web page. Projections of the future population for the United States can be found on the <a href="//www.census.gov/programs-surveys/popproj.html">Population Projections</a> web page.</p>',
    },
    pop_on_date: { label: "", content: "" },
    growth: { label: "", content: "" },
    pyramid: { label: "", content: "" },
    populous: { label: "", content: "" },
    density: { label: "", content: "" },
  },
  components: {
    counter: { label: "Population Counters" },
    us: {
      label: "U.S. Population",
      url: "https://www.census.gov/popclock/?intcmp=w_200x402",
      interval: 15,
      birth_rate_label: "One birth every <strong>%@ seconds</strong>",
      death_rate_label: "One death every <strong>%@ seconds</strong>",
      immigrant_rate_label:
        "One international migrant (net) every <strong>%@ seconds</strong>",
      net_gain_label:
        "Net gain of one person every <strong>%@ seconds</strong>",
      learn_more_link_title: "Placeholder title for component link 1",
      share_link_title: "Placeholder title for component link 1",
    },
    us_rates: {
      label: "Components of Population Change",
      table_summary: "Placeholder for population rates table summary 1",
      table_header_labels: ["Rates", "Visualization"],
    },
    world: {
      label: "World Population",
      url: "https://www.census.gov/popclock/world?intcmp=w_200x402",
      interval: 0.1,
    },
    world_rates: {
      label:
        '<a href="./world" target="_parent" title="International Programs - Country Rank">TOP 10 MOST POPULOUS COUNTRIES (July 1, 2022) </a>',
      tables: [
        {
          title:
            '<a href="./world" title="International Programs - Country Rank">TOP 10 MOST POPULOUS COUNTRIES (July 1, 2022) </a>',
          columns: [
            "Rank. Country",
            "Population",
            "Rank. Country",
            "Population",
          ],
          rows: {
            China: 1410539758,
            India: 1389637446,
            "United States": 332838183,
            Indonesia: 277329163,
            Pakistan: 242923845,
            Nigeria: 225082083,
            Brazil: 217240060,
            Bangladesh: 165650475,
            Russia: 142021981,
            Mexico: 129150971,
          },
          vintage: "2012",
          table_summary: "Placeholder for population rates table summary 5",
        },
        {
          title:
            '<a href="./population/international/data/countryrank/rank.php" title="International Programs - Country Rank">Top 10 Fastest Growing Countries</a>',
          columns: ["Rank", "Country"],
          rows: {
            China: 1410539758,
            India: 1389637446,
            "United States": 332838183,
            Indonesia: 277329163,
            Pakistan: 242923845,
            Nigeria: 225082083,
            Brazil: 217240060,
            Bangladesh: 165650475,
            Russia: 142021981,
            Mexico: 129150971,
          },
          vintage: "2012",
          table_summary: "Placeholder for population rates table summary 6",
        },
      ],
    },
    pop_on_date: {
      label: "The United States population on %@ %@: %@",
      default_year: "2022",
      default_month: "08",
      default_day: "20",
      min_year: 2020,
      min_month: 4,
      min_day: 1,
      learn_more_link_title: "Placeholder title for component link 2",
      share_link_title: "Placeholder title for component link 2",
    },
    growth: {
      label: "United States Population Growth by Region",
      y_axis_label: "Population (in millions)",
      min_year: 2020,
      max_year: 2021,
      learn_more_link_title: "Placeholder title for component link 3",
      share_link_title: "Placeholder title for component link 3",
      view_data_table_link_title: "Placeholder title for component link3",
      table_summary: "Placeholder for population rates table summary 3",
      table_header_labels: [
        "Region",
        "Population",
        "Visualization",
        "Percentage",
      ],
    },
    pyramid: {
      label: "United States Population by Age and Sex",
      x_axis_label_middle: "% of Population",
      x_axis_label_modifier: "%",
      min_year: 2020,
      max_year: 2021,
      max_total_percentage: 1,
      table_summary: "Placeholder for population rates table summary 4",
      learn_more_link_title: "Placeholder title for component link 4",
      share_link_title: "Placeholder title for component link 4",
      view_data_table_link_title: "Placeholder title for component link4",
    },
    populous: {
      label: "Most Populous",
      learn_more_link_title: "Placeholder title for component link 5",
      share_link_title: "Placeholder title for component link 5",
      tables: [
        {
          title: "States",
          columns: ["State", "Population", "Pop. per sq. mi."],
          vintage: "2021",
          table_summary: "Placeholder for population rates table summary 7",
        },
        {
          title: "Counties",
          columns: ["County", "Population", "Pop. per sq. mi."],
          vintage: "2021",
          table_summary: "Placeholder for population rates table summary 6",
        },
        {
          title: "Cities",
          columns: ["City, ST", "Population", "Pop. per sq. mi."],
          vintage: "2021",
          table_summary: "Placeholder for population rates table summary 5",
        },
      ],
    },
    density: {
      label: "Highest Density",
      learn_more_link_title: "Placeholder title for component link 6",
      share_link_title: "Placeholder title for component link 6",
      tables: [
        {
          title: "States",
          columns: ["State", "Population", "Pop. per sq. mi."],
          vintage: "2021",
          table_summary: "Placeholder for population rates table summary 10",
        },
        {
          title: "Counties",
          columns: ["County", "Population", "Pop. per sq. mi."],
          vintage: "2021",
          table_summary: "Placeholder for population rates table summary 9",
        },
        {
          title: "Cities",
          columns: ["City, ST", "Population", "Pop. per sq. mi."],
          vintage: "2021",
          table_summary: "Placeholder for population rates table summary 8",
        },
      ],
    },
  },
  api: {
    cache: false,
    methods: {
      us: { url: "https://www.census.gov/popclock/data/population.php/us" },
      world: {
        url: "https://www.census.gov/popclock/data/population.php/world",
      },
      pop_on_date: {
        url: "https://www.census.gov/popclock/data/population.php/us",
      },
      region: {
        url: "https://www.census.gov/popclock/data/population.php/region",
        data: { regions: "west,midwest,northeast,south" },
      },
      demographic: {
        url: "https://www.census.gov/popclock/data/population.php/demographic",
      },
      populous: {
        url: "https://www.census.gov/popclock/data/population.php/rank",
        data: {
          type: "states,counties,cities",
          sort: "population:DESC",
          limit: 10,
        },
      },
      density: {
        url: "https://www.census.gov/popclock/data/population.php/rank",
        data: {
          type: "states,counties,cities",
          sort: "density:DESC",
          limit: 10,
        },
      },
    },
  },
  share: {
    components: {
      counter: {
        pinterest:
          "Every minute the US #population is changing, see population changes @uscensusbureau Population Clock",
        facebook:
          "Every minute the U.S. population is changing, see how quickly it changes with the Census' Population Clock.",
        twitter:
          "Every minute the US #population is changing, see population changes @uscensusbureau Population Clock",
        email:
          "Every minute the U.S. population is changing, see how quickly it changes with the Census' Population Clock. %url%",
      },
      pop_on_date: {
        pinterest:
          "Did u know the US #population on %date% was %population%? Discover more with @uscensusbureau Population Clock",
        facebook:
          "Did you know the U.S. population on %date% was %population%? Discover how it has changed since with the new Census' Population Clock.",
        twitter:
          "Did u know the US #population on %date% was %population%? Discover more with @uscensusbureau Population Clock",
        email:
          "Did you know the U.S. population on %date% was %population%? Discover how it has changed since with the new Census' Population Clock. %url%",
      },
      growth: {
        pinterest:
          "How is the US #population changing, region by region? Find out with #Census' Population Clock. @uscensusbureau",
        facebook:
          "How is the U.S. population changing, region by region? Find out with the new Census' Population Clock.",
        twitter:
          "How is the US #population changing, region by region? Find out with #Census' Population Clock. @uscensusbureau %image%",
        email:
          "How is the U.S. population changing, region by region? Find out with the new Census' Population Clock. %url%",
      },
      pyramid: {
        pinterest:
          "What % of US women are #age 35? Men who are 58? Find out with @uscensusbureau #Population Clock",
        facebook:
          "What percentage of U.S. women are age 35? Men who are 58? Find out with the new Census' Population Clock.",
        twitter:
          "What % of US women are #age 35? Men who are 58? Find out with @uscensusbureau #Population Clock %image%",
        email:
          "What percentage of U.S. women are age 35? Men who are 58? Find out with the new Census' Population Clock. %url%",
      },
      populous: {
        pinterest:
          "What are the most populous US states, counties and cities? Find out with @uscensusbureau #Population Clock.",
        facebook:
          "What are the most populous U.S. states, counties and cities? Find out with the new Census' Population Clock.",
        twitter:
          "What are the most populous US states, counties and cities? Find out with @uscensusbureau #Population Clock.",
        email:
          "What are the most populous U.S. states, counties and cities? Find out with the new Census' Population Clock. %url%",
      },
      density: {
        pinterest:
          "Which US states and counties have the highest #population densities? Find out with @uscensusbureau Population Clock.",
        facebook:
          "Which U.S. states and counties have the highest population densities? Find out with the new Census Population Clock.",
        twitter:
          "Which US states and counties have the highest #population densities? Find out with @uscensusbureau Population Clock.",
        email:
          "Which U.S. states and counties have the highest population densities? Find out with the new Census Population Clock. %url%",
      },
    },
    pinterest: {},
    facebook: {
      title: "Census Population Clock",
      site_name: "Census.gov",
      type: "government",
      tags: { admins: "100003365860983" },
    },
    twitter: {},
    email: { to: "", subject: "Check out the Census Population Clock" },
    url: "http://go.usa.gov/2Y45",
    image: "https://www.census.gov/images/census-logo-whiteBG.png",
  },
};
