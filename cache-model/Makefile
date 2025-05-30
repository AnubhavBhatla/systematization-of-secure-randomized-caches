
MAKE = make
CXX = g++
CXXFLAGS = --std=c++11 -O2 -g -I. -fPIC

TARGETS = \
	test/cache-test \
	test/test-eviction-tar-ran \
	test/evset-effective \
	test/evset-attack \
	test/evset-attack-ppp \
	test/evset-effective-warmup \
	test/evset-attack-warmup \

OBJECTS = \
	cache/cache.o \
	cache/replace.o \
	cache/monitor.o \
	attack/search.o \
	attack/create.o \
	attack/traverse.o \
	util/statistics.o \
	util/query.o \
	util/random.o \
	util/report.o \
	util/detector.o \
	util/cache_config_parser.o \
	util/traverse_config_parser.o \

HEADERS = $(wildcard cache/*.hpp) $(wildcard attack/*.hpp) $(wildcard util/*.hpp)

all: $(TARGETS) libcache_model.a

datagen/librandomgen.a:
	$(MAKE) -C datagen $(filename $@)

$(OBJECTS): %.o:%.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(TARGETS): test/% : test/%.cpp $(OBJECTS) test/common.hpp datagen/librandomgen.a
	$(CXX) $(CXXFLAGS) $^ -o $@

libcache_model.a: cache/replace.o cache/cache.o cache/monitor.o util/query.o util/random.o util/report.o util/detector.o util/cache_config_parser.o util/traverse_config_parser.o
	ar rvs $@ $^

clean:
	-rm $(TARGETS) $(OBJECTS) libcache_model.*
