#include <bits/stdc++.h>
using namespace std;

int main() {
    int n; cin >> n;
    while (n--) {
        string s; cin >> s;
        for (int i = 0; i < 26; i++) {
            for (char & j : s) {
                j -= 'a';
                j++;
                j %= 26;
                j += 'a';
            }
            cout << s << '\n';
        }
    }
}
