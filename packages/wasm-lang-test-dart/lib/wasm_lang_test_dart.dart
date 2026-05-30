int fibonacci(int n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

void quickSort(List<int> arr, [int? left, int? right]) {
  left ??= 0;
  right ??= arr.length - 1;

  if (left >= right) return;

  int pivot = arr[(left + right) ~/ 2];
  int i = left, j = right;

  while (i <= j) {
    while (arr[i] < pivot) i++;
    while (arr[j] > pivot) j--;
    if (i <= j) {
      int temp = arr[i];
      arr[i] = arr[j];
      arr[j] = temp;
      i++;
      j--;
    }
  }

  if (left < j) quickSort(arr, left, j);
  if (i < right) quickSort(arr, i, right);
}

List<double> matrixMultiply(int size) {
  List<double> a = List.filled(size * size, 0.0);
  List<double> b = List.filled(size * size, 0.0);
  List<double> c = List.filled(size * size, 0.0);

  for (int i = 0; i < size * size; i++) {
    a[i] = (i % 10).toDouble();
    b[i] = (i % 7).toDouble();
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

  return c;
}

String wordFrequency(String text) {
  Map<String, int> freq = {};
  for (String word in text.split(RegExp(r'\s+'))) {
    word = word.toLowerCase();
    freq[word] = (freq[word] ?? 0) + 1;
  }

  List<MapEntry<String, int>> items = freq.entries.toList();
  items.sort((a, b) => b.value.compareTo(a.value));

  return items.take(10).map((e) => '${e.key}:${e.value}').join(',');
}
