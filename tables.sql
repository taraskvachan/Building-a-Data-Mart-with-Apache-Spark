# ClickHouse

CREATE TABLE visits
(
    visitid Int32,
    visitDateTime DateTime,
    URL String,
    duration Int32,
    clientID Int32,
    source String,
    UTMCampaign String,
    params String
)
ENGINE = MergeTree
ORDER BY visitDateTime;


# Postgres

create table costs(
    date date,
    campaign_id int,
    costs float,
    clicks int,
    views int
)
