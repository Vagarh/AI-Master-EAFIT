def validate_eda(df):
    if df is None:
        return False
    needed_cols = {"seq", "sst3", "sst8", "len", "has_nonstd_aa"}
    actual_cols = {c.lower() for c in df.columns}
    return needed_cols.issubset(actual_cols)
