# French people outside France
French people living outside France as per government report 2024. <br>
- The countries with the highest population are Switzerland, the United States of America, 
the United Kingdom, Belgium, and Canada. <br>
- The change 2023/2022 is calculated on a country basis and might be misleading in the grander scale, 
only use European view.<br>
- For comparison, what is the population of France in 2023?<br>
- For better view, what is the population of other countries, including or exciting French people?<br>
In this project, we load table from PDF report, plot bar chart for population, and geo charts.

## Observations
- The current method to map the countries has some deficiencies because it requires manual translation 
from French to English (plus country name should be written in some expected way). For example, was not able to map 
the Czech Republic and Argentina. 
- Python package for reading tables from PDF has some issues. When the table is populated through multiple  
pages, the first row is not read at all. Manually addressed this entering the missing data.  

## Project structure
```
├── data                    # Input data (`pdf` and `pkl`)
├── src                     # Source files 
├── fig                     # Charts
├── requirements.txt        
├── LICENSE
└── README.md
```

## References
Download the report by French Government from and put into 'data' folder <br>
<a href="https://francais-du-monde.org/wp-content/uploads/2022/11/2024-gouvernement-francais-etranger-rapport.pdf">Rapport du gouvernement 2024 sur la situation des Français de l’étranger</a> <br>
see the section V. STATISTIQUES : FRANÇAIS INSCRITS AU REGISTRE 

Geographical charts plotted following notebook <br>
https://nbviewer.org/github/bast/altair-geographic-plots/blob/fc9c036/choropleth.ipynb

Data on world population come from
<ADD HERE>

Population 2023, World Bank Group, https://datacatalog.worldbank.org/home
This dataset is classified as Public under the Access to Information Classification Policy. 
Users inside and outside the Bank can access this dataset
Key health, nutrition and population statistics gathered from a variety of international sources.
Last Updated:07/01/2024
