curl --request POST "http://172.20.238.9:8086/api/v2/query?org=SEAT%20S.A." ^
  --header "Authorization: Token my-secret-token" ^
  --header "Accept: application/csv" ^
  --header "Content-type: application/vnd.flux" ^
  --data "from(bucket:\"my-bucket\") |> range(start: -24h) |> filter(fn: (r) => r._measurement == \"KEU2A21-----BS1---KFU1\")" > output.csv 