
run: csparks.so
	python puma.py 

csparks.so: sparks/csparks.pyx
	cd sparks ; $(MAKE) $(MFLAGS)

