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
        browser {
            webpackTask {
                output.libraryTarget = "umd"
            }
        }
        binaries.executable()
    }

    sourceSets {
        val wasmJsMain by getting
    }
}
