#include <algorithm>
#include <cstring>
#include <map>
#include <sstream>
#include <string>
#include <vector>

extern "C" {

int fibonacci(int n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

void quick_sort(int* arr, int size) {
  if (size <= 1) return;
  int pivot = arr[size / 2];
  int left = 0, right = size - 1;

  while (left <= right) {
    while (arr[left] < pivot) left++;
    while (arr[right] > pivot) right--;
    if (left <= right) {
      std::swap(arr[left], arr[right]);
      left++;
      right--;
    }
  }

  if (right > 0) quick_sort(arr, right + 1);
  if (left < size) quick_sort(arr + left, size - left);
}

double* matrix_multiply(int size) {
  double* a = new double[size * size];
  double* b = new double[size * size];
  double* c = new double[size * size];

  for (int i = 0; i < size * size; i++) {
    a[i] = i % 10;
    b[i] = i % 7;
  }

  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      double sum = 0.0;
      for (int k = 0; k < size; k++) {
        sum += a[i * size + k] * b[k * size + j];
      }
      c[i * size + j] = sum;
    }
  }

  delete[] a;
  delete[] b;
  return c;
}

const char* word_frequency(const char* text) {
  std::map<std::string, int> freq;
  std::istringstream iss(text);
  std::string word;

  while (iss >> word) {
    std::transform(word.begin(), word.end(), word.begin(), ::tolower);
    freq[word]++;
  }

  std::vector<std::pair<std::string, int>> items(freq.begin(), freq.end());
  std::sort(items.begin(), items.end(),
            [](const auto& a, const auto& b) { return a.second > b.second; });

  static std::string result;
  result.clear();
  for (int i = 0; i < std::min(10, (int)items.size()); i++) {
    if (i > 0) result += ",";
    result += items[i].first + ":" + std::to_string(items[i].second);
  }

  return result.c_str();
}
}
