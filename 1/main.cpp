#include <iostream>
#include <fstream>
#include <cstdlib>
#include <cmath>
#include "args_serializer.h"

int main(int argc, char const *argv[]) {
  std::ofstream fout;

  helper::serialize::map(argc, argv)
  .handle("out", [&] (const helper::serialize::values &values, const std::string &error) {
    for (auto& filename: values) {
      fout.open(filename);
      if (fout.is_open()) break;
    }
  });

  if (!fout.is_open()) {
    std::cout << "please, set output file by inline command `out=%filename%`" << std::endl;
    return 1;
  }

  std::srand(time(NULL));

  std::list<size_t> counters = {10, 100, 1000, (size_t)1e+6};

  //Classic
  if (!counters.empty())
    fout << "n\tP(A)\tP^(A)\tdP(A)\tsigma\n" << "Classic task" << std::endl;

  double P = 6. * 5. * 4. * 3. * 2. * 1. / (6. * 6. * 6. * 6. * 6. * 6.);
  for (size_t n: counters) {
    double nA = 0;
    double sum = 0;
    std::list<size_t> NA;
    for (size_t i = 0; i < n; ++i) {
      int x1, x2, x3, x4, x5, x6;
      x1 = std::rand() % 6;
      x2 = std::rand() % 6;
      x3 = std::rand() % 6;
      x4 = std::rand() % 6;
      x5 = std::rand() % 6;
      x6 = std::rand() % 6;
      if (x1 != x2 && x1 != x3 && x1 != x4 && x1 != x5 && x1 != x6 &&
          x2 != x3 && x2 != x4 && x2 != x5 && x2 != x6 &&
          x3 != x4 && x3 != x5 && x3 != x6 &&
          x4 != x5 && x4 != x6 &&
          x5 != x6)
        ++nA;
      sum += nA;
      NA.emplace_back(nA / (i+1.));
    }
    double dsum = 0;
    double pA = nA / n;
    for (size_t val: NA)
      dsum += (val - pA/n) * (val - pA/n);
    double sigma = std::sqrt(dsum / (n - 1));
    fout << n << "\t" << P << "\t" << pA << "\t" << P - pA << "\t" << sigma << std::endl;
  }

  // Geometry

  if (!counters.empty())
    fout << "Geometry task" << std::endl;

  P = 0.25;
  for (size_t n: counters) {
    double nA = 0;
    double sum = 0;
    std::list<size_t> NA;
    for (size_t i = 0; i < n; ++i) {
      double t1, t2;
      t1 = std::rand() * 1. / RAND_MAX;
      t2 = std::rand() * 1. / RAND_MAX;
      if (t1 > t2) std::swap(t1, t2);
      t2 -= t1;

      if (t1 < (t2 + (1 - (t1 + t2))) &&
          t2 < (t1 + (1 - (t1 + t2))) &&
          (1 - (t1 + t2)) < t1 + t2)
        ++nA;
      sum += nA;
      NA.emplace_back(nA / (i+1.));
    }
    double dsum = 0;
    double pA = nA / n;
    for (size_t val: NA)
      dsum += (val - pA/n) * (val - pA/n);
    double sigma = std::sqrt(dsum / (n - 1));
    fout << n << "\t" << P << "\t" << pA << "\t" << P - pA << "\t" << sigma << std::endl;
  }

  return 0;
}
