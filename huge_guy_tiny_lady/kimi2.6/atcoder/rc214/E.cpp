#include <bits/stdc++.h>
using namespace std;

struct Fenwick {
    int n;
    vector<int> bit;
    Fenwick(int n = 0) { init(n); }
    void init(int n_) {
        n = n_;
        bit.assign(n + 1, 0);
    }
    void add(int idx, int val) {
        for (; idx <= n; idx += idx & -idx) bit[idx] += val;
    }
    int sum(int idx) const {
        int s = 0;
        for (; idx > 0; idx -= idx & -idx) s += bit[idx];
        return s;
    }
};

struct Event {
    int X, Y, idx, sign;
    bool operator<(Event const& other) const {
        return X < other.X;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    const int MAXV = 300000;               // ≤ sum of N
    vector<vector<int>> posA(MAXV + 1), posB(MAXV + 1);
    vector<int> used;
    used.reserve(MAXV);
    vector<int> A, B, P;

    while (T--) {
        int N;
        long long K;
        cin >> N >> K;
        A.assign(N + 1, 0);
        B.assign(N + 1, 0);
        used.clear();

        for (int i = 1; i <= N; ++i) {
            cin >> A[i];
            if (posA[A[i]].empty()) used.push_back(A[i]);
            posA[A[i]].push_back(i);
        }
        for (int i = 1; i <= N; ++i) {
            cin >> B[i];
            if (posB[B[i]].empty() && posA[B[i]].empty())
                used.push_back(B[i]);          // value appears only in B
            if (posB[B[i]].empty()) used.push_back(B[i]); // simpler: just mark
            posB[B[i]].push_back(i);
        }

        // Actually we must avoid duplicate entries in `used`.
        // Let's rebuild `used` cleanly.
        used.clear();
        vector<char> mark(MAXV + 1, 0);
        for (int i = 1; i <= N; ++i) {
            if (!mark[A[i]]) { mark[A[i]] = 1; used.push_back(A[i]); }
        }
        for (int i = 1; i <= N; ++i) {
            if (!mark[B[i]]) { mark[B[i]] = 1; used.push_back(B[i]); }
        }

        P.assign(N + 1, 0);
        bool hasDup = false;
        for (int v : used) {
            int c = (int)posA[v].size();
            if (c >= 2) hasDup = true;
            for (int i = 0; i < c; ++i) {
                P[posA[v][i]] = posB[v][i];
            }
        }

        // inversion number D
        Fenwick bit(N);
        long long D = 0;
        for (int i = 1; i <= N; ++i) {
            int p = P[i];
            int notGreater = bit.sum(p);
            int greater = (i - 1) - notGreater;
            D += greater;
            bit.add(p, 1);
        }

        if (!hasDup) {
            for (int v : used) {
                posA[v].clear();
                posB[v].clear();
                mark[v] = 0;
            }
            if (D == 0) {
                cout << 0 << '\n';
                continue;
            }
            if (K % 2 == 0 && (D % 2 != 0)) {
                cout << -1 << '\n';
                continue;
            }
            long long C = (D + K - 1) / K;
            if (K % 2 == 1 && (C & 1LL) != (D & 1LL)) ++C;
            cout << C << '\n';
            continue;
        }

        // ----------- duplicate exists : compute mincount -------------
        struct Query { int x1, y1, x2, y2; };
        vector<Query> qs;
        qs.reserve(N);
        for (int v : used) {
            int c = (int)posA[v].size();
            if (c >= 2) {
                for (int i = 0; i + 1 < c; ++i) {
                    qs.push_back({posA[v][i], posB[v][i],
                                  posA[v][i + 1], posB[v][i + 1]});
                }
            }
        }
        int Q = (int)qs.size();
        vector<Event> ev;
        ev.reserve(4 * Q);
        for (int i = 0; i < Q; ++i) {
            int x1 = qs[i].x1, y1 = qs[i].y1;
            int x2 = qs[i].x2, y2 = qs[i].y2;
            // count inside open rectangle (x1,x2) x (y1,y2)
            ev.push_back({x2 - 1, y2 - 1, i, +1});
            ev.push_back({x2 - 1, y1,     i, -1});
            ev.push_back({x1,     y2 - 1, i, -1});
            ev.push_back({x1,     y1,     i, +1});
        }
        sort(ev.begin(), ev.end());
        Fenwick bit2(N);
        vector<long long> cnt(Q, 0);
        size_t eptr = 0;
        for (int x = 1; x <= N; ++x) {
            bit2.add(P[x], 1);
            while (eptr < ev.size() && ev[eptr].X <= x) {
                int y = ev[eptr].Y;
                if (y > 0) cnt[ev[eptr].idx] += 1LL * ev[eptr].sign * bit2.sum(y);
                ++eptr;
            }
        }

        long long minCount = (1LL << 60);
        for (int i = 0; i < Q; ++i) minCount = min(minCount, cnt[i]);

        long long minDelta = 1 + 2 * minCount;
        long long Deven, Dodd;
        if (D % 2 == 0) {
            Deven = D;
            Dodd  = D + minDelta;
        } else {
            Dodd  = D;
            Deven = D + minDelta;
        }

        long long answer;
        if (K % 2 == 0) {
            // total length always even
            answer = (Deven + K - 1) / K;
        } else {
            // even C
            long long c = (Deven + K - 1) / K;
            if (c & 1LL) ++c;
            long long bestEven = c;
            // odd C
            c = (Dodd + K - 1) / K;
            if ((c & 1LL) == 0) ++c;
            long long bestOdd = c;
            answer = min(bestEven, bestOdd);
        }
        cout << answer << '\n';

        // cleanup for next test case
        for (int v : used) {
            posA[v].clear();
            posB[v].clear();
            mark[v] = 0;
        }
    }
    return 0;
}
