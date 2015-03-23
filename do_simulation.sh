for i in `seq 15 5 100`;
do
	./sim.py 1000 "$i" True False False
done
