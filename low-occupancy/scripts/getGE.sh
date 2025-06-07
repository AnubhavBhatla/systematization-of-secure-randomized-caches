mkdir -p results

cd aes/analysis/

FILE="ceaser/run.sh"
OLD_LINE="for j in {100..20000..1000}"
NEW_LINE="for j in {100..3000..100}"
sed -i "s%$OLD_LINE%$NEW_LINE%g" "$FILE"

FILE="mirage/run.sh"
sed -i "s%$OLD_LINE%$NEW_LINE%g" "$FILE"

FILE="sass/run.sh"
sed -i "s%$OLD_LINE%$NEW_LINE%g" "$FILE"

FILE="scatter/run.sh"
sed -i "s%$OLD_LINE%$NEW_LINE%g" "$FILE"

FILE="skew-2-ass64/run.sh"
sed -i "s%$OLD_LINE%$NEW_LINE%g" "$FILE"

FILE="skew-2-ass128/run.sh"
sed -i "s%$OLD_LINE%$NEW_LINE%g" "$FILE"

cd ceaser/
bash run.sh > ../../../results/GE_ceasers.txt

cd ../mirage/
bash run.sh > ../../../results/GE_mirage.txt

cd ../sass/
bash run.sh > ../../../results/GE_sass.txt

cd ../scatter/
bash run.sh > ../../../results/GE_scatter.txt

cd ../skew-2-ass64/
bash run.sh > ../../../results/GE_skew-2-ass64.txt

cd ../skew-2-ass128/
bash run.sh > ../../../results/GE_skew-2-ass128.txt