#nohup sh create_table.sh test_db_res.txt test_db_CUI_dict.txt > log.log &
master_input="$1"
dict_file="$2"

tail -n +2 $master_input | sed "s///g" | awk -F "|" '{print $1"|"$3}' | sed "s/:YES//g" | sed "s/:NO//g" | sed "s/:UNCLEAR//g" > test_db_res.txt.1
sort $dict_file | uniq -c | awk -F " " '{print $NF}' > dict_file_sorted.txt.1
  
srno=1
while read -r line
do
    name="$line"
    fil=${srno}.txt
    nfil=${srno}_nf.txt
    final=${srno}_final.txt
    f="$(echo "$name" | awk -F "|" '{print $1}')"
    echo "$name" | awk -F "|" '{print $2}' | tr ',' '\n' | sort -nk1,1 | uniq -c | awk -F " " '{print $NF}' > $fil    	
    grep -Fx -v -f $fil dict_file_sorted.txt.1 | sed "s/^/0|/g" > $nfil 
    echo "$name" | awk -F "|" '{print $2}' | tr ',' '\n' | sort -nk1,1 | uniq -c | awk -F " " '{print $(NF-1)"|"$NF}' > $fil
    cat $fil $nfil | sort -t "|" -nk2,2 | awk -F "|" '{print $1}' | cut -f1 | paste -s -d "|" | sed "s/^/${f}|/g"> $final 
    srno=$((srno + 1))
    rm -rf $fil
    rm -rf $nfil
    #break 
done < test_db_res.txt.1

cut -f1 dict_file_sorted.txt.1 | paste -s -d "|" | sed "s/^/file_name|/g" > first_column_dict
cat first_column_dict *_final.txt > final_data.txt
