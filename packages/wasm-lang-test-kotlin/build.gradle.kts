plugins {
    kotlin("multiplatform") version "1.9.0"
}

kotlin {
    wasmJs {
        browser()
    }

    sourceSets {
        val wasmJsMain by getting
    }
}
