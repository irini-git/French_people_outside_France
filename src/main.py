from data_manager import ReportData

# Initiate class and load data
report = ReportData()

# Explore data via visualizations
# report.explore_data()
# report.plot_geo_distribution()

# Enrich data with global information
report.enrich_with_global_data()

# END ----------------