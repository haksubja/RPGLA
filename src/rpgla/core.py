import polars as pl

def calculate_divines_per_mirror(df: pl.LazyFrame, league_name: str) -> pl.DataFrame:
    """
    Calculates the daily cost of a Mirror of Kalandra in Divine Orbs.
    """
    # 1. Filter for our specific league and remove low-confidence data
    league_data = df.filter(
        (pl.col("League") == league_name) & 
        (pl.col("Confidence") != "Low")
    )
    
    # 2. Extract Mirror prices in Chaos Orbs
    mirrors = league_data.filter(
        (pl.col("Get") == "Mirror of Kalandra") & (pl.col("Pay") == "Chaos Orb")
    ).select(
        pl.col("Date"),
        pl.col("Value").alias("Mirror_in_Chaos")
    )
    
    # 3. Extract Divine prices in Chaos Orbs
    divines = league_data.filter(
        (pl.col("Get") == "Divine Orb") & (pl.col("Pay") == "Chaos Orb")
    ).select(
        pl.col("Date"),
        pl.col("Value").alias("Divine_in_Chaos")
    )
    
    # 4. Join the two tables on 'Date' and calculate the ratio
    ratio_df = mirrors.join(divines, on="Date", how="inner").with_columns(
        (pl.col("Mirror_in_Chaos") / pl.col("Divine_in_Chaos"))
        .round(2) # Round to 2 decimal places for cleaner output
        .alias("Divines_per_Mirror")
    ).select("Date", "Divines_per_Mirror").sort("Date")
    
    # 5. collect() executes the lazy plan and brings the final tiny table into memory
    return ratio_df.collect()