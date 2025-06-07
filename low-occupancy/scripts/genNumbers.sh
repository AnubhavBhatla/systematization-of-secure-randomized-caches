export BASE_DIR=/home/randomized_caches

cd aes/analysis/skew-2-ass64/

for i in {1..8}
do 
   bash run_key1_ass64.sh $i &
   sleep 5
   bash run_key2_ass64.sh $i &
   sleep 5
done

cd ../skew-2-ass128/

for i in {1..8}
do 
   bash run_key1_ass128.sh $i &
   sleep 5
   bash run_key2_ass128.sh $i &
   sleep 5
done
