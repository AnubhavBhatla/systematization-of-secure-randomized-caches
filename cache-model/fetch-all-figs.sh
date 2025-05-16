rm *.pdf
mkdir report
for i in {3..14}; do
    echo "============================================================"
    echo "Fetching figure $i"
    python3 get-figure.py 0 "$i"
    echo "============================================================"
done
