#-----------------------------------------------------------------------------
# File          : Makefile
# Author        : Wei Song  <wsong83@gmail.com>
# Created       : 13.09.2015
# Last modified : 13.09.2015
#-----------------------------------------------------------------------------
# Description :
# A GNU Make makefile to generate a shared library
#-----------------------------------------------------------------------------
# Copyright (c) 2015 by Wei Song
# License: BSD
#          See LICENSE for more details.
#------------------------------------------------------------------------------
# Modification history :
# 13.09.2015 : created
#-----------------------------------------------------------------------------

default: all
.PHONY: default all

#--------------------------------------------------------------------
# Build rules
#--------------------------------------------------------------------
CXX = g++
CXX_CFLAGS = -Iinclude -o3 -fPIC -Wall
AR = ar

#--------------------------------------------------------------------
# Build
#--------------------------------------------------------------------
TARGETS = \
	generator \
	uniform_generator \
	poisson_generator \
	normal_generator \
	natural_generator \

TARGET_OBJS = $(addsuffix .o, $(TARGETS))

$(TARGET_OBJS): %.o:src/%.cpp include/random_generator.h
	$(CXX) $(CXX_CFLAGS) -c $< -o $@

librandomgen.so: $(TARGET_OBJS)
	$(CXX) -shared -o $@ $^ -lc

librandomgen.a: $(TARGET_OBJS)
	$(AR) rvs $@ $^

all: librandomgen.so librandomgen.a

junk += $(TARGET_OBJS) librandomgen.so librandomgen.a

#--------------------------------------------------------------------
# test
#--------------------------------------------------------------------
TEST_TARGET = \
	test_uniform \
	test_poisson \
	test_normal \
	test_natural \

TEST_LINK_FLAGS = -L. -lrandomgen

test_generator.o : test/test_generator.cpp test/test_generator.h include/random_generator.h
	$(CXX) $(CXX_CFLAGS) -std=c++11 -c $< -o $@

$(TEST_TARGET): %:test/%.cpp test_generator.o librandomgen.so
	$(CXX) $(CXX_CFLAGS) $< test_generator.o $(TEST_LINK_FLAGS) -o $@

test: $(TEST_TARGET)

.PHONY: test
junk += $(TEST_TARGET) test_generator.o

#--------------------------------------------------------------------
# clean up
#--------------------------------------------------------------------

clean:
	rm -rf $(junk)

.PHONY: clean

