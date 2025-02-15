# Technical specs

Data Mart Tables:
<ol>
<li>customer_detailed</li>
<li>campaigns_agg</li>
<li>dates_agg</li>
</ol>

## 1. Attributive composition

### customer_detailed table

| #  | Column name | Data type    | Description                                                   |
|----|------------------|---------------|------------------------------------------------------------|
| 1  | dt               | string        | Date of visit                                                |
| 2  | visit_id         | string        | Visit ID                                       |
| 3  | client_id        | string        | Client ID                                      |
| 4  | url              | string        | Page URL                                               |
| 5  | duration         | integer       | Time on site in seconds                                 |
| 6  | source           | string        | The type of source from which the user came to the site    |
| 7  | utmcampaign      | string        | Adv campaign name                               |
| 8  | event_type       | string        | Event type                                               |
| 9  | event_id         | integer       | Event ID                                     |
| 10 | submit_id        | long        | Submit ID                                     |
| 11 | name             | string        | Client name                                                |
| 12 | phone            | string        | Phone number                                         |
| 13 | phone_plus       | string        | Phone number with a plus (+) sign                              |
| 14 | phone_md5        | string        | Phone number hashed with md5 algorithm             |
| 15 | phone_plus_md5   | string        | Phone number with a plus (+) sign, hashed with md5 algorithm |
| 16 | deal_id          | long        | Deal ID                                      |
| 17 | deal_date        | string        | Deal date                                              |
| 18 | fio              | string        | Client's full name                                               |
| 19 | phone_deal       | string        | Phone from the deal table                  |
| 20 | email            | string        | Email                                          |
| 21 | address          | string        | Residential address                                     |
| 22 | username         | string        | Username from email                     |
| 23 | domain           | string        | Email domain                                    |
| 24 | campaign_name    | string        | Adv campaign name                               |
| 25 | campaign_duration| string        | Duration of the adv campaign                         |
| 26 | costs            | decimal(19,2) | Advertising expenses                                         |
| 27 | clicks           | long        | Clicks                                          |
| 28 | views            | long        | Views                                      |

### campaigns_agg table

| №#  | Column name | Data type    | Description                                   |
|----|------------------|---------------|--------------------------------------------|
| 1  | campaign_name    | string        | Adv campaign name               |
| 2  | unique_visits    | long        | Visits                         |
| 3  | unique_clients   | long        | Unique clients            |
| 4  | unique_submits   | long        | Submits                           |
| 5  | unique_deals     | long        | Deals                          |
| 6  | total_costs      | decimal(19,2) | Total adv expenses          |
| 7  | total_clicks     | long        | Total clicks                         |
| 8  | total_views      | long        | Total views                    |
| 9  | total_duration   | long        | Total duration of visits in seconds |
| 10 | avg_deal_cost    | decimal(19,2) | Average deal cost                     |

### dates_agg table

| #  | Column name | Data type    | Description                                   |
|----|------------------|---------------|--------------------------------------------|
| 1  | month            | string        | Month by expenses                          |
| 2  | unique_visits    | long        | Visits                        |
| 3  | unique_clients   | long        | Unique clients             |
| 4  | unique_submits   | long        | Submits                          |
| 5  | unique_deals     | long        | Deals                           |
| 6  | total_costs      | decimal(19,2) | Total adv expenses           |
| 7  | total_clicks     | long        | Total clicks                        |
| 8  | total_views      | long        | Total views                     |
| 9  | total_duration   | long        | Total duration of visits in seconds|
| 10 | avg_deal_cost    | decimal(19,2) | Average deal cost                        |

## 2. Sources

| № | Storage location | Schema          | Table | Description                                               |
|---|----------------|----------------|---------|--------------------------------------------------------|
| 1 | ClickHouse     | public      | visits  | Visits of site users                  |
| 2 | Postgres       | public         | costs   | Advertising costs                                    |
| 3 | csv            | -              | -       | Dict with comparison of adv campaigns           |
| 4 | HDFS           | website_events | submits | Completed forms on the website for submitting an application/callback |
| 5 | HDFS           | system_events  | deals   | Ordered design projects                             |

