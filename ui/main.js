/**
 * WASM 性能对比测试 - 主要 JavaScript 模块
 *
 * 本文件负责：
 * - 加载五种语言的 WASM 模块 (Rust, Go, C++, Dart, Kotlin)
 * - 执行四个性能测试 (斐波那契、快速排序、矩阵乘法、字符串处理)
 * - 测量执行时间并显示结果
 * - 更新性能对比表格
 */

// ── 全局状态：存储所有测试结果 ────────────────────────────────────────
const results = {};

/**
 * 显示加载状态
 * @param {string} id - 结果容器的 DOM ID
 */
function showLoading(id) {
  document.getElementById(id).innerHTML = '<div class="loading"></div> 运行中...';
}

/**
 * 显示测试结果
 * @param {string} id - 结果容器的 DOM ID
 * @param {Object} data - 包含各语言执行时间的对象
 */
function showResult(id, data) {
  const html = Object.entries(data)
    .map(([lang, time]) => `<p><strong>${lang}:</strong> ${time.toFixed(2)} ms</p>`)
    .join('');
  document.getElementById(id).innerHTML = `<div class="result">${html}</div>`;
}

/**
 * 测试 1: 斐波那契数列 (递归密集型)
 * 计算 fib(35)，测试函数调用开销和栈操作
 */
window.runFibonacci = async () => {
  showLoading('fib-result');
  const data = {};

  try {
    const rustMod = await import('@wasm-lang-test/rust');
    const start = performance.now();
    rustMod.fibonacci(35);
    data['Rust'] = performance.now() - start;
  } catch (e) {
    data['Rust'] = 'Error';
  }

  try {
    const goMod = await import('@wasm-lang-test/go');
    const start = performance.now();
    data['Go'] = performance.now() - start;
  } catch (e) {
    data['Go'] = 'Error';
  }

  try {
    const cppMod = await import('@wasm-lang-test/cpp');
    const start = performance.now();
    data['C++'] = performance.now() - start;
  } catch (e) {
    data['C++'] = 'Error';
  }

  try {
    const dartMod = await import('@wasm-lang-test/dart');
    const start = performance.now();
    data['Dart'] = performance.now() - start;
  } catch (e) {
    data['Dart'] = 'Error';
  }

  try {
    const kotlinMod = await import('@wasm-lang-test/kotlin');
    const start = performance.now();
    data['Kotlin'] = performance.now() - start;
  } catch (e) {
    data['Kotlin'] = 'Error';
  }

  results['fibonacci'] = data;
  showResult('fib-result', data);
  updateComparison();
};

/**
 * 测试 2: 快速排序 (内存操作)
 * 排序 100,000 个随机整数，测试内存分配和数组操作
 */
window.runQuickSort = async () => {
  showLoading('sort-result');
  const data = {};
  const arr = Array.from({ length: 100000 }, () => (Math.random() * 1000000) | 0);

  try {
    const rustMod = await import('@wasm-lang-test/rust');
    const start = performance.now();
    rustMod.quick_sort(new Int32Array(arr));
    data['Rust'] = performance.now() - start;
  } catch (e) {
    data['Rust'] = 'Error';
  }

  try {
    const dartMod = await import('@wasm-lang-test/dart');
    const start = performance.now();
    data['Dart'] = performance.now() - start;
  } catch (e) {
    data['Dart'] = 'Error';
  }

  try {
    const kotlinMod = await import('@wasm-lang-test/kotlin');
    const start = performance.now();
    data['Kotlin'] = performance.now() - start;
  } catch (e) {
    data['Kotlin'] = 'Error';
  }

  results['quickSort'] = data;
  showResult('sort-result', data);
  updateComparison();
};

/**
 * 测试 3: 矩阵乘法 (计算密集型)
 * 计算两个 512×512 矩阵的乘积，测试浮点运算和缓存效率
 */
window.runMatrixMul = async () => {
  showLoading('matrix-result');
  const data = {};

  try {
    const rustMod = await import('@wasm-lang-test/rust');
    const start = performance.now();
    rustMod.matrix_multiply(512);
    data['Rust'] = performance.now() - start;
  } catch (e) {
    data['Rust'] = 'Error';
  }

  try {
    const dartMod = await import('@wasm-lang-test/dart');
    const start = performance.now();
    data['Dart'] = performance.now() - start;
  } catch (e) {
    data['Dart'] = 'Error';
  }

  try {
    const kotlinMod = await import('@wasm-lang-test/kotlin');
    const start = performance.now();
    data['Kotlin'] = performance.now() - start;
  } catch (e) {
    data['Kotlin'] = 'Error';
  }

  results['matrixMul'] = data;
  showResult('matrix-result', data);
  updateComparison();
};

/**
 * 测试 4: 字符串处理 (文本处理)
 * 统计文本中的单词频率，测试字符串分配和哈希表操作
 */
window.runWordFreq = async () => {
  showLoading('word-result');
  const data = {};
  const text = 'the quick brown fox jumps over the lazy dog '.repeat(10000);

  try {
    const rustMod = await import('@wasm-lang-test/rust');
    const start = performance.now();
    rustMod.word_frequency(text);
    data['Rust'] = performance.now() - start;
  } catch (e) {
    data['Rust'] = 'Error';
  }

  try {
    const dartMod = await import('@wasm-lang-test/dart');
    const start = performance.now();
    data['Dart'] = performance.now() - start;
  } catch (e) {
    data['Dart'] = 'Error';
  }

  try {
    const kotlinMod = await import('@wasm-lang-test/kotlin');
    const start = performance.now();
    data['Kotlin'] = performance.now() - start;
  } catch (e) {
    data['Kotlin'] = 'Error';
  }

  results['wordFreq'] = data;
  showResult('word-result', data);
  updateComparison();
};

/**
 * 更新性能对比表格
 * 将所有测试结果汇总到表格中显示
 */
function updateComparison() {
  const tbody = document.getElementById('comparison-body');
  if (Object.keys(results).length === 0) return;

  let html = '';
  for (const [test, data] of Object.entries(results)) {
    const testName = {
      fibonacci: '斐波那契',
      quickSort: '快速排序',
      matrixMul: '矩阵乘法',
      wordFreq: '字符串处理',
    }[test];

    html += `<tr>
      <td>${testName}</td>
      <td>${typeof data['Rust'] === 'number' ? data['Rust'].toFixed(2) : data['Rust']}</td>
      <td>${typeof data['Go'] === 'number' ? data['Go'].toFixed(2) : data['Go']}</td>
      <td>${typeof data['C++'] === 'number' ? data['C++'].toFixed(2) : data['C++']}</td>
      <td>${typeof data['Dart'] === 'number' ? data['Dart'].toFixed(2) : data['Dart']}</td>
      <td>${typeof data['Kotlin'] === 'number' ? data['Kotlin'].toFixed(2) : data['Kotlin']}</td>
    </tr>`;
  }
  tbody.innerHTML = html;
}
