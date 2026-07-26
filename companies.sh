#!/bin/bash

CSV_URL="https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"

OUTPUT_CSV="companies_sorted.csv"
OUTPUT_TXT="companies_sorted.txt"

curl -s "$CSV_URL" |
awk -F',' '
BEGIN {
    OFS=","
}
NR>1{

    company=$2
    location=$6
    year=$7

    if(match(year,/[0-9]{4}/))
        year=substr(year,RSTART,RLENGTH)
    else
        year="Unknown"

    print year,company,location
}
' |
sort -t',' -k1,1n > "$OUTPUT_CSV"

{
printf "%-6s | %-45s | %s\n","Year","Company","Location"
printf "-------------------------------------------------------------------------------\n"

awk -F',' '
{
printf "%-6s | %-45s | %s\n",$1,$2,$3
}
' "$OUTPUT_CSV"

} > "$OUTPUT_TXT"

echo "Saved:"
echo "  $OUTPUT_CSV"
echo "  $OUTPUT_TXT"