## 3. Methodology

### visits (ClickHouse)

```
with filtered_step1 as (
    select
        visitDateTime::date as dt,
        visitid,
        clientID,
        URL,
        duration,
        source,
        UTMCampaign,
        params,
        replaceRegexpAll(params, '\[|\]', '') as params_regex,
        splitByString(', ', replaceRegexpAll(params, '\[|\]', '')) as params_split
    from marketing.visits
    where visitDateTime >= '2024-01-01' and visitDateTime < '2025-01-28'
    and source in ('ad', 'direct')
    and (
        match(URL, '.*checkout.*') or
        match(URL, '.*add.*') or
        match(URL, '.*home.*') or
        match(URL, '.*contact.*') or
        match(URL, '.*top50.*') or
        match(URL, '.*customer-service.*') or
        match(URL, '.*wishlist.*') or
        match(URL, '.*sale.*') or
        match(URL, '.*best-sellers.*') or
        match(URL, '.*view.*') or
        match(URL, '.*discount.*') or
        match(URL, '.*featured.*') or
        match(URL, '.*new-arrivals.*') or
        match(URL, '.*settings.*') or
        match(URL, '.*return-policy.*') or
        match(URL, '.*edit.*') or
        match(URL, '.*delete.*') or
        match(URL, '.*reviews.*') or
        match(URL, '.*products.*') or
        match(URL, '.*about.*')
    )
),
filtered_step2 as (
    select *,
    replaceAll(params_split[1], '\'', '') as event_type,
    toInt32OrNull(params_split[2]) as event_id
    from filtered_step1
)
select
    dt,
    visitid,
    clientID,
    URL,
    duration,
    source,
    UTMCampaign,
    event_type,
    event_id
from filtered_step2
where event_type = 'submit';
```

### costs (Postgres)

```
select
    date,
    campaign_id,
    round(sum(costs)::numeric, 2) as costs,
    sum(clicks) as clicks,
    sum(views) as views
from public.costs
group by date, campaign_id
order by date, campaign_id;
```

### campaigns_dict (Spark SQL)

```
campaigns_dict = spark.read.option('header', True).csv('campaigns_dict.csv')
campaigns_dict.createOrReplaceTempView('campaigns_dict_view')
campaigns_dict = spark.sql("""
    select
        campaign_id,
        campaign_name,
        case
            when campaign_name like 'year%' then 'Год'
            when campaign_name like 'quarter%' then 'Квартал'
            when campaign_name like 'month%' then 'Месяц'
            else null
        end as campaign_duration
    from campaigns_dict_view
""")	
```

### submits (Spark SQL)

```
submits = spark.sql("""
    SELECT
        submit_id,
        name,
        CAST(phone AS STRING) AS phone,
        CONCAT('+', phone) AS phone_plus,
        MD5(CAST(phone AS STRING)) AS phone_md5,
        MD5(CONCAT('+', phone)) AS phone_plus_md5
    FROM website_events.submits
""")
```

### deals (pandas)

```
deals_pdf = spark.table('system_events.deals').toPandas()
deals_pdf[['username', 'domain']] = deals_pdf['email'].str.split('@', expand=True)
filtered_deals_pdf = deals_pdf[deals_pdf['domain'].isin(['example.com', 'example.org', 'example.net'])]
```

## 4. Logic of creating our Data Mart

Legend:
<ol>
<li>purple - sources</li>
<li>turquoise - intermediate tables</li>
<li>maroon - cleaned and prepared dataframes</li>
<li>blue - join conditions</li>
<li>green - final tables</li>
</ol>

![5](https://github.com/user-attachments/assets/3a7475d0-1026-4996-b86b-fce62ebb7db9)

