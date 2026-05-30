@file:Suppress("UNCHECKED_CAST")

import org.jetbrains.kotlin.gradle.targets.js.dsl.ExperimentalWasmDsl

plugins {
    kotlin("multiplatform") version "1.9.23"
}

repositories {
    mavenCentral()
    google()
}

@OptIn(ExperimentalWasmDsl::class)
kotlin {
    wasmJs {
        browser()
    }

    sourceSets {
        val wasmJsMain by getting
    }
}
