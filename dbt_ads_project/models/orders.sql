select
  cast(order_id as bigint) as order_id,
  cast(customer_id as bigint) as customer_id,
  cast(amount as double) as amount,
  cast(order_date as date) as order_date
from {{ ref('orders_seed') }}
