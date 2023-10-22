def prepare_data(df):
    overview = df[["date", "country", "total_revenue"]].groupby(["date", "country"], as_index=False).sum().sort_values(by=["date"])
    count_invoices = df[["date", "country", "invoice"]].drop_duplicates().groupby(["date", "country"], as_index=False).count().sort_values(by=["date"])
    total_invoices = df[["date", "country", "invoice"]].groupby(["date", "country"], as_index=False).count().sort_values(by=["date"])
    count_content = df[["date", "country", "stream_id"]].drop_duplicates().groupby(["date", "country"], as_index=False).count().sort_values(by="date")
    merged_df = overview.merge(count_invoices, on=["date", "country"], how="inner")
    merged_df = merged_df.merge(total_invoices, on=["date", "country"], how="inner")
    merged_df = merged_df.merge(count_content, on=["date", "country"], how="inner")
    merged_df.columns = ["Date", 'Country', 'Total Revenue', "Total Unique invoices", "Total Invoice Items", "# Of Unique Content Streamed"]
    merged_df["Average items per invoice"] = merged_df.apply(lambda x: x["Total Invoice Items"] / x["Total Unique invoices"], axis=1)
    return merged_df
