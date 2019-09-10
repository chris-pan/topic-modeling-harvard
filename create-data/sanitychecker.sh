NUM=$1

tail -n +2 test_db_res.txt | sed "s///g" | sed "${NUM}q;d" | awk -F "|" '{print $3}' | sed "s/:YES//g" | sed "s/:NO//g" | sed "s/:UNCLEAR//g" | tr ',' '\n' | sort | uniq -c | awk -F " " '{print $(NF-1)"|"$NF}' > f.1

tail -n +2 test_db_res.txt | sed "s///g" | sed "${NUM}q;d" | awk -F "|" '{print $3}' | sed "s/:YES//g" | sed "s/:NO//g" | sed "s/:UNCLEAR//g" | tr ',' '\n' | sort | uniq -c | awk -F " " '{print $NF}' > f.2

grep -Fx -v -f f.2 dict_file_sorted.txt.1 | sed 's/^/0|/g' > f.3

cat f.1 f.3 | sort -t "|" -nk2,2 | awk -F "|" '{print $1}' | tr '\n' '|' > f.4

cat ${NUM}_final.txt | cut -d "|" -f2-161652 > f.5

#diff f.4 f.5 
