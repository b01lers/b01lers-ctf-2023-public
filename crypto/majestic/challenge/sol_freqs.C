#include <fstream>
#include <iostream>
#include <set>

const int N = 128;

typedef unsigned long long int u64;
typedef long long int i64;

i64 randbytes(int n) {
  std::ifstream f("/dev/urandom");
  i64 res = 0;
  f.read((char*) &res, n);
  return res;
}

struct Key {
  double A, B;
  int p, q;

  Key(double _A, double _B, int _p, int _q) : A(_A), B(_B), p(_p), q(_q) {}
  ~Key() {}
};


double f(double z, const Key& key) {
  for (i64 i = 0; i < key.p; ++i) z = key.A * z * (1 - z);
  for (i64 i = 0; i < key.q; ++i) z = key.B * z * (1 - z);
  return z;
}

int g(int b, const Key& key) {
  return int(f(0.5 / (N + 1) * (b + 1), key) * 256);
}

int enc1(int b, const Key& key) {
  return (g(b, key) << 8) + g(b ^ 0xbc, key);
}

Key keygen(int p, int q) {
  const double A0 = 3.95;
  while (true) {
    double A = A0 + randbytes(4) * 1e-11;
    double B = A0 + randbytes(4) * 1e-11;
    Key key(A, B, p, q);
    std::set<int> taken;
    for (int k = 0; k < N; ++k) {
       int c = enc1(k, key);
       if (taken.find(c) != taken.end()) break;
       taken.insert(c);
    }
    if (taken.size() == N) return key;
  }
}


void getFreqs(i64 p, i64 q, int n) {
  //std::cout.precision(18);
  // counts[256*i + j] gives number of times i->j was in generated map
  int counts[256 * 256]; 
  for (int i = 0; i < 256*256; ++i) counts[i] = 0;
  for (int i = 0; i < n; ++i) {
    Key K = keygen(p, q);
    // update counts
    for (int k = 0; k < 256; ++k) counts[k*256 + g(k, K)]++;
    //std::cout << i << ": " << K.A << ' ' << K.B << ' ' << K.p << ' ' << K.q << '\n';
    // progress indicator
    if ((i % 10000) == 0) std::cerr << '.';
  }

  // dump result
  // for each input byte list frequencies of output bytes
  for (int k = 0; k < 256; ++k) {
    std::cout << k << ":";
    for (int n = 0; n < 256; ++n) std::cout << ' ' << counts[k*256 + n];
    std::cout << '\n';
  }
}



int main(int argc, const char** const argv) {

  const int p = (argc > 1) ? atoi(argv[1]) : 3;
  const int q = (argc > 2) ? atoi(argv[2]) : 7;
  const int Nruns = (argc > 3) ? atoi(argv[3]) : 1000000;

  std::cout << "# p=" << p << " q=" << q << " Nruns=" << Nruns << '\n';

  getFreqs(p, q, Nruns);

  return 0;
}


