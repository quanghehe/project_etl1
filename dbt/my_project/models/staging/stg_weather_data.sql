{{ config(
    materialized='table',
    unique_key='id'
) }}

with source as (

select * from {{source('wt','raw_weather_data')}}
),

dedupe as (
    select * ,
    row_number() over(partition by time order by inserted_at) as rm
    from source
)

select 
    id ,
    city,
    temperature,
    weather_description,
    wind_speed,
    time as weather_time_local,
    (inserted_at + (utc_offset || 'hours')::interval) as inserted_at_local
    from dedupe
    where rm = 1
