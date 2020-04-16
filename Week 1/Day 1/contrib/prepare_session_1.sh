#!/bin/bash

wget https://github.com/CGAL/cgal/releases/download/releases/CGAL-4.14.1/CGAL-4.14.1.tar.xz \
    && tar -xf CGAL-4.14.1.tar.xz \
    && cd CGAL-4.14.1 && cmake -DCMAKE_BUILD_TYPE=Release && make -j4 && cd .. && rm CGAL-4.14.1.tar.xz

cd cxx && g++ -o voronoi_1 voronoi_1.cpp -I../CGAL-4.14.1/include -lCGAL -lgmp -std=c++11

