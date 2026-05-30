fun fibonacci(n: Int): Int {
    return if (n <= 1) n else fibonacci(n - 1) + fibonacci(n - 2)
}

fun quickSort(arr: IntArray, left: Int = 0, right: Int = arr.size - 1) {
    if (left >= right) return
    val pivot = arr[(left + right) / 2]
    var i = left
    var j = right

    while (i <= j) {
        while (arr[i] < pivot) i++
        while (arr[j] > pivot) j--
        if (i <= j) {
            val temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp
            i++
            j--
        }
    }

    if (left < j) quickSort(arr, left, j)
    if (i < right) quickSort(arr, i, right)
}

fun matrixMultiply(size: Int): DoubleArray {
    val a = DoubleArray(size * size) { (it % 10).toDouble() }
    val b = DoubleArray(size * size) { (it % 7).toDouble() }
    val c = DoubleArray(size * size)

    for (i in 0 until size) {
        for (j in 0 until size) {
            var sum = 0.0
            for (k in 0 until size) {
                sum += a[i * size + k] * b[k * size + j]
            }
            c[i * size + j] = sum
        }
    }

    return c
}

fun wordFrequency(text: String): String {
    val freq = mutableMapOf<String, Int>()
    text.split(Regex("\\s+")).forEach { word ->
        val lower = word.lowercase()
        freq[lower] = (freq[lower] ?: 0) + 1
    }

    return freq.entries
        .sortedByDescending { it.value }
        .take(10)
        .joinToString(",") { "${it.key}:${it.value}" }
}
