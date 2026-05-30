package main

import (
	"sort"
	"strings"
)

func main() {}

//export fibonacci
func fibonacci(n int) int {
	if n <= 1 {
		return n
	}
	return fibonacci(n-1) + fibonacci(n-2)
}

//export quickSort
func quickSort(arr []int) {
	if len(arr) <= 1 {
		return
	}
	pivot := arr[len(arr)/2]
	left, right := 0, len(arr)-1

	for left <= right {
		for arr[left] < pivot {
			left++
		}
		for arr[right] > pivot {
			right--
		}
		if left <= right {
			arr[left], arr[right] = arr[right], arr[left]
			left++
			right--
		}
	}

	if right > 0 {
		quickSort(arr[:right+1])
	}
	if left < len(arr) {
		quickSort(arr[left:])
	}
}

//export matrixMultiply
func matrixMultiply(size int) []float64 {
	a := make([]float64, size*size)
	b := make([]float64, size*size)
	c := make([]float64, size*size)

	for i := 0; i < size*size; i++ {
		a[i] = float64(i % 10)
		b[i] = float64(i % 7)
	}

	for i := 0; i < size; i++ {
		for j := 0; j < size; j++ {
			sum := 0.0
			for k := 0; k < size; k++ {
				sum += a[i*size+k] * b[k*size+j]
			}
			c[i*size+j] = sum
		}
	}

	return c
}

//export wordFrequency
func wordFrequency(text string) string {
	freq := make(map[string]int)
	for _, word := range strings.Fields(text) {
		freq[strings.ToLower(word)]++
	}

	type kv struct {
		Key   string
		Value int
	}
	var items []kv
	for k, v := range freq {
		items = append(items, kv{k, v})
	}

	sort.Slice(items, func(i, j int) bool {
		return items[i].Value > items[j].Value
	})

	result := make([]string, 0)
	for i := 0; i < len(items) && i < 10; i++ {
		result = append(result, items[i].Key+":"+string(rune(items[i].Value)))
	}

	return strings.Join(result, ",")
}
