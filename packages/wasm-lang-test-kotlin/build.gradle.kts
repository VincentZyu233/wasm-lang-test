plugins {
    kotlin("multiplatform") version "1.9.23"
}

kotlin {
    wasmJs {
        browser()
    }

    sourceSets {
        val wasmJsMain by getting
    }
}
