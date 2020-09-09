all:
	cp README.md rpki-vrp-checker.7.ronn
	ronn -r --pipe rpki-vrp-checker.7.ronn > rpki-vrp-checker.7
	rm rpki-vrp-checker.7.ronn

clean:
	rm -rf *.egg *.egg-info dist build
