
cd tmp
\rm -R *
cd ..

cd src

python cvfeatures.py -h 

echo "test runs below: "

# python cvfeatures.py -i ../imgs/6336682747_a3221c47a5_m.jpg -o ../tmp -v 3

# python cvfeatures.py -i ../imgs/61/6132418346_5853b5b126.jpg -o ../tmp -v 3

# python cvfeatures.py -i ../imgs/63/6305774532_f59b8bf71c.jpg -o ../tmp -v 3

python cvfeatures.py -i ../imgs/ -o ../tmp -v 1