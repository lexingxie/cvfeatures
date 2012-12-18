
cd tmp
\rm -R *
cd ..

cd src

python cvfeatures.py -h 

echo "test runs below: "

python cvfeatures.py -i ../imgs/6336682747_a3221c47a5_m.jpg -o ../tmp -v 3

python cvfeatures.py -i ../imgs/ -o ../tmp -v 2