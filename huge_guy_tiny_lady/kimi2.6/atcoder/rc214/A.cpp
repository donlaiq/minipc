#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  
  int N;
  cin >> N;
  vector<string> S(N);
  for(int i = 0; i < N; ++i) cin >> S[i];
  
  int M = 2 * N - 1;        // number of anti-diagonals
  vector<int> val(M, -1);   // -1 means still unknown
  
  for(int i = 0; i < N; ++i) {
    for(int j = 0; j < N; ++j) {
      char c = S[i][j];
      if(c != '?') {
        int d = c - '0';
        int k = i + j;
        if(val[k] == -1) {
          val[k] = d;
        } else if(val[k] != d) {
          cout << -1 << '\n';
          return 0;
        }
      }
    }
  }
  
  vector<string> ans = S;
  for(int i = 0; i < N; ++i) {
    for(int j = 0; j < N; ++j) {
      int k = i + j;
      if(ans[i][j] == '?') {
        int d = (val[k] == -1 ? 0 : val[k]);
        ans[i][j] = char('0' + d);
      }
    }
  }
  
  for(int i = 0; i < N; ++i) {
    cout << ans[i] << '\n';
  }
  return 0;
}
