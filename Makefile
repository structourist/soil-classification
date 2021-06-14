VPATH=bin:out:site

build: build-csv build-json build-hugo
	echo hello

content: site soil.json
	# cp src/config.toml site/
	python scripts/site.py ./out/soil.json ./site/content
	cd site && ../bin/hugo --quiet

site: hugo
	mkdir -p site
	./bin/hugo --quiet new site site > /dev/null
	rmdir site/content
	mkdir -p site/themes
	git submodule add --force  https://github.com/beaucronin/hugo-eureka.git site/themes/eureka
	mkdir -p site/config/_default
	cp src/config/_default/* site/config/_default
	rm site/config.toml

soil.json: out
	python scripts/airtable_json.py
	mv soil.json out

out:
	mkdir -p out	

hugo: bin
	wget https://github.com/gohugoio/hugo/releases/download/v0.83.1/hugo_0.83.1_macOS-64bit.tar.gz -O hugo.tar.gz
	tar xzf hugo.tar.gz
	rm hugo.tar.gz
	chmod a+x hugo
	mv hugo bin
	touch bin/hugo

bin:
	mkdir -p bin

clean: clean-out clean-site

clean-out:
	rm -rf out

clean-site:
	rm -rf site

clean-content:
	rm -rf site/content