use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn fibonacci(n: u32) -> u32 {
    if n <= 1 {
        n
    } else {
        fibonacci(n - 1) + fibonacci(n - 2)
    }
}

#[wasm_bindgen]
pub fn quick_sort(arr: &mut [i32]) {
    if arr.len() <= 1 {
        return;
    }
    let pivot = arr[arr.len() / 2];
    let mut left = 0;
    let mut right = arr.len() - 1;

    loop {
        while arr[left] < pivot {
            left += 1;
        }
        while arr[right] > pivot {
            right -= 1;
        }
        if left >= right {
            break;
        }
        arr.swap(left, right);
        left += 1;
        right -= 1;
    }

    if right > 0 {
        quick_sort(&mut arr[..=right]);
    }
    if left < arr.len() - 1 {
        quick_sort(&mut arr[left..]);
    }
}

#[wasm_bindgen]
pub fn matrix_multiply(size: usize) -> Vec<f64> {
    let mut a = vec![0.0; size * size];
    let mut b = vec![0.0; size * size];
    let mut c = vec![0.0; size * size];

    for i in 0..size * size {
        a[i] = (i as f64) % 10.0;
        b[i] = (i as f64) % 7.0;
    }

    for i in 0..size {
        for j in 0..size {
            let mut sum = 0.0;
            for k in 0..size {
                sum += a[i * size + k] * b[k * size + j];
            }
            c[i * size + j] = sum;
        }
    }

    c
}

#[wasm_bindgen]
pub fn word_frequency(text: &str) -> String {
    use std::collections::HashMap;

    let mut freq = HashMap::new();
    for word in text.split_whitespace() {
        let word = word.to_lowercase();
        *freq.entry(word).or_insert(0) += 1;
    }

    let mut items: Vec<_> = freq.iter().collect();
    items.sort_by(|a, b| b.1.cmp(a.1));

    items
        .iter()
        .take(10)
        .map(|(w, c)| format!("{}:{}", w, c))
        .collect::<Vec<_>>()
        .join(",")
}
