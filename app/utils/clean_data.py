import pandas as pd
#write all of the above cells into one file
def clean_data(df):
    df["stream_id"] = df["stream_id"].fillna(df["StreamID"])
    df["total_price"] = df["total_price"].fillna(df["price"])
    df["times_viewed"] = df["times_viewed"].fillna(df["TimesViewed"])
    df["date"] = pd.to_datetime(df[["day", "month", "year"]])
    df = df.drop(["StreamID", "TimesViewed", "price", "day"], axis=1)
    #compute total revenue
    df["total_revenue"] = df.apply(lambda x: x["total_price"], axis=1)

    #fix missing customer ids
    max_id = df["customer_id"].max()
    users = df[["invoice", "customer_id"]]
    ids_per_invoice = users.drop_duplicates().groupby(["invoice"]).count().sort_values(by=["customer_id"], ascending=False)
    missing_ids = len(ids_per_invoice[ids_per_invoice["customer_id"]==0])
    unique_invoices = df['invoice'].unique()
    existing_customer_ids = df['customer_id'].dropna().unique()
    new_customer_ids = [max_id+i for i in range(1, len(unique_invoices) + 1)]
    invoice_to_int_mapping = {invoice: new_id for invoice, new_id in zip(unique_invoices, new_customer_ids)}

    # Fill missing "customer_id" values using the mapping
    df['customer_id'] = df['invoice'].map(invoice_to_int_mapping)
    return df
