PREFIX=/usr/local
DESTDIR=

destdir=$(DESTDIR)$(PREFIX)
sharedir=$(destdir)/share

OPENDICT_DIR=$(sharedir)/opendict/dictionaries/plain

BUILD_DATE := $(shell dpkg-parsechangelog -ldebian/changelog --show-field Date)

all: mueller7.dict.dz mueller7accent.dict.dz

%.dict.dz: %.dict
	# Ensure deterministic mtime for dictzip to inherit
	touch --date='$(BUILD_DATE)' $^
	dictzip -k $^

mueller7accent.dict: mueller7accent.data
	sh debian/scripts/df.sh $^ " (with accents)"

mueller7.dict: mueller7.data
	sh debian/scripts/df.sh $^ ""

mueller7accent.data: Mueller7accentGPL.koi
	python3 debian/scripts/to-dict.py $^ > $@

mueller7.data: Mueller7GPL.koi
	python3 debian/scripts/to-dict.py $^ > $@

clean:
	rm -f *.data *.dict *.dict.dz *.index

install:
	install -d -m 0755 $(sharedir)/dictd
	install -m 0644 *.dict.dz *.index $(sharedir)/dictd

	for i in mueller7 mueller7accent; do \
		install -d -m 0755 $(OPENDICT_DIR)/$$i.dict.dz; \
		install -d -m 0755 $(OPENDICT_DIR)/$$i.dict.dz/conf; \
		install -d -m 0755 $(OPENDICT_DIR)/$$i.dict.dz/file; \
		ln -s ../../../../../dictd/$$i.dict.dz \
			$(OPENDICT_DIR)/$$i.dict.dz/file/$$i.dict.dz; \
		ln -s ../../../../../dictd/$$i.index \
			$(OPENDICT_DIR)/$$i.dict.dz/file/$$i.index; \
		cp debian/$$i-dict.xml \
			$(OPENDICT_DIR)/$$i.dict.dz/conf/config.xml; \
	done
