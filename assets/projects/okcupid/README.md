# OGPlot

OGPlot is an R Shiny dashboard for exploring patterns in OkCupid profile data from vegan and non-vegan users. The current app pairs a restyled `shinydashboard` interface with interactive charts covering essay writing, age, religion, ethnicity, language patterns, and login activity.

## Project Overview

The app is organized as a classic multi-file Shiny project:

- `ui.R` defines the dashboard layout, explanatory copy, controls, and custom styling
- `server.R` renders the charts and handles user interaction
- `global.R` loads packages, reads the datasets, and creates derived variables
- `vegan_dat.csv` and `nonvegan_dat.csv` provide the source data
- `www/okcupidlogo.png` stores the logo asset used in the dashboard landing page

Several derived variables and pattern flags are created in `global.R`, including:

- `religious_category`
- `horoscope_dismisser`
- `days_since`
- preset text-pattern indicators such as `winkyUsers` and `emotiUsers`

## Requirements

Install R and the following packages:

- `shiny`
- `shinydashboard`
- `ggplot2`
- `tm`
- `wordcloud`
- `gridExtra`
- `ggthemes`
- `rsconnect` for `shinyapps.io` deployment

Example install command:

```r
install.packages(c(
  "shiny",
  "shinydashboard",
  "ggplot2",
  "tm",
  "wordcloud",
  "gridExtra",
  "ggthemes",
  "rsconnect"
))
```

## Running the App

From the project directory, start the app with:

```r
shiny::runApp(".")
```

Or in a terminal:

```bash
R -e 'shiny::runApp(".")'
```

## Dashboard Views

The current dashboard includes seven views:

1. `Subset Description`
Overview page describing the OkCupid subset, important variables, and the project framing.

2. `Word Length Histogram`
Histogram of average essay word length with an optional density overlay and tunable smoothing.

3. `Age & Essay Length Scatterplot`
Sampled scatterplot of age versus average essay length, with an optional text-label view for sex and a fitted regression line.

4. `Religion & Age Density`
Faceted density plots of age grouped by simplified religion categories with an adjustable bandwidth control.

5. `Ethnicity Bar Chart`
Bar charts of ethnicity counts conditioned on `sex`, `status`, or `region`.

6. `Last Logged In Histogram`
Histogram and density display of `days_since`, with an optional rug plot for individual observations.

7. `Custom Word Mosaic Plot`
Mosaic plot connecting essay text patterns with a selected attribute such as `sex`, `religious_category`, or `horoscope_dismisser`.

## What Changed In The Current Build

Compared with the earlier version of the dashboard, the current app now reflects a more focused chart set and a more polished presentation:

- the sidebar has been simplified to the views that are still actively surfaced in the UI
- a new introduction page documents the subset and variables directly inside the app
- the religion view now shows age density by religion category rather than height
- the ethnicity chart now conditions on `status` instead of `orientation`
- the scatterplot uses a reproducible random sample and adds an optional text-label mode
- the custom mosaic plot focuses on preset emoticon-related patterns plus user-entered custom text
- the app now includes a logo asset in `www/` and more extensive dashboard styling

These are worth documenting because they change both what users see and how they should interpret the dashboard.

## Data Notes

- `vegan_dat.csv` is the main dataset used throughout the app
- `nonvegan_dat.csv` is retained for comparison-oriented analysis work in the project
- expected columns include fields such as `age`, `sex`, `status`, `orientation`, `ethnicity`, `religion`, `region`, `sign`, `last_online`, essay columns `essay0` through `essay9`, and summary fields such as `avgl`

## Deploying To shinyapps.io

1. Create a `shinyapps.io` account at <https://www.shinyapps.io/>.
2. In the `shinyapps.io` dashboard, create or view your account tokens.
3. In R, install `rsconnect` if you have not already:

```r
install.packages("rsconnect")
```

4. Authenticate your machine with your account values. You can get your token and secret from <https://www.shinyapps.io/admin/#/tokens> in your account:

```r
rsconnect::setAccountInfo(
  name = "YOUR_ACCOUNT_NAME",
  token = "YOUR_TOKEN",
  secret = "YOUR_SECRET"
)
```

5. From the project directory, deploy the app:

```r
rsconnect::deployApp(appDir = ".")
```

6. After the first deploy, `shinyapps.io` will return the application URL. Future updates can be pushed with the same `deployApp()` command from this folder.

If you prefer to deploy from a terminal, you can run:

```bash
R -e 'rsconnect::deployApp(appDir = ".")'
```

## Deployment Notes

- Keep `ui.R`, `server.R`, `global.R`, the CSV files, and the `www/` directory together in the deployed app directory.
- `shinyapps.io` installs packages listed in the app dependency scan, so `rsconnect` only needs to be installed locally for deployment.
- If deployment fails on missing packages, install them locally first and redeploy.
- The logo should remain at `www/okcupidlogo.png`; Shiny serves files in `www/` automatically.

## Notes

- The app starts successfully with the package set above.
- Running the app currently shows a warning about a missing `ggmap` namespace tied to `map_object`; it did not block startup in local testing, but it is worth double-checking before production deployment if that warning appears in your environment.
- `global.R` uses the deprecated `size` argument in `element_rect()` for the custom theme. This does not stop the app from running, but `linewidth` would be the modern `ggplot2` equivalent.
