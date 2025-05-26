rm *.pdf
mkdir -p report

OPTION=($1)

for i in {3..14}; do
    echo "============================================================"
    echo "Fetching figure $i..."
    python3 get-figure.py "$OPTION" "$i"
    echo "============================================================"
done

for i in {18..19}; do
    echo "============================================================"
    echo "Fetching figure $i..."
    python3 get-figure.py "$OPTION" "$i"
    echo "============================================================"
done
