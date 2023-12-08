
import pandas as pd

def prepare_data(df):
    overview = df[["date", "total_revenue"]].groupby(["date"], as_index=False).sum().sort_values(by=["date"])
    count_invoices = df[["date", "invoice"]].drop_duplicates().groupby(["date"], as_index=False).count().sort_values(by=["date"])
    total_invoices = df[["date", "invoice"]].groupby(["date"], as_index=False).count().sort_values(by=["date"])
    count_content = df[["date", "stream_id"]].drop_duplicates().groupby(["date"], as_index=False).count().sort_values(by="date")
    merged_df = overview.merge(count_invoices, on=["date"], how="inner")
    merged_df = merged_df.merge(total_invoices, on=["date"], how="inner")
    merged_df = merged_df.merge(count_content, on=["date"], how="inner")
    merged_df.columns = ["Date", 'Total Revenue', "Total Unique invoices", "Total Invoice Items", "# Of Unique Content Streamed"]
    merged_df["Average items per invoice"] = merged_df.apply(lambda x: x["Total Invoice Items"] / x["Total Unique invoices"], axis=1)
    return merged_df

def prepare_data_by_country(df, country=None):
    if country:
        if country not in df["country"].unique():
            raise Exception("Not a valid country name")
    overview = df[["date", "country", "total_revenue"]].groupby(["date", "country"], as_index=False).sum().sort_values(by=["date"])
    count_invoices = df[["date", "country", "invoice"]].drop_duplicates().groupby(["date", "country"], as_index=False).count().sort_values(by=["date"])
    total_invoices = df[["date", "country", "invoice"]].groupby(["date", "country"], as_index=False).count().sort_values(by=["date"])
    count_content = df[["date", "country", "stream_id"]].drop_duplicates().groupby(["date", "country"], as_index=False).count().sort_values(by="date")
    merged_df = overview.merge(count_invoices, on=["date", "country"], how="inner")
    merged_df = merged_df.merge(total_invoices, on=["date", "country"], how="inner")
    merged_df = merged_df.merge(count_content, on=["date", "country"], how="inner")
    merged_df.columns = ["Date", 'Country', 'Total Revenue', "Total Unique invoices", "Total Invoice Items", "# Of Unique Content Streamed"]
    merged_df["Average items per invoice"] = merged_df.apply(lambda x: x["Total Invoice Items"] / x["Total Unique invoices"], axis=1)
    if country:
        return merged_df[merged_df["Country"] == country]
    return merged_df

def train_test_split(df, split=0.7):
    n = int(len(df)*split)
    train = df[df.index < n]
    test = df[df.index >= n]
    train.index = train["Date"]
    test.index = test["Date"]
    return train, test