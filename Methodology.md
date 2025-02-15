# Technical specs

Data Mart Tables:
<ol>
<li>customer_detailed</li>
<li>campaigns_agg</li>
<li>dates_agg</li>
</ol>

## Attributive composition

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
| 12 | phone            | string        | Phone                                          |
| 13 | phone_plus       | string        | Phone with a + sign                              |
| 14 | phone_md5        | string        | Phone hashed with md5 algorithm             |
| 15 | phone_plus_md5   | string        | Phone with + sign, hashed with md5 algorithm |
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
